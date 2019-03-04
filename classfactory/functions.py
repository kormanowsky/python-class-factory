import inspect


def type_str(value):
    if inspect.isclass(value):
        return "class"
    if callable(value):
        return "function"
    return type(value).__name__
