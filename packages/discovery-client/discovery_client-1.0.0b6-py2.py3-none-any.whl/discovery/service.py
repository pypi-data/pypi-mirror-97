import json
import socket
import uuid
from functools import singledispatch
from typing import Optional


class Service:
    def __init__(
        self,
        name: str,
        port: int,
        # dc: str = "",
        service_id: Optional[str] = None,
        address: Optional[str] = None,
        tags: Optional[list] = None,
        meta: Optional[dict] = None,
        # namespace: str = "default",
        check: Optional[str] = None,
    ):
        self.name = name
        self.port = port
        self.service_id = service_id or f"{name}-{uuid.uuid4().hex}"
        self.address = f"{socket.gethostbyname(socket.gethostname())}"
        self.check = check
        self.meta = meta or {}
        self.tags = tags or []
        self._tags_is_valid(self.tags)
        self._meta_is_valid(self.meta)

    def _tags_is_valid(self, tags: Optional[list]) -> bool:
        if not isinstance(tags, list):
            raise ValueError("tags must be list")
        return True

    def _meta_is_valid(self, meta: Optional[dict]) -> bool:
        if not isinstance(meta, dict):
            raise ValueError("meta must be dict")
        return True

    def __str__(self):
        data = {
            "name": self.name,
            "id": self.service_id,
            "address": self.address,
            "port": self.port,
            "tags": self.tags,
            "meta": self.meta,
        }
        if self.check:
            data.update(register_check(self.check))
        return json.dumps(data)

    def __repr__(self):
        return f"Service({json.loads(str(self))})"


@singledispatch
def register_check(check) -> dict:
    response = {"check": json.loads(check)}
    return response


@register_check.register(list)
def _(check) -> dict:
    response: dict = {"checks": []}
    for chk in check:
        response["checks"].append(json.loads(chk))
    return response
