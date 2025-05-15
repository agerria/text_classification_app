
import hashlib
from typing import Any

def hash_json(data: Any) -> str:
    def hasher(value: Any):
        if type(value) is list:
            for item in value:
                hasher(item)
            return

        if type(value) is dict:
            for item_key in sorted(value.keys()):
                hash.update(item_key.encode())
                hasher(value[item_key])
            return

        if type(value) is not str:
            value = str(value)

        hash.update(value.encode())
        
    hash = hashlib.sha1()
    hasher(data)
    return hash.hexdigest()