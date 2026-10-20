"""Neutral lifecycle fixtures; no installed clients, host changes or model calls."""

import os
from unittest.mock import patch

from agent_guides import git_source, lifecycle, native, preparation, task_identity
from agent_guides.integrity import GuidanceError, canonical, digest, parse_json
from agent_guides.storage import locked
from fixtures import GitFixture


class LifecycleTests(GitFixture):
    def setUp(self):
        super().setUp()
        environment = patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": ""})
        environment.start()
        self.addCleanup(environment.stop)

    def install(self, selected=None, **kwargs):
        return lifecycle.install(self.project, self.request, selected or ["claude", "opencode"],
                                 self.cache, fixtures=self.fixtures, **kwargs)

    def check(self, expected):
        return lifecycle.verify(self.project, expected, fixtures=self.fixtures)

    def test_install_noop_and_selected_scope_entry(self):
        original = b"# Local policy\r\n\r\nKeep exceptions.\r\n"
        (self.project / "CLAUDE.md").write_bytes(original)
        (self.project / "CLAUDE.md").chmod(0o640)
        (self.project / "AGENTS.md").write_bytes(b"Existing root authority.\n")
        (self.project / "opencode.jsonc").write_bytes(b'{ // keep comments\n "model": "example/model"\n}\n')
        with patch.object(git_source, "resolve", wraps=git_source.resolve) as resolve:
            result = self.install()
        self.assertEqual(resolve.call_count, 2)
        expected = result["selection"]
        self.assertEqual(result["status"], "installed")
        self.assertEqual(result["restart"], ["claude", "opencode"])
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), original + native.block(b"\r\n"))
        self.assertEqual((self.project / "CLAUDE.md").stat().st_mode & 0o777, 0o640)
        entry = (self.project / native.ENTRY).read_text()
        for scope in (".", "mobile", "web"):
            self.assertIn(f"scope `{scope}`", entry)
        self.assertIn(f"selections/{result['snapshot']}/alpha/common/detail/topic.md", entry)
        self.assertNotIn("[Entry](../README.md)", entry)  # No topic bodies injected.
        self.assertIn("https://example.org/guide", entry)
        self.assertEqual((self.project / native.CONFIG).read_bytes(), native.configuration())
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), b"Existing root authority.\n")
        self.assertIn(b"// keep comments", (self.project / "opencode.jsonc").read_bytes())
        with patch.object(git_source, "resolve", side_effect=AssertionError("no implicit latest")):
            self.assertFalse(self.install(expected=expected)["changed"])
            self.assertEqual(preparation.verify(self.project, expected, fixtures=self.fixtures)["status"], "installed")
        self.assertEqual((self.project / result["record"]).read_bytes(), self.read_lock())
        self.assertEqual(self.check(expected)["selection"], expected)

    def test_entry_rendition_relocates_references_images_fragments_and_preserves_labels(self):
        text = ("Read [Details][topic], [Topic] and [Topic][]. ![Image](<detail/topic.md#part>).\n"
                "[Here](#local). [External](https://example.org/guide).\n"
                "[topic]: detail/topic.md \"Title\"\n")
        raw = native.relocate(text, "README.md", "selections/digest/alpha/common")
        self.assertIn("Read [Details][selections-digest-alpha-common-0]", raw)
        self.assertIn("[Topic][selections-digest-alpha-common-0]", raw)
        self.assertIn("![Image](<selections/digest/alpha/common/detail/topic.md#part>)", raw)
        self.assertIn("[Here](selections/digest/alpha/common/README.md#local)", raw)
        self.assertIn('[selections-digest-alpha-common-0]: selections/digest/alpha/common/detail/topic.md "Title"', raw)
        self.assertIn("[External](https://example.org/guide)", raw)

    def test_update_resolves_once_preserves_bytes_and_restores_exact_old_selection(self):
        first = self.install()
        old_raw = self.read_lock()
        claude = self.project / "CLAUDE.md"
        claude.write_bytes(b"User prefix.\n" + claude.read_bytes() + b"User suffix.\n")
        self.write("alpha", "one/detail/topic.md", b"Changed guide.\n")
        new_commit = self.commit("alpha")
        with patch.object(git_source, "resolve", wraps=git_source.resolve) as resolve:
            updated = lifecycle.update(self.project, first["selection"], self.cache, fixtures=self.fixtures)
        self.assertEqual(resolve.call_count, 2)
        self.assertNotEqual(updated["selection"], first["selection"])
        self.assertEqual(parse_json(self.read_lock())["sources"][0]["commit"], new_commit)
        self.assertTrue(claude.read_bytes().startswith(b"User prefix.\n"))
        self.assertTrue(claude.read_bytes().endswith(b"User suffix.\n"))
        self.assertTrue((self.project / ".guidance/selections" / first["snapshot"]).is_dir())
        with patch.object(git_source, "git", side_effect=AssertionError("complete cache stays offline")):
            restored = lifecycle.restore(self.project, old_raw, first["selection"], self.cache,
                                         current=updated["selection"], fixtures=self.fixtures)
        self.assertEqual(restored["selection"], first["selection"])
        self.assertEqual(self.read_lock(), old_raw)

    def test_explicit_revision_policy_survives_update(self):
        self.request["sources"][0]["revision"] = self.commits["alpha"]
        result = self.install()
        self.write("alpha", "one/detail/topic.md", b"Unselected new version.\n")
        self.commit("alpha")
        updated = lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.fixtures)
        self.assertFalse(updated["changed"])
        lock = parse_json(self.read_lock())
        self.assertEqual(lock["sources"][0]["commit"], self.commits["alpha"])
        self.assertEqual(lock["connection"]["revisions"], {"alpha": self.commits["alpha"]})

    def test_remove_preserves_user_edits_lock_retained_versions_and_empty_preexisting_file(self):
        (self.project / "CLAUDE.md").write_bytes(b"")
        first = self.install()
        raw_lock = self.read_lock()
        claude = self.project / "CLAUDE.md"
        claude.write_bytes(b"Before.\n" + claude.read_bytes() + b"After.\n")
        removed = lifecycle.remove(self.project, first["selection"], fixtures=self.fixtures)
        self.assertEqual(removed["status"], "removed")
        self.assertEqual(claude.read_bytes(), b"Before.\nAfter.\n")
        self.assertEqual(self.read_lock(), raw_lock)
        self.assertTrue((self.project / first["record"]).is_file())
        self.assertTrue((self.project / ".guidance/selections" / first["snapshot"]).is_dir())
        self.assertFalse((self.project / native.ENTRY).exists())
        self.assertFalse((self.project / native.CONFIG).exists())
        self.assertFalse(lifecycle.remove(self.project, first["selection"], fixtures=self.fixtures)["changed"])
        restored = lifecycle.restore(self.project, raw_lock, first["selection"], self.cache, fixtures=self.fixtures)
        self.assertEqual(restored["status"], "installed")
        lifecycle.remove(self.project, first["selection"], fixtures=self.fixtures)
        self.assertEqual(claude.read_bytes(), b"Before.\nAfter.\n")

    def test_remove_deletes_only_new_empty_owned_claude_file(self):
        result = self.install(["claude"])
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertFalse((self.project / "CLAUDE.md").exists())
        (self.project / "CLAUDE.md").write_bytes(b"")
        lifecycle.restore(self.project, self.read_lock(), result["selection"], self.cache, fixtures=self.fixtures)
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), b"")

    def test_changed_owned_material_refuses_verify_update_and_remove(self):
        result = self.install()
        owned = self.project / native.CONFIG
        owned.write_bytes(b'{"instructions":["user.md"],"model":"user/model"}\n')
        changed = owned.read_bytes()
        for operation in (lambda: self.check(result["selection"]),
                          lambda: lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.fixtures),
                          lambda: lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)):
            with self.subTest(operation=operation), self.assertRaisesRegex(GuidanceError, "modified owned"):
                operation()
            self.assertEqual(owned.read_bytes(), changed)

    def test_modified_claude_block_preserved_and_rejected(self):
        result = self.install(["claude"])
        path = self.project / "CLAUDE.md"
        path.write_bytes(path.read_bytes().replace(native.IMPORT, b"@./user.md"))
        raw = path.read_bytes()
        with self.assertRaisesRegex(GuidanceError, "modified owned"):
            lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual(path.read_bytes(), raw)

    def test_remove_revalidates_owned_bytes_captured_after_initial_verification(self):
        result = self.install(["opencode"])
        original_verify = lifecycle.verify
        modified = b'{"instructions":["user.md"],"model":"user/model"}\n'
        injected = False
        def concurrent_edit(*args, **kwargs):
            nonlocal injected
            verified = original_verify(*args, **kwargs)
            if not injected:
                injected = True
                (self.project / native.CONFIG).write_bytes(modified)
            return verified
        with patch.object(lifecycle, "verify", side_effect=concurrent_edit):
            with self.assertRaisesRegex(GuidanceError, "modified owned"):
                lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual((self.project / native.CONFIG).read_bytes(), modified)
        self.assertFalse((self.project / ".guidance/transaction.json").exists())

    def test_existing_jsonc_is_preserved_using_an_empty_native_slot(self):
        directory = self.project / ".opencode"
        directory.mkdir()
        path = directory / "opencode.jsonc"
        raw = b'{ // untouched\n "model": "mine"\n}\n'
        path.write_bytes(raw)
        result = self.install(["opencode"])
        self.assertEqual(parse_json(self.read_lock())["connection"]["config"], "opencode.json")
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual(path.read_bytes(), raw)
        self.assertFalse((self.project / "opencode.json").exists())

    def test_occupied_config_slots_and_legacy_loader_fail_before_resolution(self):
        directory = self.project / ".opencode"
        directory.mkdir()
        (directory / "opencode.jsonc").write_bytes(b'{ // keep\n "model":"mine"\n}\n')
        (self.project / "opencode.jsonc").write_bytes(b'{"model":"also-mine"}\n')
        with patch.object(git_source, "resolve", side_effect=AssertionError("no resolution")):
            with self.assertRaisesRegex(GuidanceError, "slots are occupied"):
                self.install(["opencode"])
        (self.project / "CLAUDE.md").write_bytes(b"@./flutter-agent-guidelines/entry.md\n")
        with self.assertRaisesRegex(GuidanceError, "legacy"):
            self.install(["claude"])
        self.assertFalse((self.project / preparation.LOCK).exists())

    def test_inventory_only_selected_clients_and_preserve_guards(self):
        directory = self.project / ".opencode"
        directory.mkdir()
        (directory / "opencode.json").symlink_to(self.root / "not-present")
        (self.project / ".claude").mkdir()
        settings = self.project / ".claude/settings.json"
        raw = b'{"permissions":{"deny":["Bash(git push:*)"]},"hooks":{}}\n'
        settings.write_bytes(raw)
        result = self.install(["claude"])
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual(settings.read_bytes(), raw)
        self.assertTrue((directory / "opencode.json").is_symlink())

    def test_managed_host_is_not_silently_enabled(self):
        with patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": "1"}), \
                patch.object(git_source, "resolve", side_effect=AssertionError("no acquisition")):
            with self.assertRaisesRegex(GuidanceError, "host-controlled"):
                self.install(["opencode"])
        self.assertFalse((self.project / native.CONFIG).exists())
        self.assertFalse((self.project / preparation.LOCK).exists())

    def test_expected_identity_engine_and_path_rejection(self):
        result = self.install()
        raw = self.read_lock()
        with self.assertRaisesRegex(GuidanceError, "expected selection"):
            lifecycle.remove(self.project, "0" * 64, fixtures=self.fixtures)
        value = parse_json(raw)
        value["engine"]["digest"] = "0" * 64
        bad = canonical(value)
        with self.assertRaisesRegex(GuidanceError, "engine"):
            lifecycle.restore(self.project, bad, digest(bad), self.cache, fixtures=self.fixtures)
        (self.project / ".git").mkdir()
        nested = self.project / "nested"
        nested.mkdir()
        with self.assertRaisesRegex(GuidanceError, "root"):
            lifecycle.install(nested, self.request, ["claude"], self.cache, fixtures=self.fixtures)
        self.assertEqual(self.read_lock(), raw)
        self.assertEqual(self.check(result["selection"])["status"], "installed")

    def test_preparation_cannot_overwrite_active_lifecycle(self):
        result = self.install()
        raw = self.read_lock()
        with self.assertRaisesRegex(GuidanceError, "lifecycle"):
            self.prepare()
        with self.assertRaisesRegex(GuidanceError, "lifecycle"):
            preparation.restore(self.project, raw, result["selection"], self.cache, fixtures=self.fixtures)
        self.assertEqual(self.read_lock(), raw)

    def test_offline_restore_second_root_and_shared_task_identity(self):
        result = self.install()
        expected = result["selection"]
        evidence = task_identity.capture(self.project, expected, policies=[native.CONFIG], fixtures=self.fixtures)
        raw = self.read_lock()
        second = self.root / "second"
        second.mkdir()
        with patch.object(git_source, "git", side_effect=AssertionError("offline")):
            restored = lifecycle.restore(second, raw, expected, self.cache, fixtures=self.fixtures)
            joined = task_identity.join(second, canonical(evidence), digest(canonical(evidence)), fixtures=self.fixtures)
        self.assertEqual(restored["selection"], expected)
        self.assertEqual(joined["selection"], expected)
        self.assertEqual((second / native.ENTRY).read_bytes(), (self.project / native.ENTRY).read_bytes())

    def test_task_evidence_retains_selected_settings_and_local_ownership(self):
        settings = self.project / "opencode.jsonc"
        settings.write_bytes(b'{"model":"example/first"}\n')
        result = self.install()
        evidence = task_identity.capture(self.project, result["selection"], fixtures=self.fixtures)
        raw = canonical(evidence)
        expected_task = digest(raw)
        settings.write_bytes(b'{"model":"example/second"}\n')
        self.assertEqual(self.check(result["selection"])["status"], "installed")
        with self.assertRaisesRegex(GuidanceError, "task engine/policy"):
            task_identity.join(self.project, raw, expected_task, fixtures=self.fixtures)
        settings.write_bytes(b'{"model":"example/first"}\n')
        state_path = self.project / native.STATE
        state = parse_json(state_path.read_bytes())
        state["claude_created"] = False
        state_path.write_bytes(canonical(state))
        with self.assertRaisesRegex(GuidanceError, "task engine/policy"):
            task_identity.join(self.project, raw, expected_task, fixtures=self.fixtures)

    def test_missing_offline_cache_and_concurrent_writer_leave_selection_untouched(self):
        result = self.install()
        raw = self.read_lock()
        empty = self.root / "empty-cache"
        with self.assertRaises(GuidanceError):
            lifecycle.restore(self.project, raw, result["selection"], empty, fixtures=self.fixtures)
        with locked(self.project / ".guidance"), \
                patch.object(git_source, "resolve", side_effect=AssertionError("no resolution")):
            with self.assertRaisesRegex(GuidanceError, "writer lock"):
                lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.fixtures)
        self.assertEqual(self.read_lock(), raw)

    def test_local_storage_is_ignored_without_changing_root_ignore_policy(self):
        git_source.git("init", "--template=", "--initial-branch=develop", self.project)
        root_ignore = self.project / ".gitignore"
        root_ignore.write_bytes(b"# User policy\nuser-cache/\n")
        result = self.install()
        ignored = git_source.git("-C", self.project, "check-ignore", ".guidance/entry.md",
                                 ".guidance/.gitignore").decode().splitlines()
        self.assertEqual(ignored, [".guidance/entry.md", ".guidance/.gitignore"])
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual(root_ignore.read_bytes(), b"# User policy\nuser-cache/\n")
        self.assertEqual((self.project / ".guidance/.gitignore").read_bytes(), b"*\n")
        self.check(result["selection"])

    def test_retained_selection_metadata_is_owner_only_and_mode_drift_is_not_repaired(self):
        result = self.install()
        path = self.project / result["record"]
        raw = path.read_bytes()
        self.assertEqual(path.stat().st_mode & 0o7777, 0o400)
        path.chmod(0o444)
        with self.assertRaisesRegex(GuidanceError, "unsafe permissions"):
            lifecycle.retain_lock(self.project, raw)
        self.assertEqual(path.stat().st_mode & 0o7777, 0o444)
        self.assertEqual(path.read_bytes(), raw)
