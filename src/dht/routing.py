from dataclasses import dataclass, field
from typing import List
from .id import xor_distance

@dataclass
class Contact:
    id_hex: str
    host: str
    port: int
    last_seen: float = field(default=0.0)

class RoutingTable:
    def __init__(self, self_id: bytes, k: int = 20):
        self.k = k
        self.self_id = self_id
        self._contacts: List[Contact] = []

    def add(self, c: Contact):
        key = c.id_hex
        self._contacts = [x for x in self._contacts if x.id_hex != key]
        self._contacts.append(c)
        self._contacts.sort(key=lambda x: xor_distance(bytes.fromhex(x.id_hex), self.self_id))
        self._contacts = self._contacts[: self.k * 8]

    def closest(self, target_hex: str, count: int = 20) -> List[Contact]:
        target = bytes.fromhex(target_hex)
        return sorted(self._contacts, key=lambda x: xor_distance(bytes.fromhex(x.id_hex), target))[:count]

    def all(self) -> List[Contact]:
        return list(self._contacts)
