

SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID = "finiteautomata/bertweet-base-sentiment-analysis"
ID2LABEL = {
        0: "NEG",
        1: "NEU",
        2: "POS",
    }
SENTIMENT_CLASSIFICATION_ONNX_MODEL_ID = "bertweet_sentiment_onnx"
MAX_LENGTH = 128

__all__ = ["SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID", "ID2LABEL", "SENTIMENT_CLASSIFICATION_ONNX_MODEL_ID",
           "MAX_LENGTH"]