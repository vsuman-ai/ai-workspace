from __future__ import annotations
from typing import Optional
import numpy as np
from transformers import AutoTokenizer

from ai.core.triton.grpc_client import TritonGrpcClient, TritonTensor
from ai.sentiment.src.app.constant.common import (ID2LABEL,
                                                  SENTIMENT_CLASSIFICATION_ONNX_MODEL_ID,
                                                  SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID,
                                                  MAX_LENGTH)
from ai.sentiment.src.app.dto.common import SentimentClassifierResponse
from ai.core.loggers.log_time import log_time
from ai.sentiment.src.app.utils.logger import logger


class SentimentService:
    def __init__(
        self,
        *,
        triton_url: str,
        model_name: Optional[str] = SENTIMENT_CLASSIFICATION_ONNX_MODEL_ID,
        tokenizer_model: Optional[str] = SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID,
    ) -> None:
        self.ID2LABEL = ID2LABEL
        self.model_name = model_name
        self.triton = TritonGrpcClient(url=triton_url)
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_model,
            use_fast=False,
        )

    @log_time(logger=logger)
    def predict(
        self,
        texts: list[str],
        *,
        max_length: int = MAX_LENGTH,
    ) -> list[SentimentClassifierResponse]:
        if isinstance(texts, str):
            texts = [texts]

        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="np",
        )

        encoded.pop("token_type_ids", None)

        result = self.triton.infer(
            model_name=self.model_name,
            inputs=[
                TritonTensor(
                    name="input_ids",
                    array=encoded["input_ids"].astype(np.int64),
                    datatype="INT64",
                ),
                TritonTensor(
                    name="attention_mask",
                    array=encoded["attention_mask"].astype(np.int64),
                    datatype="INT64",
                ),
            ],
            output_names=["logits"],
        )

        logits = result.outputs["logits"]
        probs = self._softmax(logits)

        predictions = []

        for text, logit, prob in zip(texts, logits, probs):
            label_id = int(np.argmax(prob))
            label = self.ID2LABEL[label_id]

            predictions.append(
                SentimentClassifierResponse(
                    text=text,
                    label=label,
                    score=float(prob[label_id]),
                    logits=logit.tolist(),
                    probabilities={
                        self.ID2LABEL[i]: float(prob[i])
                        for i in range(len(prob))
                    },
                )
            )

        return predictions

    @staticmethod
    def _softmax(logits: np.ndarray) -> np.ndarray:
        logits = logits - np.max(logits, axis=-1, keepdims=True)
        exp = np.exp(logits)
        return exp / np.sum(exp, axis=-1, keepdims=True)