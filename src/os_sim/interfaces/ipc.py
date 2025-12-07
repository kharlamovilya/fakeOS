from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List
from os_sim.domain.messages import Message


class IMessageBus(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        """Sends message to a bus."""
        ...

    @abstractmethod
    def poll_for_device(self, device_id: int) -> List[Message]:
        """Pull all messages addressed to a device and remove them from the bus."""
        ...
