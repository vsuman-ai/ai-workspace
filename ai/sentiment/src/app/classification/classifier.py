from typing import Callable, List

from ai.core.text_processing.text_processor import TextProcessor
from ai.core.utils.string_utils import is_empty_string
from ai.sentiment.src.app.classification.model_loader import (
    SentimentModelLoader,
)
from ai.sentiment.src.app.dto.common import SentimentClassifierResponse


class SentimentClassifier:
    classifier: Callable[[str | List[str]], dict]

    def __init__(self, model_id: str, device: str):
        self.classifier = SentimentModelLoader.load_model(model_id=model_id, device=device)

    def classify(self, content, platform) -> SentimentClassifierResponse:

        clean_text = (
            TextProcessor(text=content)
            .for_source(platform)
            .normalize_whitespace()
            .remove_urls()
            .remove_html()
            .fix_contractions()
            .remove_punctuation()
            .remove_contact_info()
            .text()
        )

        if is_empty_string(clean_text):
            return SentimentClassifierResponse(Raw=content, CleanText=clean_text, sentiment="None")

        sentiment_resp = self.classifier(content)

        return SentimentClassifierResponse(
            Raw=content,
            CleanText=clean_text,
            sentiment=sentiment_resp[0]["label"],
        )
