from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import hmac
import re
import secrets

DOMAIN_TAG = b"nyx:l0-identity:v1"
ERROR_WALLET_AS_IDENTITY = "NYX_CONFORMANCE_WALLET_AS_IDENTITY"
ERROR_INVALID_INPUT = "NYX_IDENTITY_INVALID_INPUT"

_ACCOUNT_PATTERNS = (
    re.compile(r"^0x[0-9a-fA-F]{8,}$"),
    re.compile(r"^did:pkh:", re.IGNORECASE),
    re.compile(r"^eip155:", re.IGNORECASE),
)


class IdentityInputError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


class IdentityStateError(RuntimeError):
    pass


def _is_account_like(value: str) -> bool:
    return any(pattern.search(value) for pattern in _ACCOUNT_PATTERNS)


def _reject_account_like(value: str) -> None:
    if _is_account_like(value):
        raise IdentityInputError(
            ERROR_WALLET_AS_IDENTITY,
            "account-like identifiers are not permitted",
        )


def _require_root_secret(value: object) -> "RootSecret":
    if isinstance(value, str):
        _reject_account_like(value)
        raise IdentityInputError(ERROR_INVALID_INPUT, "root secret must be a RootSecret")
    if not isinstance(value, RootSecret):
        raise IdentityInputError(ERROR_INVALID_INPUT, "root secret must be a RootSecret")
    return value


def _require_context(value: object) -> "Context":
    if isinstance(value, str):
        _reject_account_like(value)
        raise IdentityInputError(ERROR_INVALID_INPUT, "context must be a Context")
    if not isinstance(value, Context):
        raise IdentityInputError(ERROR_INVALID_INPUT, "context must be a Context")
    return value


@dataclass(frozen=True)
class Context:
    label: str

    def __post_init__(self) -> None:
        if not isinstance(self.label, str):
            raise IdentityInputError(ERROR_INVALID_INPUT, "context label must be a string")
        if not self.label.strip():
            raise IdentityInputError(ERROR_INVALID_INPUT, "context label is required")
        _reject_account_like(self.label)

    def tag_bytes(self) -> bytes:
        return self.label.encode("utf-8")


class RootSecret:
    __slots__ = ("_material",)
    _SENTINEL = object()

    def __init__(self, material: bytes, _internal: object = _SENTINEL) -> None:
        if _internal is not RootSecret._SENTINEL:
            raise IdentityInputError(
                ERROR_INVALID_INPUT,
                "root secret must be generated locally",
            )
        if not isinstance(material, (bytes, bytearray)):
            raise IdentityInputError(ERROR_INVALID_INPUT, "root secret must be bytes")
        if len(material) < 32:
            raise IdentityInputError(ERROR_INVALID_INPUT, "root secret entropy is too short")
        self._material = bytes(material)

    @classmethod
    def generate(cls) -> "RootSecret":
        return cls(secrets.token_bytes(32), _internal=cls._SENTINEL)

    def redacted(self) -> str:
        return "<redacted>"

    def export(self) -> bytes:
        raise IdentityInputError(ERROR_INVALID_INPUT, "root secret export is prohibited")

    def __bytes__(self) -> bytes:
        raise IdentityInputError(ERROR_INVALID_INPUT, "root secret export is prohibited")

    def __repr__(self) -> str:
        return "<RootSecret redacted>"

    def _material_bytes(self) -> bytes:
        return self._material


@dataclass(frozen=True)
class DerivedToken:
    digest: bytes
    context_label: str
    generation: int


@dataclass(frozen=True)
class SerializedIdentity:
    context_label: str
    nonce: bytes
    blob: bytes


def _derive_digest(
    root_secret: RootSecret,
    context: Context,
    generation: int,
    nonce: bytes | None = None,
) -> bytes:
    base = b"|".join(
        [
            DOMAIN_TAG,
            str(generation).encode("ascii"),
            context.tag_bytes(),
        ]
    )
    if nonce is not None:
        base = base + b"|" + nonce
    return hmac.new(root_secret._material_bytes(), base, hashlib.sha256).digest()


class IdentityState(Enum):
    CREATED = "created"
    ACTIVE = "active"
    ROTATED = "rotated"
    DESTROYED = "destroyed"


class Identity:
    __slots__ = ("_root_secret", "_state", "_generation")

    def __init__(self, root_secret: RootSecret, state: IdentityState, generation: int) -> None:
        self._root_secret = root_secret
        self._state = state
        self._generation = generation

    @classmethod
    def create(cls, root_secret: RootSecret, context: Context) -> "Identity":
        _require_root_secret(root_secret)
        _require_context(context)
        return cls(root_secret, IdentityState.CREATED, 0)

    @property
    def state(self) -> IdentityState:
        return self._state

    @property
    def generation(self) -> int:
        return self._generation

    def activate(self) -> None:
        self._require_state(IdentityState.CREATED)
        self._state = IdentityState.ACTIVE

    def rotate(self) -> None:
        self._require_state(IdentityState.ACTIVE)
        self._root_secret = RootSecret.generate()
        self._generation += 1
        self._state = IdentityState.ROTATED

    def destroy(self) -> None:
        if self._state == IdentityState.DESTROYED:
            raise IdentityStateError("identity already destroyed")
        self._state = IdentityState.DESTROYED

    def derive(self, context: Context) -> DerivedToken:
        self._ensure_usable()
        context = _require_context(context)
        digest = _derive_digest(self._root_secret, context, self._generation)
        return DerivedToken(digest=digest, context_label=context.label, generation=self._generation)

    def serialize(self, context: Context) -> SerializedIdentity:
        self._ensure_usable()
        context = _require_context(context)
        nonce = secrets.token_bytes(16)
        blob = _derive_digest(self._root_secret, context, self._generation, nonce=nonce)
        return SerializedIdentity(context_label=context.label, nonce=nonce, blob=blob)

    def assert_token_current(self, token: DerivedToken) -> None:
        if self._state == IdentityState.DESTROYED:
            raise IdentityStateError("identity is destroyed")
        if token.generation != self._generation:
            raise IdentityStateError("token generation is not current")

    def _ensure_usable(self) -> None:
        if self._state == IdentityState.CREATED:
            raise IdentityStateError("identity is not active")
        if self._state == IdentityState.DESTROYED:
            raise IdentityStateError("identity is destroyed")

    def _require_state(self, expected: IdentityState) -> None:
        if self._state != expected:
            raise IdentityStateError(
                f"illegal state transition: {self._state.value} -> {expected.value}"
            )
