from elasticapm.instrumentation.packages.base import AbstractInstrumentedModule
from elasticapm.traces import capture_span

from .utils import get_function_name, get_module_funcs


def _instrument_method(self):
    for handler, args in self._before_instrument_handlers:
        handler(self, **args)
    result = super(self.__class__, self).instrument()
    for handler, args in self._before_instrument_handlers:
        handler(self, **args)
    return result


def call_method(self, module, method, wrapped, instance, args, kwargs):
    signature = get_function_name(wrapped)

    with capture_span(
        signature,
        span_type=self.span_type,
        span_subtype=self.span_subtype,
    ) as span:
        return wrapped(*args, **kwargs)


class InstrumentationBuilder:
    def __init__(self, name: str) -> None:
        self.name = name
        self._span_type = "logic"
        self._span_subtype = "function"
        self._instrument_list = []
        self._before_instrument_handlers = []
        self._after_instrument_handlers = []
        self._call_handler = call_method
        self._methods = {}
        self._attributes = {}

    def set_call_method(self, call_method):
        self._call_handler = call_method

    def set_span_type(self, span_type):
        self._span_type = span_type

    def set_span_subtype(self, span_subtype):
        self._span_subtype = span_subtype

    def add_instrument(self, module, func_pattern):
        functions = get_module_funcs(module, func_pattern)
        self._instrument_list.extend(functions)

    def add_before_instrument_handler(self, handler):
        self._before_instrument_handlers.append(handler)

    def add_after_instrument_handler(self, handler):
        self._after_instrument_handlers.append(handler)

    def create_metadata(self):
        self.methods = {
            "instrument": _instrument_method,
            "call": self._call_handler,
        }
        self.attributes = {
            "name": self.name,
            "instrument_list": self._instrument_list,
            "span_type": self._span_type,
            "span_subtype": self._span_subtype,
            "_before_instrument_handlers": self._before_instrument_handlers,
            "_after_instrument_handlers": self._after_instrument_handlers,
        }
        return (
            self.name,
            (AbstractInstrumentedModule,),
            {**self.attributes, **self.methods},
        )

    def create_instrument(self):
        name, base, attrs = self.create_metadata()
        return type(name, base, attrs)
