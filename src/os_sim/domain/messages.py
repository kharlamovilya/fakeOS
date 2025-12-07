from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    """
    A message of kind (device) -> (device) [MSG].
    """
    from_device: int
    to_device: int
    payload: str
