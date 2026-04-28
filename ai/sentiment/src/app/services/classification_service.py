from typing import Callable, List
from ai.core.loggers.log_time import log_time
from ai.sentiment.src.app.utils.logger import logger
from ai.core.text_processing.text_processor import TextProcessor
from ai.core.utils.string_utils import is_empty_string
from ai.sentiment.src.app.dto.common import SentimentClassifierResponse
from ai.sentiment.src.app.dto.common import SentimentClassifierRequest
from ai.sentiment.src.app.services.configurations import SentimentClassificationAppConfiguration

class SentimentClassifier:
    classifier: Callable[[str | List[str]], dict]

    def __init__(self):
        self.configurations = SentimentClassificationAppConfiguration()
       

    @log_time(logger=logger)
    def predict(self, dto: SentimentClassifierRequest) -> SentimentClassifierResponse:
        clean_text = (
            TextProcessor(text=dto.content)
            .for_source(source=dto.platform)
            .normalize_whitespace()
            .remove_urls()
            .remove_html()
            .fix_contractions()
            .remove_punctuation()
            .remove_contact_info()
            .text()
        )

        if is_empty_string(clean_text):
            return SentimentClassifierResponse(Raw=dto.content, CleanText=clean_text, sentiment="None")

        sentiment_resp = self.classifier(dto.content)

        return SentimentClassifierResponse(
            Raw=dto.content,
            CleanText=clean_text,
            sentiment=sentiment_resp[0]["label"],
        )


