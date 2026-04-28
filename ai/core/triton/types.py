from dataclasses import dataclass
import numpy as np
from typing import Mapping, Sequence

@dataclass(frozen=True)
class TritonTensor:
    name: str
    array: np.ndarray
    datatype: str


@dataclass(frozen=True)
class TritonInferenceResult:
    model_name: str
    outputs: Mapping[str, np.ndarray]