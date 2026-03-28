# Root BUILD — global lint/format targets
lint_target = "ai::"

DEFAULT_CPU_RESOLVE = "default_cpu"

ALL_RESOLVES = [DEFAULT_CPU_RESOLVE]

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


