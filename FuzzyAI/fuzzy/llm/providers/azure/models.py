from typing import Literal

from pydantic import BaseModel, Field

from fuzzy.consts import PARAMETER_MAX_TOKENS, ROLE_USER


class AzureGenerateOptions(BaseModel):
    max_tokens: int = Field(0, alias=PARAMETER_MAX_TOKENS) # type: ignore
    
class AzureMessage(BaseModel):
    role: str = ROLE_USER
    content: str
    
class AzureRequest(BaseModel):
    messages: list[AzureMessage]
    max_tokens: int = 5
