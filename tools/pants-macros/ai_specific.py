# type: ignore
SUPPORTED_PLATFORM = "python_linux_amd64"
BASE_IMAGE = "python:3.10-slim"


def ai_py_lib(
    name="lib", sources=None, extra_dependencies=[], dependencies_map={}, overrides=None
):
    _dependencies_map = dependencies_map
    if "neuron" not in _dependencies_map:
        _dependencies_map["neuron"] = []

    python_sources(
        name=name,
        sources=sources,
        overrides=overrides,
        **parametrize(
            "cpu",
            resolve="default_cpu",
            dependencies=(
                []
                + extra_dependencies
                + common_cpu_dependencies(
                    _dependencies_map["cpu"] if "cpu" in _dependencies_map else []
                )
                + common_dependencies(
                    _dependencies_map["common"] if "common" in _dependencies_map else []
                )
            ),
        ),
        **parametrize(
            "neuron",
            resolve="default_neuron",
            dependencies=(
                []
                + extra_dependencies
                + common_neuron_dependencies(
                    _dependencies_map["neuron"] if "neuron" in _dependencies_map else []
                )
                + common_dependencies(
                    _dependencies_map["common"] if "common" in _dependencies_map else []
                )
            ),
        ),
        **parametrize(
            "cuda",
            resolve="default_cuda",
            dependencies=(
                []
                + extra_dependencies
                + common_cuda_dependencies(
                    _dependencies_map["cuda"] if "cuda" in _dependencies_map else []
                )
                + common_dependencies(
                    _dependencies_map["common"] if "common" in _dependencies_map else []
                )
            ),
        ),
    )


def ai_py_app(
    entry_point,
    name="app",
    env={},
    restartable=False,
    dependencies_map={
        "cpu": [":lib@parametrize=cpu"],
        "cuda": [":lib@parametrize=cuda"],
        "neuron": [":lib@parametrize=neuron"],
    },
):

    _dependencies_map = dependencies_map
    if "neuron" not in _dependencies_map:
        _dependencies_map["neuron"] = []


    common_params = {
        "entry_point": entry_point,
        "env": env,
        "execution_mode": "venv",
        "layout": "packed",
        # NOTE: This flag is important to include .so files
        "venv_site_packages_copies": True,
        "include_tools": True,
        # "environment": SUPPORTED_PLATFORM,
        "restartable": restartable,
    }

    pex_binary(
        name=f"{name}-deps",
        include_sources=False,
        **common_params,
        **parametrize("cpu", dependencies=_dependencies_map["cpu"], resolve="default_cpu"),
        **parametrize("neuron", dependencies=_dependencies_map["neuron"], resolve="default_neuron"),
        **parametrize("cuda", dependencies=_dependencies_map["cuda"], resolve="default_cuda"),
    )

    pex_binary(
        name=f"{name}-srcs",
        include_requirements=False,
        **common_params,
        **parametrize("cpu", dependencies=_dependencies_map["cpu"], resolve="default_cpu"),
        **parametrize("neuron", dependencies=_dependencies_map["neuron"], resolve="default_neuron"),
        **parametrize("cuda", dependencies=_dependencies_map["cuda"], resolve="default_cuda"),
    )

    pex_binary(
        name=name,
        **common_params,
        include_sources=True,
        include_requirements=True,
        **parametrize(
            "cpu",
            dependencies=[f":{name}-srcs@parametrize=cpu", f":{name}-deps@parametrize=cpu"],
            resolve="default_cpu",
        ),
        **parametrize(
            "neuron",
            dependencies=[f":{name}-srcs@parametrize=neuron", f":{name}-deps@parametrize=neuron"],
            resolve="default_neuron",
        ),
        **parametrize(
            "cuda",
            dependencies=[f":{name}-srcs@parametrize=cuda", f":{name}-deps@parametrize=cuda"],
            resolve="default_cuda",
        ),
    )


DOCKER_FILE_TEMPLATE = """
FROM {image} as deps
COPY {pex} /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --scope=deps --compile /opt/app
FROM {image} as srcs
COPY {pex} /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --scope=srcs --compile /opt/app
FROM {image}
COPY --from=deps /opt/app /opt/app
COPY --from=srcs /opt/app /opt/app
{entrypoint}
{cmd}
"""


def create_docker_template(image=None, pex=None, entrypoint=None, cmd=None):
    return DOCKER_FILE_TEMPLATE.format(
        image=image,
        pex=pex,
        entrypoint=(
            f"ENTRYPOINT {entrypoint}"
            if entrypoint
            else "ENTRYPOINT [/opt/app/pex]" if not cmd else ""
        ),
        cmd=(f"CMD {cmd}" if cmd else ""),
    )


def ai_py_container(
    tag,
    pex_map={},
    dependencies_map={},
    instructions_map={},
    base_image=BASE_IMAGE,
    name="container",
):
    docker_image(
        name=name,
        repository=tag,
        **parametrize(
            "cpu",
            dependencies=dependencies_map["cpu"] if "cpu" in dependencies_map else [],
            instructions=(
                (
                    DOCKER_FILE_TEMPLATE.format(
                        image=base_image,
                        pex=pex_map["cpu"] if "cpu" in pex_map else "",
                    ).split("\n")
                )
                if "cpu" not in instructions_map
                else instructions_map["cpu"]
            ),
        ),
        **parametrize(
            "cuda",
            dependencies=dependencies_map["cuda"] if "cuda" in dependencies_map else [],
            instructions=(
                (
                    DOCKER_FILE_TEMPLATE.format(
                        image=base_image,
                        pex=pex_map["cuda"] if "cuda" in pex_map else "",
                    ).split("\n")
                )
                if "cuda" not in instructions_map
                else instructions_map["cuda"]
            ),
        ),
        build_platform=["linux/amd64"],
    )
