import functools

import elasticapm

from .utils import get_function_name


def default_transaction_name_creator(
    func, *args, **kwargs
):
    return get_function_name(func)


def default_result_creator(result):
    return "success"

class CustomAPMClient(elasticapm.Client):
    def capture_function(
        self,
        func,
        transaction_type = "logic",
        transaction_name_creator=None,
        result_creator=None,
    ):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.begin_transaction(transaction_type=transaction_type)
            r = func(*args, **kwargs)
            if transaction_name_creator:
                transaction_name = transaction_name_creator(
                    func, *args, **kwargs
                )
            else:
                transaction_name = default_transaction_name_creator(
                    func, *args, **kwargs
                )

            if result_creator:
                result = result_creator(r)
            else:
                result = default_result_creator(r)
            self.end_transaction(name=transaction_name, result=result)
            return r

        return wrapper
