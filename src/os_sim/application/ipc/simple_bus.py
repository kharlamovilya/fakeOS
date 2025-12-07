from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from os_sim.domain.messages import Message
from os_sim.interfaces.ipc import IMessageBus
from os_sim.interfaces.logging import ILogger


@dataclass(slots=True)
class SimpleMessageBus(IMessageBus):
    logger: ILogger | None = None
    _pending: List[Message] = field(default_factory=list)

    def send(self, message: Message) -> None:
        self._pending.append(message)
        if self.logger:
            self.logger.log(
                f"[IPC] {message.from_device} → {message.to_device}: {message.payload}"
            )

    def poll_for_device(self, device_id: int) -> List[Message]:
        to_deliver: List[Message] = [
            m for m in self._pending if m.to_device == device_id
        ]
        if not to_deliver:
            return []

        self._pending = [m for m in self._pending if m.to_device != device_id]

        if self.logger and to_deliver:
            self.logger.log(
                f"[IPC] Delivered {len(to_deliver)} messages to device {device_id}"
            )

        return to_deliver
