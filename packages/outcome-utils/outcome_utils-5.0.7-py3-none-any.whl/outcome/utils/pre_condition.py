"""Pre-condition check decorator."""

from asyncio import iscoroutinefunction
from typing import Any, Callable, Coroutine, Protocol, TypeVar, Union, cast

from asgiref.sync import async_to_sync
from makefun import wraps

Predicate = Union[Callable[..., bool], Callable[..., Coroutine[Any, Any, bool]]]

F = TypeVar('F', bound=Callable[..., Any])


class PreconditionDecorator(Protocol):  # pragma: no cover
    def __call__(self, fn: F) -> F:
        ...


def pre_condition(pre_condition_fn: Predicate) -> PreconditionDecorator:  # noqa: WPS231,WPS212,WPS238
    """Executes a pre-condition function over the provided arguments before calling the decorated function.

    Automatically handles async pre-condition functions and wrapped functions.

    Exceptions raised in the pre-condition will pass through the decorator.
    If the pre-condition returns False, an UnmetPreconditionException will be raised.

    Args:
        pre_condition_fn (Predicate): The pre-condition function.

    Returns:
        PreconditionDecorator: The wrapped function
    """

    def pre_condition_decorator(fn: F) -> F:  # noqa: WPS231,WPS212,WPS238
        if iscoroutinefunction(fn) and iscoroutinefunction(pre_condition_fn):

            # iscoroutinefunction doesn't work as a type guard
            async_precondition = cast(Callable[..., Coroutine[Any, Any, bool]], pre_condition_fn)

            @wraps(fn)  # type: ignore - The type markings are incorrect
            async def async_fn_with_async_precondition(*args: Any, **kwargs: Any):
                if not await async_precondition(*args, **kwargs):
                    raise UnmetPreconditionException
                return await fn(*args, **kwargs)

            return cast(F, async_fn_with_async_precondition)

        elif iscoroutinefunction(fn):

            @wraps(fn)  # type: ignore - The type markings are incorrect
            async def async_fn_with_sync_precondition(*args: Any, **kwargs: Any):  # noqa: WPS440
                if not pre_condition_fn(*args, **kwargs):
                    raise UnmetPreconditionException
                return await fn(*args, **kwargs)

            return cast(F, async_fn_with_sync_precondition)

        elif iscoroutinefunction(pre_condition_fn):

            @wraps(fn)  # type: ignore - The type markings are incorrect
            def sync_fn_with_async_precondition(*args: Any, **kwargs: Any):  # noqa: WPS440
                # Use async_to_sync to call an async from a sync: https://www.aeracode.org/2018/02/19/python-async-simplified/
                if not async_to_sync(pre_condition_fn)(*args, **kwargs):
                    raise UnmetPreconditionException
                return fn(*args, **kwargs)

            return cast(F, sync_fn_with_async_precondition)

        @wraps(fn)  # type: ignore - The type markings are incorrect
        def sync_fn_with_sync_precondition(*args: Any, **kwargs: Any):  # noqa: WPS440
            if not pre_condition_fn(*args, **kwargs):
                raise UnmetPreconditionException
            return fn(*args, **kwargs)

        return cast(F, sync_fn_with_sync_precondition)

    return pre_condition_decorator


class UnmetPreconditionException(Exception):
    ...
