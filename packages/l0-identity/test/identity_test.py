import os
import sys
import unittest

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from identity import (  # noqa: E402
    Context,
    RootSecret,
    Identity,
    IdentityInputError,
    IdentityStateError,
    ERROR_WALLET_AS_IDENTITY,
)


class IdentityDerivationTests(unittest.TestCase):
    def _active_identity(self):
        root = RootSecret.generate()
        context = Context("l0:test")
        identity = Identity.create(root, context)
        identity.activate()
        return identity, context

    def test_same_context_stable(self):
        identity, context = self._active_identity()
        first = identity.derive(context)
        second = identity.derive(context)
        self.assertEqual(first.digest, second.digest)

    def test_different_contexts_diverge(self):
        identity, context = self._active_identity()
        other = Context("l0:other")
        self.assertNotEqual(identity.derive(context).digest, identity.derive(other).digest)

    def test_different_roots_diverge(self):
        context = Context("l0:roots")
        identity_a = Identity.create(RootSecret.generate(), context)
        identity_a.activate()
        identity_b = Identity.create(RootSecret.generate(), context)
        identity_b.activate()
        self.assertNotEqual(identity_a.derive(context).digest, identity_b.derive(context).digest)

    def test_serialize_requires_context(self):
        identity, _ = self._active_identity()
        with self.assertRaises(IdentityInputError):
            identity.serialize(None)

    def test_context_bound_serialization_not_stable(self):
        identity, context = self._active_identity()
        first = identity.serialize(context)
        second = identity.serialize(context)
        self.assertNotEqual(first.blob, second.blob)
        self.assertEqual(first.context_label, context.label)

    def test_destroyed_rejects_use(self):
        identity, context = self._active_identity()
        identity.destroy()
        with self.assertRaises(IdentityStateError):
            identity.derive(context)
        with self.assertRaises(IdentityStateError):
            identity.serialize(context)

    def test_illegal_transitions_fail(self):
        context = Context("l0:state")
        identity = Identity.create(RootSecret.generate(), context)
        with self.assertRaises(IdentityStateError):
            identity.rotate()
        identity.activate()
        with self.assertRaises(IdentityStateError):
            identity.activate()

    def test_rotation_retires_tokens(self):
        identity, context = self._active_identity()
        token = identity.derive(context)
        identity.rotate()
        with self.assertRaises(IdentityStateError):
            identity.assert_token_current(token)

    def test_account_like_input_rejected(self):
        with self.assertRaises(IdentityInputError) as captured:
            Identity.create("0x1234abcd", Context("l0:input"))
        self.assertIn(ERROR_WALLET_AS_IDENTITY, str(captured.exception))

    def test_context_rejects_account_like(self):
        with self.assertRaises(IdentityInputError) as captured:
            Context("did:pkh:eip155:1:0x1234")
        self.assertIn(ERROR_WALLET_AS_IDENTITY, str(captured.exception))


if __name__ == "__main__":
    unittest.main()
