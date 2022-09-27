import json
import uuid
from typing import Any


class UUIDEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, uuid.UUID):
            return str(o)

        return super().default(o)


def uuid_aware_json_encode(obj: Any) -> bytes:
    result = json.dumps(obj, sort_keys=True, indent=None, separators=(",", ":"), ensure_ascii=False, cls=UUIDEncoder)
    return result.encode("utf-8")
