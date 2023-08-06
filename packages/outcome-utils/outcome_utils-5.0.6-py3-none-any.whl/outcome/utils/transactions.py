"""Transactions handler.

Usage examples:

- Default usage auto-applies all added operations.
```
with transaction() as ops:
    op = Operation(apply_fn=your_apply_fn, rollback_fn=your_rollback_fn)
    ops.add(op)
```

- We can disable auto-apply if necessary. In this case, the context manager
will check if some operations weren't applied at the end of the transaction.
```
op = None
with transaction(auto_apply=False) as ops:
    op = Operation(apply_fn=your_apply_fn, rollback_fn=your_rollback_fn)
    ops.add(create_user)
    op.apply()
```

"""

from __future__ import annotations

import abc
from contextlib import contextmanager
from contextvars import ContextVar
from enum import Enum
from types import TracebackType
from typing import Callable, Generic, Iterator, List, Optional, Type, TypeVar

txns = ContextVar('txns', default=[])


def reset_context():  # pragma: no cover
    # This method exposes a way to reset the ContextVar.
    txns.set([])


E = TypeVar('E', bound=Exception)


class TransactionManager:
    @property
    def transactions(self) -> List[Transaction]:
        # We store transactions of a hierarchie in a ContextVar to make sure
        # there are no conflicts in an async context.
        return txns.get()

    @property
    def current_txn(self) -> Optional[Transaction]:
        if self.transactions:
            # Return the current transaction.
            return self.transactions[-1]
        return None

    @current_txn.setter
    def current_txn(self, value: Transaction):
        self.transactions.append(value)

    def __enter__(self) -> Transaction:
        parent_transaction = self.current_txn
        self.current_txn = Transaction()
        if parent_transaction is not None:
            # We wrap the transaction to give it the same interface as a resource, and link it
            # to the parent transaction. That way, the parent transaction will be able to abort its
            # child transactions if any of them fails.
            parent_transaction.join(TransactionResourceManager(self.current_txn))
        return self.current_txn

    def __exit__(self, exc_type: Type[E], exc_value: E, traceback: TracebackType):
        assert self.current_txn
        if exc_value is None:
            self.current_txn.commit()
        else:
            self.current_txn.abort()
        self.transactions.pop()


class Status(Enum):
    active = 'Active'
    committed = 'Committed'
    commitfailed = 'Commit failed'


class Transaction:
    _resources: List[ResourceManager]

    def __init__(self):
        self.status = Status.active
        self._resources = []

    def join(self, resource: ResourceManager) -> None:
        assert self.status is Status.active  # noqa: S101
        self._resources.append(resource)

    def commit(self) -> None:
        assert self.status is Status.active  # noqa: S101

        try:
            self._commit_resources()
            self.status = Status.committed
        except Exception as e:  # pragma: no cover
            self.status = Status.commitfailed
            raise e

    def abort(self) -> None:
        exceptions: List[Exception] = []
        for rm in reversed(self._resources):
            try:
                rm.abort()
            except Exception as e:  # pragma: no cover
                exceptions.append(e)
        if exceptions:  # pragma: no cover
            raise Exception(exceptions)

    def _commit_resources(self) -> None:
        try:
            for rm in self._resources:
                rm.commit()
        except Exception:  # pragma: no cover
            # If an error occurs committing a transaction, we try
            # to revert the changes in each of the resource managers.
            for rm in reversed(self._resources):  # noqa: WPS440
                rm.abort()  # noqa: WPS441


class ResourceManager(abc.ABC):
    def __init__(self, txn: Transaction):
        self.txn = txn

    @abc.abstractmethod
    def abort(self) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    def commit(self) -> None:  # pragma: no cover
        ...


@contextmanager
def transaction(auto_apply: bool = True) -> Iterator[OperationManager]:
    manager = TransactionManager()

    with manager as txn:
        ops = OperationManager(txn)
        txn.join(ops)

        yield ops

        if auto_apply:
            ops.apply()
        else:
            ops.ensure_applied()


class OperationState(Enum):
    pending = 'pending'
    applied = 'applied'
    errored = 'errored'
    reset = 'reset'


class InvalidState(Exception):
    ...


class OperationNotApplied(Exception):
    ...


T = TypeVar('T', covariant=True)

OperationApplyFn = Callable[[], Optional[T]]
OperationRollbackFn = Callable[[Optional[T]], None]


class Operation(Generic[T]):
    result: Optional[T]
    apply_fn: OperationApplyFn[T]
    rollback_fn: OperationRollbackFn[T]

    def __init__(self, apply_fn: OperationApplyFn[T], rollback_fn: OperationRollbackFn[T]):
        self.apply_fn = apply_fn
        self.rollback_fn = rollback_fn
        self.state = OperationState.pending
        self.result = None

    def apply(self) -> None:
        if self.state != OperationState.pending:
            raise InvalidState

        try:
            self.result = self.apply_fn()
            self.state = OperationState.applied
        except Exception as ex:
            self.state = OperationState.errored
            raise Exception('Failed to apply operation') from ex

    def rollback(self) -> None:
        if self.state != OperationState.applied:
            raise InvalidState

        self.rollback_fn(self.result)
        self.state = OperationState.reset


class OperationManager(ResourceManager):  # noqa: WPS214 - too many methods
    operations: List[Operation[object]]

    def __init__(self, txn: Transaction):
        super().__init__(txn)
        self.operations = []

    def add(self, operation: Operation[object]) -> None:
        self.operations.append(operation)

    def apply(self) -> None:
        for op in self.operations:
            op.apply()

    def abort(self) -> None:
        for op in reversed(self.operations):
            if op.state == OperationState.applied:
                op.rollback()

    def ensure_applied(self) -> None:
        for op in self.operations:
            if op.state != OperationState.applied:
                raise OperationNotApplied(op.state)

    def commit(self) -> None:
        pass


class TransactionResourceManager(ResourceManager):
    def abort(self) -> None:
        self.txn.abort()

    def commit(self) -> None:
        pass
