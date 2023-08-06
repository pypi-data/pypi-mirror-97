# coding: utf-8
# Copyright (c) Qotto, 2018

from .base import BaseEvent

from typing import Any, Dict

__all__ = [
    'GenericEvent'
]


class GenericEvent(BaseEvent):
    """
    Allows to create generic named events.

    >>> evt = GenericEvent(name='qotto.payment.command.CreatePayment', data={'quantity': '1L'})
    >>> evt.name
    'qotto.payment.command.CreatePayment'
    >>> evt.data['quantity']
    '1L'
    """

    def __init__(self, name: str, data: Dict[str, Any]) -> None:
        super().__init__(name=name, data=data)

    @classmethod
    def from_data(cls, event_name: str, event_data: Dict[str, Any]):
        event = cls(name=event_name, data=event_data)
        return event
