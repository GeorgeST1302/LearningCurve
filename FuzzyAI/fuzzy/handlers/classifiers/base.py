import abc
import inspect
from typing import Any, Type

from fuzzy.utils.flavor_manager import FlavorManager


class BaseClassifier(abc.ABC):
    """
    Base class for classifiers.
    """
    def __init__(self, **extra: Any) -> None:
        self._name = str()

    """
    Run the classification logic. Explicitly extract the needed parameter in the function signature.
    """
    @abc.abstractmethod
    async def classify(self, *args: Any, **extra: Any) -> Any: ...

    @abc.abstractmethod
    def sync_classify(self, *args: Any, **extra: Any) -> Any: ...

    @property
    def name(self) -> str:
        return self._name 

    @classmethod
    def description(cls) -> str:
        return cls.__doc__ or "No description available"
    
    @classmethod
    def requires_llm(cls) -> bool:
        method_signature = inspect.signature(cls.classify)
        if "llm" not in method_signature.parameters:
            return False
        
        param = method_signature.parameters['llm']
        return bool(param.default == inspect.Parameter.empty)
    
classifiers_fm: FlavorManager[str, Type[BaseClassifier]] = FlavorManager()
