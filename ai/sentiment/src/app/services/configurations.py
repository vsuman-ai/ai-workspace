from enum import Enum

from ai.core.configurations import BaseConfigurations
from ai.sentiment.src.app.constant.common import SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID

class EnvMapping(Enum):
    inferenceModelID = "SENTIMENT_MODEL_ID"
    tritonInferenceUrl = "TRITON_INFERENCE_URL"

class SentimentClassificationAppConfiguration(BaseConfigurations):

    def get_inference_model_id(self):
        return self.get_env(EnvMapping.inferenceModelID.value, SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID)

    def get_triton_inference_url(self):
        return self.get_env(EnvMapping.tritonInferenceUrl.value)

__all__ = ["SentimentClassificationAppConfiguration"]