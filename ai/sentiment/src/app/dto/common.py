from typing import List, Dict

from pydantic import BaseModel
from ai.core.enums.source_type import SourceType

class Probability(BaseModel):
    label: str
    score: float


class SentimentClassifierResponse(BaseModel):
    text: str
    label: str
    score: float
    logits: List[float]
    probabilities: Dict[str, float]

class SentimentClassifierRequest(BaseModel):
    content: str
    platform: SourceType = SourceType.TWITTER


__all__ = ["SentimentClassifierResponse", "SentimentClassifierRequest"]