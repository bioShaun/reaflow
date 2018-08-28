from .base import expression_filter


def extract_params(kwargs):
    def decorate(func):
        func_params = kwargs['params']
        return func(**func_params)
    return decorate
