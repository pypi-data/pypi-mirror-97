from . import constants


def get_memory_limit(config, default=constants.MAX_VIRTUAL_MEMORY):
    extensions = {"": 1, "_kb": 1024, "_mb": 1024 * 1024}
    return _get_with_extensions(config, "memory_limit", default, extensions)
    

def get_timeout(config, default=constants.EXECUTABLE_TIMEOUT):
    extensions = {"": 1, "_sec": 1, "_min": 60, "_ms": 0.001}
    return _get_with_extensions(config, "timeout", default, extensions)

def _get_with_extensions(config, name, default, extensions):
    vals = [getattr(config, f"{name}{extension}") * multiplier 
            for extension, multiplier in extensions.items()
            if hasattr(config, f"{name}{extension}")]
    if len(vals) <= 0:
        return default
    val = min(vals)
    if val < 0:
        return -1
    return val

def get_child_limit(config, base_child_limit):
    if hasattr(config, "child_process_limit"):
        if config.child_process_limit < 0 or base_child_limit < 0:
            return -1
        else:
            return config.child_process_limit + base_child_limit
    return -1 if base_child_limit < 0 else base_child_limit