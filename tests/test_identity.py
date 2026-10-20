"""One independently retained identity for implementer and reviewer."""

from unittest.mock import patch

from agent_guides_cli import preparation, task_identity
from agent_guides_cli.integrity import GuidanceError, canonical, digest
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

    def test_case_variants_of_generated_names_are_reserved_for_all_evidence(self):
        names = (".GUIDANCE/task.json", ".Guidance/nested/task.json", "Guidance.Lock.Json")
        for name in names:
            with self.subTest(name=name):
                with self.assertRaisesRegex(GuidanceError, "independently of generated storage"):
                    task_identity.retain(self.project / name, self.value, self.project)
                for role in ("policies", "overlays"):
                    with self.assertRaisesRegex(GuidanceError, "generated files cannot"):
                        task_identity.capture(self.project, self.result["selection"],
                                              fixtures=self.fixtures, **{role: [name]})

    def test_filesystem_project_alias_cannot_hide_generated_storage(self):
        alias = self.project.with_name(self.project.name.upper())
        if not alias.exists() or not alias.samefile(self.project):
            self.skipTest("requires case-insensitive project alias")
        output = alias / ".GUIDANCE/review-task.json"
        with self.assertRaisesRegex(GuidanceError, "independently of generated storage"):
            task_identity.retain(output, self.value, self.project)
        self.assertFalse((self.project / ".guidance/review-task.json").exists())

    def test_evidence_symlink_rejection_preserves_unowned_bytes(self):
        evidence = self.root / "evidence.json"
        evidence.write_bytes(b"host-owned evidence\n")
        alias = self.root / "alias.json"
        alias.symlink_to(evidence)
        with self.assertRaisesRegex(GuidanceError, "symlink rejected"):
            task_identity.retain(alias, self.value, self.project)
        self.assertEqual(evidence.read_bytes(), b"host-owned evidence\n")
