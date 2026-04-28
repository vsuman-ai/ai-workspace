def common_dependency(name, resolve=None):
    if resolve:
        return f"//:reqs#{name}@resolve={resolve}"
    return f"//:reqs#{name}"


def common_dependencies(names, resolve=None):
    return [common_dependency(name, resolve) for name in names]

def common_cpu_dependency(name, resolve=None):
    if resolve:
        return f"//:reqs_cpu#{name}@resolve={resolve}"
    return f"//:reqs_cpu#{name}"

def common_cpu_dependencies(names, resolve=None):
    return [common_cpu_dependency(name, resolve) for name in names]

def common_cuda_dependency(name, resolve=None):
    if resolve:
        return f"//:reqs_cuda#{name}@resolve={resolve}"
    return f"//:reqs_cuda#{name}"

def common_cuda_dependencies(names, resolve=None):
    return [common_cuda_dependency(name, resolve) for name in names]

def common_neuron_dependency(name, resolve=None):
    if resolve:
        return f"//:reqs_neuron#{name}@resolve={resolve}"
    return f"//:reqs_neuron#{name}"

def common_neuron_dependencies(names, resolve=None):
    return [common_neuron_dependency(name, resolve) for name in names]
