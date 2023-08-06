"""A decorator to simplify intercepting an exception and re-raising it as another.

Example:
    You can simplify the following code:
    ```
    def some_function():
        try:
            return some_other_function()
        exception MyException as ex:
            raise MyOtherException(ex)
    ```
    It becomes
    ```
    @reraise_as(MyException, MyOtherException)
    def some_function():
        return some_other_function()
    ````
"""

import asyncio
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generic, Protocol, Type, TypeVar, cast

SE = TypeVar('SE', bound=Exception)
TE = TypeVar('TE', bound=Exception)

Mapper = Callable[[SE, Type[TE]], TE]


F = TypeVar('F', bound=Callable[..., Any])


class Decorator(Protocol):  # pragma: no cover
    def __call__(self, fn: F) -> F:
        ...


class DefaultMapper(Generic[TE]):  # pragma: no-cover-for-integration
    def __call__(self, ex: Exception, target_exc: Type[TE]) -> TE:
        """Default mapper that doesn't attempt to preserve any information. Just instantiates a TargetExClass.

        Args:
            ex (Exception): The source exception.
            target_exc (TE): The target Exception class.

        Returns:
            TE: An instance of the provided tartget Exception class.
        """
        return target_exc()


# Actually performs the catching and remapping, shouldn't be called directly
@contextmanager
def remap_exception(
    source_exc: Type[SE], target_exc: Type[TE], mapper: Mapper[SE, TE],
) -> Any:  # pragma: no-cover-for-integration
    try:
        return cast(Any, (yield))
    except source_exc as ex:  # type: ignore
        ex = cast(SE, ex)
        raise mapper(ex, target_exc)


def reraise_as(  # noqa: WPS212
    source_exc: Type[SE], target_exc: Type[TE], mapper: Mapper[SE, TE] = DefaultMapper[TE](),
) -> Decorator:  # pragma: no-cover-for-integration
    """A decorator function that intercepts raised Exceptions and maps them to a different Exception class.

    Args:
        source_exc (SourceExClass): The Exception class to intercept.
        target_exc (TargetExClass): The Exception class to raise.
        mapper (MapperFn): The mapping function that determines how to build a TargetEx from the SourceEx.

    Returns:
        Decorator
    """

    def reraise_as_decorator(fn: F) -> F:
        # If we're dealing with an async function, we need return an
        # async function
        if asyncio.iscoroutinefunction(fn):
            # Using @wraps ensures we keep the identity of the wrapped function
            @wraps(fn)
            async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
                with remap_exception(source_exc, target_exc, mapper):
                    return await fn(*args, **kwargs)

            return cast(F, async_wrapped)

        # Using @wraps ensures we keep the identity of the wrapped function
        @wraps(fn)
        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            with remap_exception(source_exc, target_exc, mapper):
                return fn(*args, **kwargs)

        return cast(F, sync_wrapped)

    return reraise_as_decorator
