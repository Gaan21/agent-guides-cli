"""One independently retained identity for implementer and reviewer."""

from unittest.mock import patch

from agent_guides import preparation, task_identity
from agent_guides.integrity import GuidanceError, canonical, digest
from fixtures import GitFixture


class TaskIdentityTests(GitFixture):
    def setUp(self):
        super().setUp()
        (self.project / "AGENTS.md").write_bytes(b"local policy\n")
        (self.project / "overlay.md").write_bytes(b"local exception\n")
        self.result = self.prepare()
        self.value = task_identity.capture(self.project, self.result["selection"],
                                           overlays=["overlay.md"], fixtures=self.fixtures)
        self.raw = canonical(self.value)
        self.expected = digest(self.raw)

    def test_shared_roles_and_root_portability(self):
        evidence = self.root / "retained.json"
        self.assertEqual(task_identity.retain(evidence, self.value, self.project), self.expected)
        with self.assertRaises(FileExistsError):
            task_identity.retain(evidence, self.value, self.project)
        joined = task_identity.join(self.project, evidence.read_bytes(), self.expected, fixtures=self.fixtures)
        self.assertEqual(joined["selection"], self.result["selection"])
        self.assertNotIn(str(self.root), self.raw.decode())
        second = self.root / "second"
        second.mkdir()
        preparation.restore(second, self.read_lock(), self.result["selection"], self.cache, fixtures=self.fixtures)
        for name in ("AGENTS.md", "overlay.md"):
            (second / name).write_bytes((self.project / name).read_bytes())
        self.assertEqual(task_identity.join(second, self.raw, self.expected, fixtures=self.fixtures), joined)

    def test_policy_overlay_new_native_policy_and_engine_drift(self):
        for name in ("AGENTS.md", "overlay.md", "CLAUDE.md"):
            path = self.project / name
            before = path.read_bytes() if path.exists() else None
            path.write_bytes(b"changed\n")
            with self.subTest(name=name), self.assertRaises(GuidanceError):
                task_identity.join(self.project, self.raw, self.expected, fixtures=self.fixtures)
            if before is None:
                path.unlink()
            else:
                path.write_bytes(before)
        with patch.object(preparation, "engine_identity", return_value={"version": "changed", "digest": "0" * 64}):
            with self.assertRaisesRegex(GuidanceError, "engine identity mismatch"):
                task_identity.join(self.project, self.raw, self.expected, fixtures=self.fixtures)

    def test_expected_task_evidence_and_generated_storage_rejection(self):
        with self.assertRaisesRegex(GuidanceError, "expected task identity mismatch"):
            task_identity.join(self.project, self.raw, "0" * 64, fixtures=self.fixtures)
        for name in (".guidance/expected.json", "guidance.lock.json"):
            with self.subTest(name=name), self.assertRaises(GuidanceError):
                task_identity.retain(self.project / name, self.value, self.project)
        with self.assertRaises(GuidanceError):
            task_identity.capture(self.project, self.result["selection"], policies=["guidance.lock.json"], fixtures=self.fixtures)
