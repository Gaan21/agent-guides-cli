"""Fault injection at every native write/publication stage and safe recovery."""

import os
from unittest.mock import patch

from agent_guides import lifecycle, native, transactions as tx
from agent_guides.integrity import GuidanceError, canonical, digest
from fixtures import GitFixture

PROJECT_SURFACES = (native.ENTRY, native.CLAUDE, native.CONFIG, native.STATE, "guidance.lock.json")

class TransactionTests(GitFixture):
    def setUp(self):
        super().setUp()
        environment = patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": ""})
        environment.start()
        self.addCleanup(environment.stop)

    def install_at(self, project):
        return lifecycle.install(project, self.request, ["claude", "opencode"], self.cache,
                                 fixtures=self.fixtures)

    def fault(self, phase):
        def checkpoint(actual):
            if actual == phase:
                raise OSError("simulated crash: " + phase)
        return patch.object(tx, "checkpoint", side_effect=checkpoint)

    def test_install_interrupted_at_every_stage_then_rollback_retry_or_finish_commit(self):
        baseline = self.install_at(self.project)
        expected = baseline["selection"]
        for index, phase in enumerate(["journal", *("write:" + n for n in PROJECT_SURFACES),
                                      "committed", "archived:committed"]):
            with self.subTest(phase=phase):
                project = self.root / f"fault-{index}"
                project.mkdir()
                with self.fault(phase), self.assertRaisesRegex(OSError, "simulated crash"):
                    self.install_at(project)
                with self.assertRaises(GuidanceError):
                    lifecycle.verify(project, expected, fixtures=self.fixtures)
                self.assertTrue(lifecycle.recover(project)["recovered"])
                self.assertFalse(lifecycle.recover(project)["recovered"])
                if phase not in ("committed", "archived:committed"):
                    for name in tx.SURFACES:
                        self.assertIsNone(tx.read(project, name), name)
                    retried = self.install_at(project)
                    self.assertEqual(retried["selection"], expected)
                self.assertEqual(lifecycle.verify(project, expected, fixtures=self.fixtures)["status"], "installed")

    def test_update_and_remove_faults_restore_previous_bytes(self):
        first = self.install_at(self.project)
        old_lock = (self.project / "guidance.lock.json").read_bytes()
        self.write("alpha", "one/detail/topic.md", b"Changed content.\n")
        self.commit("alpha")
        # Updating changes entry and ownership, then publishes the portable lock.
        for index, phase in enumerate(["journal", "write:" + native.ENTRY,
                                      "write:" + native.STATE, "write:guidance.lock.json"]):
            project = self.root / f"update-{index}"
            project.mkdir()
            lifecycle.restore(project, old_lock, first["selection"], self.cache, fixtures=self.fixtures)
            before = {n: tx.read(project, n) for n in tx.SURFACES}
            with self.subTest(operation="update", phase=phase), self.fault(phase), self.assertRaises(OSError):
                lifecycle.update(project, first["selection"], self.cache, fixtures=self.fixtures)
            lifecycle.recover(project)
            self.assertEqual({n: tx.read(project, n) for n in tx.SURFACES}, before)
            lifecycle.verify(project, first["selection"], fixtures=self.fixtures)
        for index, phase in enumerate(["journal", *("write:" + n for n in PROJECT_SURFACES if n != "guidance.lock.json")]):
            project = self.root / f"remove-{index}"
            project.mkdir()
            lifecycle.restore(project, old_lock, first["selection"], self.cache, fixtures=self.fixtures)
            before = {n: tx.read(project, n) for n in tx.SURFACES}
            with self.subTest(operation="remove", phase=phase), self.fault(phase), self.assertRaises(OSError):
                lifecycle.remove(project, first["selection"], fixtures=self.fixtures)
            lifecycle.recover(project)
            self.assertEqual({n: tx.read(project, n) for n in tx.SURFACES}, before)

    def test_unknown_user_edits_stop_recovery_before_any_rollback(self):
        with self.fault("write:" + native.CONFIG), self.assertRaises(OSError):
            self.install_at(self.project)
        path = self.project / "CLAUDE.md"
        path.write_bytes(path.read_bytes() + b"User changed this during interruption.\n")
        before = {n: tx.read(self.project, n) for n in tx.SURFACES}
        with self.assertRaisesRegex(GuidanceError, "recovery conflict"):
            lifecycle.recover(self.project)
        self.assertEqual({n: tx.read(self.project, n) for n in tx.SURFACES}, before)
        self.assertTrue((self.project / tx.JOURNAL).exists())

    def test_write_failures_before_and_after_each_native_replacement_are_recoverable(self):
        original = tx.save_bytes
        for index, name in enumerate(PROJECT_SURFACES):
            for when in ("before", "after"):
                project = self.root / f"replacement-{index}-{when}"
                project.mkdir()
                target = project / name
                def fail(path, raw, **kwargs):
                    if path == target and when == "before":
                        raise OSError("before replacement")
                    original(path, raw, **kwargs)
                    if path == target and when == "after":
                        raise OSError("after replacement")
                with self.subTest(path=name, when=when), patch.object(tx, "save_bytes", side_effect=fail):
                    with self.assertRaises(OSError):
                        self.install_at(project)
                lifecycle.recover(project)
                self.assertTrue(all(tx.read(project, name) is None for name in tx.SURFACES))

    def test_recovery_itself_can_be_interrupted_and_retried(self):
        with self.fault("write:" + native.CONFIG), self.assertRaises(OSError):
            self.install_at(self.project)
        with self.fault("rollback:" + native.CONFIG), self.assertRaises(OSError):
            lifecycle.recover(self.project)
        self.assertTrue((self.project / tx.JOURNAL).exists())
        self.assertTrue(lifecycle.recover(self.project)["recovered"])
        self.assertTrue(all(tx.read(self.project, name) is None for name in tx.SURFACES))
        self.assertTrue(list((self.project / ".guidance/transactions").glob("*.json")))

    def test_recovery_never_widens_concurrently_tightened_user_permissions(self):
        (self.project / ".guidance").mkdir()
        path = self.project / native.CLAUDE
        path.write_bytes(b"Original local authority.\n")
        path.chmod(0o640)
        with self.fault("write:" + native.CLAUDE), self.assertRaises(OSError):
            tx.apply(self.project, [(native.CLAUDE, path.read_bytes(), b"Changed policy.\n"),
                                    ("guidance.lock.json", None, None)], lambda: None)
        path.chmod(0o600)
        with self.assertRaisesRegex(GuidanceError, "recovery conflict"):
            lifecycle.recover(self.project)
        self.assertEqual(path.read_bytes(), b"Changed policy.\n")
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertTrue((self.project / tx.JOURNAL).exists())

    def test_application_rechecks_modes_captured_before_preparation(self):
        (self.project / ".guidance").mkdir()
        path = self.project / native.CLAUDE
        path.write_bytes(b"Original policy.\n")
        path.chmod(0o640)
        before = tx.Preimages(self.project, [native.CLAUDE, "guidance.lock.json"])
        after = dict(before, **{native.CLAUDE: b"Changed policy.\n"})
        path.chmod(0o600)
        with self.assertRaisesRegex(GuidanceError, "preimage changed"):
            tx.apply(self.project, before.plan(after), lambda: None)
        self.assertEqual(path.read_bytes(), b"Original policy.\n")
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertFalse((self.project / tx.JOURNAL).exists())

    def test_private_policy_preimages_are_retained_owner_only(self):
        (self.project / ".guidance").mkdir()
        path = self.project / native.CLAUDE
        path.write_bytes(b"Private original policy.\n")
        path.chmod(0o600)
        tx.apply(self.project, [(native.CLAUDE, path.read_bytes(), b"Private changed policy.\n"),
                                ("guidance.lock.json", None, None)], lambda: None)
        archives = list((self.project / ".guidance/transactions").glob("*.json"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].stat().st_mode & 0o7777, 0o400)
        self.assertEqual(path.stat().st_mode & 0o7777, 0o600)

    def test_unsafe_existing_archive_permissions_stop_finalization_without_repair(self):
        with self.fault("archived:committed"), self.assertRaises(OSError):
            self.install_at(self.project)
        archive, = (self.project / ".guidance/transactions").glob("*.json")
        archive.chmod(0o444)
        raw = archive.read_bytes()
        with self.assertRaisesRegex(GuidanceError, "unsafe permissions"):
            lifecycle.recover(self.project)
        self.assertEqual(archive.read_bytes(), raw)
        self.assertEqual(archive.stat().st_mode & 0o7777, 0o444)
        self.assertTrue((self.project / tx.JOURNAL).exists())

    def test_preimage_edit_between_preparation_and_apply_is_not_overwritten(self):
        original = lifecycle.retain_lock
        def concurrent_edit(project, raw):
            result = original(project, raw)
            (project / "CLAUDE.md").write_bytes(b"Concurrent user policy.\n")
            return result
        with patch.object(lifecycle, "retain_lock", side_effect=concurrent_edit):
            with self.assertRaisesRegex(GuidanceError, "preimage changed"):
                self.install_at(self.project)
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), b"Concurrent user policy.\n")
        self.assertFalse((self.project / tx.JOURNAL).exists())
        self.assertFalse((self.project / "guidance.lock.json").exists())

    def test_journal_rejects_path_traversal_and_duplicate_targets(self):
        directory = self.project / ".guidance"
        directory.mkdir()
        change = {"path": "../outside", "before": None, "after": tx.encode(b"bad"), "mode": 0o644}
        journal = {"schema": 1, "phase": "applying", "changes": [change],
                   "transaction": digest(canonical([change])), "old": None, "new": None}
        path = self.project / tx.JOURNAL
        path.write_bytes(canonical(journal))
        with self.assertRaisesRegex(GuidanceError, "target"):
            lifecycle.recover(self.project)
        change["path"] = native.ENTRY
        journal["changes"] = [change, change]
        path.write_bytes(canonical(journal))
        with self.assertRaisesRegex(GuidanceError, "target"):
            lifecycle.recover(self.project)

    def test_automatic_recovery_precedes_retry_and_abandoned_locks_are_not_deleted(self):
        with self.fault("write:" + native.ENTRY), self.assertRaises(OSError):
            self.install_at(self.project)
        result = self.install_at(self.project)
        self.assertEqual(result["status"], "installed")
        lock = self.project / ".guidance/writer-lock"
        lock.mkdir()
        with self.assertRaisesRegex(GuidanceError, "inspect before retry"):
            lifecycle.recover(self.project)
        self.assertTrue(lock.is_dir())
