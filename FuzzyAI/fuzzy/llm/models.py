from pydantic import BaseModel

from fuzzy.models.prompt import BasePrompt


class BaseLLMProviderResponse(BaseModel):
    response: str


class BaseLLMProviderRequest(BaseModel):
    prompt: BasePrompt
