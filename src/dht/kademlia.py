import asyncio
from typing import Any, List, Optional
from .routing import Contact
from .client import rpc

async def find_value(start: List[Contact], key_hex: str, alpha: int = 3) -> Optional[Any]:
    seen = set()
    shortlist = list(start)

    while shortlist:
        batch, shortlist = shortlist[:alpha], shortlist[alpha:]
        tasks = [rpc(c.host, c.port, "/find_value", {"key": key_hex}) for c in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        next_contacts: List[Contact] = []
        for res in results:
            if isinstance(res, Exception):
                continue
            if res.get("value") is not None:
                return res["value"]
            for cc in res.get("contacts", []):
                k = cc["id"]
                if k not in seen:
                    seen.add(k)
                    next_contacts.append(Contact(id_hex=cc["id"], host=cc["host"], port=cc["port"]))
        shortlist.extend(next_contacts)
    return None

async def store_value(contacts: List[Contact], key_hex: str, value: Any, alpha: int = 3) -> None:
    batch = contacts[:alpha]
    tasks = [rpc(c.host, c.port, "/store", {"key": key_hex, "value": value}) for c in batch]
    await asyncio.gather(*tasks, return_exceptions=True)
