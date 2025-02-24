import logging
from typing import Any, Optional

from pydantic import BaseModel

from fuzzy.handlers.attacks.base import BaseAttackTechniqueHandler, attack_handler_fm
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.models import AttackResultEntry
from fuzzy.handlers.attacks.piglatin.utils import english_to_pig_latin, is_pig_latin, pig_latin_to_english
from fuzzy.llm.providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)

@attack_handler_fm.flavor(FuzzerAttackMode.PIGLATIN)
class PigLatinAttackHandler(BaseAttackTechniqueHandler[BaseModel]):
    """
    Pig Latin attack - uses pig latin to attack the model.
    """
    def __init__(self, **extra: Any):
        super().__init__(**extra)

    async def _attack(self, prompt: str, **extra: Any) -> Optional[AttackResultEntry]:
        result: Optional[AttackResultEntry] = None
        llm: BaseLLMProvider
        classifications: dict[str, Any] = {}

        async with self._borrow(self._model) as llm:
            # logger.debug("Generating response for prompt: %s", adv_prompt)
            adv_prompt = english_to_pig_latin(prompt)
            response = await llm.generate(adv_prompt, **self._extra)
            if response and is_pig_latin(response.response):
                response.response = pig_latin_to_english(response.response)

            result = AttackResultEntry(original_prompt=prompt,
                                       current_prompt=adv_prompt, 
                                       response=response.response) if response else None
            logger.debug("Response: %s", response.response if response else "None")
            
        classifications = await self._classify_llm_response(response, original_prompt=prompt)
        
        if result:
            result.classifications = classifications

        return result
