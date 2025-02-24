import abc
import asyncio
from typing import Any, Callable, Optional, Type, TypeVar, Union, overload

from pydantic import BaseModel

from fuzzy.llm.chain import FuzzChain, FuzzNode
from fuzzy.llm.models import BaseLLMProviderResponse
from fuzzy.llm.providers.enums import LLMProvider
from fuzzy.utils.flavor_manager import FlavorManager

T = TypeVar('T')
KeyT = TypeVar('KeyT')
ValT = TypeVar('ValT')


class BaseLLMProviderRateLimitException(Exception):
    pass

class BaseLLMProviderException(Exception):
    pass

class BaseLLMMessage(BaseModel):
    role: str
    content: str

class BaseLLMProvider(abc.ABC):
    """
    Base class for Language Model Providers.
    Args:
        model (str): The model to use.
        **extra (Any): Additional arguments for the provider.
    """
    def __init__(self, provider: LLMProvider, model: str, **extra: Any) -> None:
        super().__init__()

        self._qualified_model_name = f"{provider.value}/{model}"
        self._model_name = model

        self._history: list[BaseLLMProviderResponse] = []

    @abc.abstractmethod
    async def generate(self, prompt: str, **extra: Any) -> Optional[BaseLLMProviderResponse]:
        ...
        
    @abc.abstractmethod
    async def chat(self, messages: list[BaseLLMMessage], **extra: Any) -> Optional[BaseLLMProviderResponse]:
        ...
    
    @abc.abstractmethod
    async def close(self) -> None:
        ...
        
    @classmethod
    @abc.abstractmethod
    def get_supported_models(cls) -> Union[list[str], str]:
        ...

    def sync_generate(self, prompt: str, **extra: Any) -> Optional[BaseLLMProviderResponse]:
        return asyncio.run(self.generate(prompt, **extra))

    def sync_chat(self, messages: list[BaseLLMMessage], **extra: Any) -> Optional[BaseLLMProviderResponse]:
        return asyncio.run(self.chat(messages, **extra))
    
    def add_to_history(self, responses: list[BaseLLMProviderResponse]) -> None:
        self._history.extend(responses)
    
    def clear_history(self) -> None:
        self._history.clear()
    
    def get_history(self) -> list[BaseLLMProviderResponse]:
        return self._history
    
    @property
    def qualified_model_name(self) -> str:
        return self._qualified_model_name
    
    @property
    def history(self) -> list[BaseLLMProviderResponse]:
        return self._history
    
    def __or__(self, other: Union[FuzzNode, FuzzChain, str]) -> FuzzChain:
        if other.__class__ == FuzzChain:
            return FuzzChain([FuzzNode(self, "{input}"), *other._nodes]) # type: ignore
        elif other.__class__ == FuzzNode:
            return FuzzChain([FuzzNode(self, "{input}"), other]) # type: ignore
        elif other.__class__ == str:
            return FuzzChain([FuzzNode(self, other)]) # type: ignore
            
        raise ValueError(f"Invalid type for other: {other.__class__}")

    def __repr__(self) -> str:
        return f"model: {self._model_name}"
    
    def __str__(self) -> str:
        return f"model: {self._model_name}"
    
class ProviderFlavorManager(FlavorManager[KeyT, ValT]):
    def __init__(self) -> None:
        super().__init__()

    @overload
    def flavor(self, flavor: KeyT) -> Callable[[T], T]:
        ...

    @overload
    def flavor(self, flavor: KeyT, value: ValT) -> None:
        ...

    def flavor(self, flavor: KeyT, value: Optional[ValT] = None) -> Optional[Callable[[T], T]]:
        if value is not None:
            return super().flavor(flavor, value)

        fm_super = super()

        def decorator(cls: T) -> T:
            original_init = cls.__init__ # type: ignore

            def new_init(self, *args: Any, **kwargs: Any) -> None: # type: ignore
                kwargs['provider'] = flavor
                original_init(self, *args, **kwargs)

            cls.__init__ = new_init  # type: ignore
            return fm_super.flavor(flavor)(cls) # type: ignore

        return decorator
    
llm_provider_fm: ProviderFlavorManager[str, Type[BaseLLMProvider]] = ProviderFlavorManager()
