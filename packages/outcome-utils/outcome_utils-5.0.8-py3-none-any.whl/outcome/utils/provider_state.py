"""Helpers to manipulate provider states headers."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class ProviderState(BaseModel):
    method: str
    path: str
    state: str

    @classmethod
    def create(cls, method: str, path: str, state: str) -> ProviderState:
        return ProviderState(method=method, path=path, state=state)


class ProviderStates(BaseModel):
    __root__: List[ProviderState]


class ProviderStateMap:
    states: List[ProviderState]

    def __init__(self, states: Optional[List[ProviderState]] = None):
        self.states = []
        if states:
            self.add_states(states)

    def add_state(self, state: ProviderState) -> None:
        self.states.append(state)

    def add_states(self, states: List[ProviderState]) -> None:
        for state in states:
            self.add_state(state)

    def as_headers(self, key: str = 'pact-provider-state-map') -> Dict[str, str]:
        return {key: ProviderStates(__root__=self.states).json()}
