from enum import Enum


class Device(Enum):
    cpu = "cpu"
    cuda = "cuda"
    neuron = "neuron"
