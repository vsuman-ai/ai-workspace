from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import inject, Provide
from ai.sentiment.src.app.dto.common import SentimentClassifierResponse, SentimentClassifierRequest
from ai.sentiment.src.app.containers.app import AppContainer
from ai.sentiment.src.app.services.sentiment_service import SentimentService
from ai.sentiment.src.app.constant.common import MAX_LENGTH

sentiment_router = APIRouter()

@sentiment_router.post("/predict")
@inject
def predict(payload: SentimentClassifierRequest,
            classifier: SentimentService = Depends(Provide[AppContainer.sentiment_service]), ) -> List[SentimentClassifierResponse]:
    texts = [payload.content]
    return classifier.predict(texts=texts, max_length=MAX_LENGTH)