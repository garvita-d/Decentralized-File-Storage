import httpx
from typing import Any, Dict

async def rpc(host: str, port: int, path: str, body: Dict[str, Any], timeout=3.0) -> Dict[str, Any]:
    url = f"http://{host}:{port}{path}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, json=body)
        r.raise_for_status()
        return r.json()
