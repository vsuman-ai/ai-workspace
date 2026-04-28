DEVICE_DEPENDENCIES = ["torch", "numpy", "transformers"]

ai_py_lib(
    sources=["src/**/*.py", "cli/**/*.py", "neuron/**/*.py"],
    dependencies_map={
      "common": [],
      "cpu": DEVICE_DEPENDENCIES,
      "cuda": DEVICE_DEPENDENCIES,
    },
    extra_dependencies=[
        "ai/core/triton:lib",
    ]
)

ai_py_app(
    "cli/run_cli.py",
    dependencies_map={
        "cpu": [":lib@parametrize=cpu"],
        "cuda": [":lib@parametrize=cuda"],
        "neuron": [":lib@parametrize=neuron"],
    },
)
