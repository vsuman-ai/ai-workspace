def common_dependency(name, resolve=None):
    if resolve:
        return f"//:reqs#{name}@resolve={resolve}"
    return f"//:reqs#{name}"


def common_dependencies(names, resolve=None):
    return [common_dependency(name, resolve) for name in names]
