import logging
import os
from typing import Any, Optional, Union

import aiohttp
import backoff
import tiktoken

from fuzzy.consts import ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER
from fuzzy.handlers.tokenizers.handler import TokensHandler  # type: ignore
from fuzzy.llm.models import BaseLLMProviderResponse
from fuzzy.llm.providers.base import (BaseLLMMessage, BaseLLMProvider, BaseLLMProviderException,
                                      BaseLLMProviderRateLimitException, llm_provider_fm)
from fuzzy.llm.providers.enums import LLMProvider, LLMProviderExtraParams
from fuzzy.llm.providers.openai.models import OpenAIChatRequest
from fuzzy.llm.providers.shared.decorators import api_endpoint

logger = logging.getLogger(__name__)

class OpenAIProviderException(BaseLLMProviderException):
    pass

OPENAI_API_BASE_URL = "https://api.openai.com/v1"
O1_FAMILY_MODELS = ["o1-mini","o1-preview"]

@llm_provider_fm.flavor(LLMProvider.OPENAI)
class OpenAIProvider(BaseLLMProvider):
    OPENAI_API_KEY = "OPENAI_API_KEY"
    CHAT_COMPLETIONS_URL = f"{OPENAI_API_BASE_URL}/chat/completions"

    def __init__(self, model: str, **extra: Any):
        super().__init__(model=model, **extra)

        if (api_key := os.environ.get(self.OPENAI_API_KEY)) is None:
            raise BaseLLMProviderException(f"{self.OPENAI_API_KEY} not in os.environ")

        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        self._session = aiohttp.ClientSession(headers=self._headers)

        self._base_url = OPENAI_API_BASE_URL
        self._tokenizer = tiktoken.encoding_for_model(model_name=model)
        self.tokens_handler = TokensHandler(tokenizer=self._tokenizer)

    @classmethod
    def get_supported_models(cls) -> Union[list[str], str]:
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "o1-mini", "o1-preview"]

    
    @api_endpoint("/chat/completions")
    async def generate(self, prompt: str, url: str, system_prompt: Optional[str] = None, **extra: Any) -> Optional[BaseLLMProviderResponse]:
        messages = [BaseLLMMessage(role=ROLE_USER, content=prompt)]
        if self._model_name not in O1_FAMILY_MODELS and system_prompt is not None:
            messages = [BaseLLMMessage(role=ROLE_SYSTEM, content=system_prompt)] + messages

        return await self.chat(messages=messages, **extra) # type: ignore

    @backoff.on_exception(backoff.expo, BaseLLMProviderRateLimitException, max_value=10)
    @api_endpoint("/chat/completions")
    async def chat(self, messages: list[BaseLLMMessage], url: str, system_prompt: Optional[str] = None, **extra: Any) -> BaseLLMProviderResponse:
        error: dict[str, Any]
        
        if self._model_name not in O1_FAMILY_MODELS and system_prompt is not None:
            messages = [BaseLLMMessage(role=ROLE_SYSTEM, content=system_prompt)] + messages

        try:
            request = OpenAIChatRequest(model=self._model_name, messages=messages, **extra)
            async with self._session.post(url, json=request.model_dump()) as response:
                openai_response = await response.json()
                if (error := openai_response.get("error")) is not None:
                    if error.get('code') == 'rate_limit_exceeded':
                        logger.debug(f'Rate limit exceeded')
                        raise BaseLLMProviderRateLimitException()
                    else:
                        raise OpenAIProviderException('OpenAI error: ' + error.get('message'))
                    
                return BaseLLMProviderResponse(response=openai_response["choices"][0]['message']['content'])
        except (BaseLLMProviderRateLimitException, OpenAIProviderException) as e:
            raise e
        except Exception as e:            
            logger.error(f'Error generating text: {e}')
            raise OpenAIProviderException('Cant generate text')
    
    @backoff.on_exception(backoff.expo, BaseLLMProviderRateLimitException, max_value=10)
    def sync_generate(self, prompt: str, **extra: Any) -> Optional[BaseLLMProviderResponse]:
        messages = [BaseLLMMessage(role=ROLE_USER, content=prompt)]
        
        if extra.get(LLMProviderExtraParams.APPEND_LAST_RESPONSE):
            if history := self.get_history():
                messages.append(BaseLLMMessage(role=ROLE_ASSISTANT, content=history[-1].response))
        
        chat_extra_params = {k:v for k, v in extra.items() if k not in [LLMProviderExtraParams.APPEND_LAST_RESPONSE]}
        return self.sync_chat(messages, **chat_extra_params)

    async def close(self) -> None:
        await self._session.close()
