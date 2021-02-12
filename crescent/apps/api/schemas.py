from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class Context(BaseModel):
    input_text: Optional[str] = None
    options: Optional[Dict[str, Any]] = []


class Contexts(BaseModel):
    contexts: List[Context]


class PopUnknownWordsOption(BaseModel):
    limit: Optional[int]
