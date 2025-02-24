import json
import logging
from typing import Any, Optional, Type

from pydantic import BaseModel, Field

from fuzzy.handlers.attacks.base import BaseAttackTechniqueHandler, attack_handler_fm
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.models import AttackResultEntry
from fuzzy.handlers.attacks.taxonomy.prompts import PERSUASION_PROMPT
from fuzzy.handlers.db.adv_prompts import AdversarialPromptDTO
from fuzzy.llm.models import BaseLLMProviderResponse
from fuzzy.llm.providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)

MAX_RETRY_COUNT = 1

class TaxonomyParaphraserExtraParams(BaseModel):
    taxonomy_model: Optional[str] = Field(None, description="Model to be used for generated taxonomy prompts")
    
@attack_handler_fm.flavor(FuzzerAttackMode.TAXONOMY)
class TaxonomyParaphraser(BaseAttackTechniqueHandler[TaxonomyParaphraserExtraParams]):
    """
    Taxonomy Paraphraser attack technique (https://arxiv.org/pdf/2401.06373)
    """

    def __init__(self, **extra: Any):
        super().__init__(**extra)

        self._taxonomies: list[dict[str, Any]] = []

        self._load_taxonomy_dataset()
        self._original_prompt_responses: dict[str, str] = {}
    
    @classmethod
    def extra_args_cls(cls) -> Type[BaseModel]:
        return TaxonomyParaphraserExtraParams
    
    def _load_taxonomy_dataset(self) -> None:
        with open('resources/persuasion_taxonomy.jsonl', 'r') as f:
            data = f.read()

        self._taxonomies = [json.loads(jline) for jline in data.splitlines()]
    
    def _generate_attack_params(self, prompts: list[AdversarialPromptDTO]) -> list[dict[str, Any]]:
        return [{"prompt": prompt.prompt, "taxonomy": taxonomy} for prompt in prompts for taxonomy in self._taxonomies]

    async def _reduce_attack_params(self, entries: list[AttackResultEntry], 
                                    attack_params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        
        updated_params = [param for param in attack_params
                            if not any(entry.original_prompt == param['prompt'] and entry.extra['category'] == param['taxonomy']['ss_technique']
                                for entry in entries)]
        
        return updated_params
    
    async def _attack(self, prompt: str, taxonomy: dict[str, Any], **extra: Any) -> Optional[AttackResultEntry]:
        result: Optional[AttackResultEntry] = None
        llm: BaseLLMProvider
        num_tries = 0
        classifications = {}

        max_tokens = self._extra.get("max_tokens", 200)

        async with self._borrow(self._model) as llm:
            if prompt not in self._original_prompt_responses:
                logger.debug("Generating original response for prompt: %s", prompt)
                response = await llm.generate(prompt, max_tokens=max_tokens)
                self._original_prompt_responses[prompt] = response.response if response else str()
                
        while num_tries < MAX_RETRY_COUNT:
            num_tries += 1
            
            async with self._borrow(self._extra_args.taxonomy_model or self._model) as llm:
                category, posioned_question = await self._generate_poisioned(llm, prompt, taxonomy)

            result = AttackResultEntry(original_prompt=prompt,
                                    current_prompt=posioned_question,
                                    extra={"category": category})
            
            async with self._borrow(self._model) as llm:
                llm_response = await llm.generate(posioned_question, max_tokens=max_tokens)

            classifications = await self._classify_llm_response(llm_response, original_prompt=prompt)
            result.extra["sample_rounds"] = num_tries
            result.response = llm_response.response if llm_response else None # type: ignore
            
            if any(x == 1 for x in classifications.values()):
                break
                
        if result:
            result.extra['original_response'] = self._original_prompt_responses[prompt]
            result.classifications = classifications
            
        return result

    async def _generate_poisioned(self, llm: BaseLLMProvider, prompt: str, taxonomy: dict[str, Any]) -> tuple[str, str]:
        category = taxonomy['ss_technique']
        definition = taxonomy['ss_definition']
        example = taxonomy['ss_example']
        logger.debug("Generating poisoned prompt for category: %s", category)
        full_prompt = PERSUASION_PROMPT % (category, definition, example, prompt, category, prompt, prompt)
        response: Optional[BaseLLMProviderResponse] = await llm.generate(full_prompt, temperature=1.0, top_p=1.0, max_tokens=500)
        poisoned_prompt = response.response if response else str()
        
        if poisoned_prompt.startswith("\""):
            poisoned_prompt = poisoned_prompt[1:]
        if poisoned_prompt.endswith("\""):
            poisoned_prompt = poisoned_prompt[:-1]

        return category, poisoned_prompt

        