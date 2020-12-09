import inspect

# TODO: These functions are not fully thought out, misplaced, and/or wrong. Fix it tomorrow


def infer_function_return_type(func):
    """
    Infer the return type of a function from the type annotation
    :param func:
    :return: return type(s), or None if no annotation exists
    """
    annotation = inspect.signature(func).return_annotation
    if annotation == inspect.Signature.empty:
        return None
    return annotation


def infer_function_param_types(func):
    sig = inspect.signature(func)
    return sig.parameters

