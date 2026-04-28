

class FixedTokenizer:
    def __init__(self, base, max_length=128, truncation=True, return_tensors="pt"):
        self._base = base
        self._max_length = max_length
        self._truncation = truncation
        self._return_tensors = return_tensors

    def __call__(self, *args, **_ignored_kwargs):
        return self._base(
            *args,
            padding="max_length",
            truncation=True,
            max_length=self._max_length,
            return_tensors=self._return_tensors,
        )

    def __getattr__(self, name):
        return getattr(self._base, name)
