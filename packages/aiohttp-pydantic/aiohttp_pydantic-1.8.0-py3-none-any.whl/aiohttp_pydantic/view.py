from functools import update_wrapper
from inspect import iscoroutinefunction
from typing import Any, Callable, Generator, Iterable

from aiohttp.abc import AbstractView
from aiohttp.hdrs import METH_ALL
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_response import StreamResponse
from pydantic import ValidationError

from .injectors import (
    AbstractInjector,
    BodyGetter,
    HeadersGetter,
    MatchInfoGetter,
    QueryGetter,
    _parse_func_signature,
)


class PydanticView(AbstractView):
    """
    An AIOHTTP View that validate request using function annotations.
    """

    async def _iter(self) -> StreamResponse:
        method = getattr(self, self.request.method.lower(), None)
        resp = await method()
        return resp

    def __await__(self) -> Generator[Any, None, StreamResponse]:
        return self._iter().__await__()

    def __init_subclass__(cls, **kwargs):
        cls.allowed_methods = {
            meth_name for meth_name in METH_ALL if hasattr(cls, meth_name.lower())
        }

        for meth_name in METH_ALL:
            if meth_name not in cls.allowed_methods:
                setattr(cls, meth_name.lower(), cls.raise_not_allowed)
            else:
                handler = getattr(cls, meth_name.lower())
                decorated_handler = inject_params(handler, cls.parse_func_signature)
                setattr(cls, meth_name.lower(), decorated_handler)

    async def raise_not_allowed(self):
        raise HTTPMethodNotAllowed(self.request.method, self.allowed_methods)

    @staticmethod
    def parse_func_signature(func: Callable) -> Iterable[AbstractInjector]:
        path_args, body_args, qs_args, header_args, defaults = _parse_func_signature(
            func
        )
        injectors = []

        def default_value(args: dict) -> dict:
            """
            Returns the default values of args.
            """
            return {name: defaults[name] for name in args if name in defaults}

        if path_args:
            injectors.append(MatchInfoGetter(path_args, default_value(path_args)))
        if body_args:
            injectors.append(BodyGetter(body_args, default_value(body_args)))
        if qs_args:
            injectors.append(QueryGetter(qs_args, default_value(qs_args)))
        if header_args:
            injectors.append(HeadersGetter(header_args, default_value(header_args)))
        return injectors


def inject_params(
    handler, parse_func_signature: Callable[[Callable], Iterable[AbstractInjector]]
):
    """
    Decorator to unpack the query string, route path, body and http header in
    the parameters of the web handler regarding annotations.
    """

    injectors = parse_func_signature(handler)

    async def wrapped_handler(self):
        args = []
        kwargs = {}
        for injector in injectors:
            try:
                if iscoroutinefunction(injector.inject):
                    await injector.inject(self.request, args, kwargs)
                else:
                    injector.inject(self.request, args, kwargs)
            except ValidationError as error:
                errors = error.errors()
                for error in errors:
                    error["in"] = injector.context

                return json_response(data=errors, status=400)

        return await handler(self, *args, **kwargs)

    update_wrapper(wrapped_handler, handler)
    return wrapped_handler


def is_pydantic_view(obj) -> bool:
    """
    Return True if obj is a PydanticView subclass else False.
    """
    try:
        return issubclass(obj, PydanticView)
    except TypeError:
        return False
