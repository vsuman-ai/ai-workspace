from __future__ import annotations


from typing import Sequence
from ai.core.triton.types import TritonInferenceResult, TritonTensor
import tritonclient.grpc as grpcclient


class TritonGrpcClient:
    def __init__(
        self,
        url: str,
        *,
        verbose: bool = False,
        ssl: bool = False,
    ) -> None:
        self._client = grpcclient.InferenceServerClient(
            url=url,
            verbose=verbose,
            ssl=ssl,
        )

    def is_server_live(self) -> bool:
        return self._client.is_server_live()

    def is_server_ready(self) -> bool:
        return self._client.is_server_ready()

    def is_model_ready(self, model_name: str, model_version: str = "") -> bool:
        return self._client.is_model_ready(
            model_name=model_name,
            model_version=model_version,
        )

    def infer(
            self,
            *,
            model_name: str,
            inputs: Sequence[TritonTensor],
            output_names: Sequence[str],
            model_version: str = "",
            request_id: str | None = None,
            timeout: float | None = None,
    ) -> TritonInferenceResult:
        infer_inputs = []

        for item in inputs:
            infer_input = grpcclient.InferInput(
                item.name,
                item.array.shape,
                item.datatype,
            )
            infer_input.set_data_from_numpy(item.array)
            infer_inputs.append(infer_input)

        infer_outputs = [
            grpcclient.InferRequestedOutput(name)
            for name in output_names
        ]

        infer_kwargs = {
            "model_name": model_name,
            "inputs": infer_inputs,
            "outputs": infer_outputs,
            "model_version": model_version,
        }

        if request_id is not None:
            infer_kwargs["request_id"] = request_id

        if timeout is not None:
            infer_kwargs["client_timeout"] = timeout

        response = self._client.infer(**infer_kwargs)

        return TritonInferenceResult(
            model_name=model_name,
            outputs={
                name: response.as_numpy(name)
                for name in output_names
            },
        )