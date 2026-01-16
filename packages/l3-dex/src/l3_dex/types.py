from __future__ import annotations

from .errors import ValidationError


def ensure_bytes32(value: object, name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise ValidationError(f"{name} must be bytes32")
    if isinstance(value, bytearray):
        value = bytes(value)
    if len(value) != 32:
        raise ValidationError(f"{name} must be 32 bytes")
    return value


def hex_from_bytes(value: bytes) -> str:
    if not isinstance(value, (bytes, bytearray)):
        raise ValidationError("value must be bytes")
    return bytes(value).hex()


def bytes_from_hex(value: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise ValidationError("hex value must be non-empty string")
    try:
        data = bytes.fromhex(value)
    except ValueError as exc:
        raise ValidationError("invalid hex value") from exc
    return data
