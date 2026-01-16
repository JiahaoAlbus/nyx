from __future__ import annotations

import hashlib
import hmac

from .errors import ValidationError


def sha256(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise ValidationError("sha256 input must be bytes")
    return hashlib.sha256(bytes(data)).digest()


def compare_digest(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


def framed(parts: list[bytes]) -> bytes:
    payload = bytearray()
    for part in parts:
        if not isinstance(part, (bytes, bytearray)):
            raise ValidationError("framed parts must be bytes")
        part_bytes = bytes(part)
        payload.extend(len(part_bytes).to_bytes(4, "big"))
        payload.extend(part_bytes)
    return bytes(payload)
