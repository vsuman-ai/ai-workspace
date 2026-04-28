import os
import time

import torch
import torch_neuronx as tnx
import tqdm
from huggingface_hub import upload_folder as hf_upload_folder, login as hf_login
from pydantic import BaseModel
from torch import nn
from transformers import (
    AutoTokenizer,
    pipeline,
    AutoConfig,
    AutoModelForSequenceClassification,
)
from ai.core.tokenizer.fixed_tokenizer import FixedTokenizer


class NeuronWrapper(nn.Module):
    """
    Wraps a TorchScript-compiled NeuronX model and exposes a HF-like interface
    for the pipeline. Assumes the graph was traced with (input_ids, attention_mask)
    as positional args and returns (logits,).
    """

    def __init__(self, jit_module: torch.jit.ScriptModule, config):
        super().__init__()
        self.jit = jit_module
        self.config = config  # pipeline reads labels/num_labels from here

    def forward(self, **inputs):
        input_ids = inputs["input_ids"]
        attention_mask = inputs.get("attention_mask")
        # Call with the SAME positional signature used during trace:
        if attention_mask is None:
            logits = self.jit(input_ids)
        else:
            logits = self.jit(input_ids, attention_mask)
        # Ensure a tuple is returned (pipeline expects logits in first slot)
        return {"logits": logits}


class AWSNeuron(BaseModel):
    device: str
    model_id: str
    folder: str
    compiled_name: str | None = "neuronx_token_cls.pt"

    def trace(self):
        tok = AutoTokenizer.from_pretrained(self.model_id)

        tok.save_pretrained(self.folder)

        model = AutoModelForSequenceClassification.from_pretrained(self.model_id, return_dict=False)
        model.eval()
        model.config.to_json_file(f"{self.folder}/config.json")
        cfg = AutoConfig.from_pretrained(self.model_id)
        cfg.compiled_filename = self.compiled_name
        cfg.save_pretrained(self.folder)

        enc = tok.encode_plus(
            "The company HuggingFace is based in New York City",
            "HuggingFace's headquarters are situated in Manhattan",
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        # Build example inputs as a tuple, not a dict
        example_inputs = (enc["input_ids"], enc.get("attention_mask"))

        # Warm up eager model (kwargs are fine here)
        _ = model(input_ids=enc["input_ids"], attention_mask=enc.get("attention_mask"))

        # Analyze + compile
        tnx.analyze(model, example_inputs)
        neff = tnx.trace(model, example_inputs)
        torch.jit.save(neff, f"./{self.folder}/{self.compiled_name}")
        print(f"✅ Compiled & saved {self.folder}/{self.compiled_name}")

        hf_login(token=os.getenv("HF_TOKEN"))
        hf_upload_folder(
            folder_path=self.folder,
            repo_id="Ontic-Tech/bertweet-base-sentiment-analysis-traced-128-tkn",
            repo_type="model",
        )

    def test_model(self):
        string_inputs = [
            "I love to eat pizza!",
            "I am sorry. I really want to like it, but I just can not stand sushi.",
            "I really do not want to type out 128 strings to create batch 128 data.",
            "Ah! Multiplying this list by 32 would be a great solution!",
        ]
        string_inputs = string_inputs * 32

        original_tokenizer = AutoTokenizer.from_pretrained(self.model_id, use_fast=True)

        fixed_tokenizer = FixedTokenizer(base=original_tokenizer, max_length=128, truncation=True, return_tensors="pt")

        compiled_name = "neuronx_token_cls.pt"
        compiled_path = f"{self.model_id}/{compiled_name}"

        cfg = AutoConfig.from_pretrained(self.model_id)
        jit_model = torch.jit.load(compiled_path).eval()

        wrapped = NeuronWrapper(jit_module=jit_model, config=cfg)

        neuron_pipe = pipeline(
            "sentiment-analysis", model=wrapped, tokenizer=fixed_tokenizer, framework="pt"
        )

        neuron_pipe(string_inputs)

        neuron_b128_times = []
        print(f"Total Batch {100} & each Batch size 128 sentences")
        iterate_range = 100
        for _ in tqdm.tqdm(range(iterate_range)):
            start = time.time()
            _ = neuron_pipe(string_inputs)
            end = time.time()
            neuron_b128_times.append(end - start)

        neuron_b128_times = sorted(neuron_b128_times)

        print(
            f"Average throughput for batch 128 neuron model is {(sum(neuron_b128_times)/len(neuron_b128_times))/128} sentences/s."
        )
        print(
            f"Peak throughput for batch 128 neuron model is {min(neuron_b128_times)/128} sentences/s."
        )
        print()

        print(
            f"50th percentile latency for batch 128 neuron model is {neuron_b128_times[int(iterate_range*.5)] * 1000} ms."
        )
        print(
            f"90th percentile latency for batch 128 neuron model is {neuron_b128_times[int(iterate_range*.9)] * 1000} ms."
        )
        print(
            f"95th percentile latency for bacth 128 neuron model is {neuron_b128_times[int(iterate_range*.95)] * 1000} ms."
        )
        print(
            f"99th percentile latency for batch 128 neuron model is {neuron_b128_times[int(iterate_range*.99)] * 1000} ms."
        )
        print()
