# coding: utf-8
# Copyright (c) Qotto, 2018

from ..event.base import BaseEvent

from typing import Any, Type

__all__ = [
    'BaseEventSerializer',
]


class BaseEventSerializer:

    def __init__(self, settings: object) -> None:
        pass

    def encode(self, event: BaseEvent) -> Any:
        raise NotImplementedError

    def decode(self, encoded_event: Any) -> BaseEvent:
        raise NotImplementedError

    def register_event_class(self, event_class: Type[BaseEvent], event_name: str = None) -> None:
        raise NotImplementedError
