from transformers import AutoTokenizer


class BertTweetTokenizer:
    def __init__(
        self,
        model_name: str = "finiteautomata/bertweet-base-sentiment-analysis",
        use_fast: bool = False,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=use_fast,
        )

    def encode(self, texts: list[str], max_length: int = 128) -> dict:
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="np",
        )

        encoded.pop("token_type_ids", None)

        return encoded