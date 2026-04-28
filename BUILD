# Root BUILD — global lint/format targets
lint_target = "ai::"

DEFAULT_CPU_RESOLVE = "default_cpu"
DEFAULT_CUDA_RESOLVE = "default_cuda"
DEFAULT_NEURON_RESOLVE = "default_neuron"

ALL_RESOLVES = [DEFAULT_CPU_RESOLVE, DEFAULT_CUDA_RESOLVE, DEFAULT_NEURON_RESOLVE]

####################################################################################################
# Requirements
####################################################################################################

python_requirements(
    name="reqs",
    source="3rdParty/requirements-common.txt",
    resolve=parametrize(*ALL_RESOLVES),
    overrides={
        "clean-text": {"modules": ["cleantext"]},
        "dspy-ai": {"modules": ["dspy"]},
    },
)
python_requirements(
    name="reqs_cpu",
    source="3rdParty/requirements-cpu.txt",
    resolve=DEFAULT_CPU_RESOLVE,
    overrides={
        "optimum": {"modules": ["optimum", "onnxruntime"]},
        "transformers": {"modules": ["transformers", "tokenizers"]},
        "protobuf": {"modules": ["google", "protobuf"]},
        "google-api-python-client": {"modules": ["googleapiclient"]},
        "sentence-transformers": {"modules": ["sentence_transformers"]},
    },
)

python_requirements(
    name="reqs_neuron",
    source="3rdParty/requirements-neuron.txt",
    resolve=DEFAULT_NEURON_RESOLVE,
    overrides={
        "optimum-neuron": {"modules": ["optimum.neuron", "torch", "optimum", "transformers" ]},
        "protobuf": {"modules": ["google", "protobuf"]},
        "sentence-transformers": {"modules": ["sentence_transformers"]},
    },
)

python_requirements(
    name="reqs_cuda",
    source="3rdParty/requirements-cuda.txt",
    resolve=DEFAULT_CUDA_RESOLVE,
    overrides={
        "optimum": {"modules": ["optimum", "onnxruntime"]},
        "transformers": {"modules": ["transformers", "tokenizers"]},
        "protobuf": {"modules": ["google", "protobuf"]},
        "sentence-transformers": {"modules": ["sentence_transformers"]},
    },
)

####################################################################################################
# Environments
####################################################################################################

docker_environment(
    name="python_linux_amd64",
    platform="linux_x86_64",
    image="python@sha256:4a5330e9f281d53214299d80d98198dcda3ce97ada3f3d48f2e617d43a6e15b3",
)

docker_environment(
    name="python_linux_arm64",
    platform="linux_arm64",
    image="python@sha256:74c52fb8fa25b6aa1a7cd25cce70e45d638c88fdf0d8b649f2334e2fb3fc8d43",
)


