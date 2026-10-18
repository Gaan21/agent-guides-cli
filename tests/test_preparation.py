"""Real Git acceptance: exact multi-source preparation and offline restoration."""

import copy
import json
from pathlib import Path
import shutil
from unittest.mock import patch

from agent_guides import git_source, preparation
from agent_guides.integrity import GuidanceError, canonical
from agent_guides.storage import locked
from agent_guides import storage
from fixtures import GitFixture


class PreparationTests(GitFixture):
    def test_resolve_once_and_offline_restore_after_branches_move(self):
        with patch.object(git_source, "resolve", wraps=git_source.resolve) as resolver:
            self.result = self.prepare()
            self.assertEqual(resolver.call_count, 2)
        lock = json.loads(self.read_lock())
        self.assertEqual({s["id"]: s["commit"] for s in lock["sources"]}, self.commits)
        self.assertEqual(len(lock["bundles"]), 3)
        self.assertNotIn(str(self.root), self.read_lock().decode())
        for alias in self.fixtures:
            self.write(alias, "one/NOTICE", b"changed upstream\n")
            self.commit(alias)
        with patch.object(git_source, "resolve", side_effect=AssertionError("no latest")), \
                patch.object(git_source, "git", side_effect=AssertionError("no Git/network")):
            self.verify()
            second = self.root / "second"
            second.mkdir()
            actual = preparation.restore(second, self.read_lock(), self.result["selection"],
                                         self.cache, fixtures=self.fixtures)
            self.assertEqual(actual, self.result)
            preparation.verify(second, self.result["selection"], fixtures=self.fixtures)
        path = self.project / ".guidance/selections" / self.result["snapshot"]
        self.assertEqual((path / "alpha/common/detail/topic.md").read_bytes(), b"[Entry](../README.md)\n")
        self.assertIn(b"https://example.org/guide", (path / "alpha/common/README.md").read_bytes())

    def test_offline_objects_reconstruct_missing_bundle_cache(self):
        self.result = self.prepare()
        raw = self.read_lock()
        shutil.rmtree(self.cache / "bundles")
        original = git_source.git
        def offline(*args, **kwargs):
            self.assertNotIn("fetch", args)
            self.assertNotIn("ls-remote", args)
            return original(*args, **kwargs)
        with patch.object(git_source, "resolve", side_effect=AssertionError("no resolver")), \
                patch.object(git_source, "git", side_effect=offline):
            self.assertEqual(preparation.restore(self.project, raw, self.result["selection"],
                                                self.cache, fixtures=self.fixtures), self.result)
        self.verify()

    def test_missing_cache_does_not_switch_or_fetch(self):
        self.result = self.prepare()
        old = self.read_lock()
        empty = self.root / "empty-cache"
        with patch.object(git_source, "resolve", side_effect=AssertionError("no resolver")), \
                patch.object(git_source, "git", side_effect=AssertionError("no network")):
            with self.assertRaisesRegex(GuidanceError, "missing cached exact commit: alpha"):
                preparation.restore(self.project, old, self.result["selection"], empty, fixtures=self.fixtures)
        self.assertEqual(self.read_lock(), old)
        self.verify()

    def test_explicit_revision_precedes_branch_and_acquisition_never_reresolves(self):
        self.request["sources"][0]["revision"] = self.commits["alpha"]
        self.request["sources"][0]["ref"] = "refs/heads/missing"
        original = git_source.resolve
        def moving(source, fixtures):
            selected = original(source, fixtures)
            self.write(source["id"], "one/NOTICE", b"moved after resolve\n")
            self.commit(source["id"])
            return selected
        with patch.object(git_source, "resolve", side_effect=moving) as resolver:
            self.result = self.prepare()
            self.assertEqual(resolver.call_count, 2)
        self.assertEqual({s["id"]: s["commit"] for s in json.loads(self.read_lock())["sources"]}, self.commits)
        self.verify()

    def test_multiple_scopes_share_bundle_bytes_without_duplicate_resolution(self):
        self.request["bundles"].append({"source": "alpha", "path": "one", "binding": "mobile"})
        self.result = self.prepare()
        lock = json.loads(self.read_lock())
        common = [b for b in lock["bundles"] if b["id"] == "common"]
        self.assertEqual(len(common), 2)
        self.assertEqual(common[0]["snapshot"], common[1]["snapshot"])
        self.verify()

    def test_prepare_failure_preserves_existing_lock_and_snapshot(self):
        self.result = self.prepare()
        old = self.read_lock()
        self.write("beta", "one/README.md", b"[Escape](../../outside.md)\n")
        self.commit("beta")
        with self.assertRaises(GuidanceError):
            self.prepare()
        self.assertEqual(self.read_lock(), old)
        self.verify()

    def test_noop_preparation_and_held_writer_lock(self):
        self.result = self.prepare()
        self.assertEqual(self.prepare(), self.result)
        with locked(self.project / ".guidance"):
            with self.assertRaisesRegex(GuidanceError, "writer lock exists"):
                self.prepare()
        self.verify()

    def test_unsafe_inputs_fail_before_resolution(self):
        mutations = []
        for url in ("/tmp/source", "file:///tmp/source", "ext::command", "https://u:p@example.org/repo",
                    "https://example.org/repo?token=secret", "ssh://host/repo", "--upload-pack=cmd"):
            value = copy.deepcopy(self.request)
            value["sources"][0]["url"] = url
            mutations.append(value)
        for ref in ("develop", "refs/heads/../main", "refs/heads/x.lock", "refs/heads/a:b", "refs/heads/a\n"):
            value = copy.deepcopy(self.request)
            value["sources"][0]["ref"] = ref
            mutations.append(value)
        for key, value in (("path", "../one"), ("binding", "/absolute"), ("source", "unknown")):
            item = copy.deepcopy(self.request)
            item["bundles"][0][key] = value
            mutations.append(item)
        duplicate = copy.deepcopy(self.request)
        duplicate["sources"].append(duplicate["sources"][0])
        mutations.append(duplicate)
        duplicate = copy.deepcopy(self.request)
        duplicate["bundles"].append(duplicate["bundles"][0])
        mutations.append(duplicate)
        for value in mutations:
            with self.subTest(value=value), patch.object(git_source, "resolve", side_effect=AssertionError("early")):
                with self.assertRaises(GuidanceError):
                    preparation.prepare(self.project, value, self.cache, fixtures=self.fixtures)
        self.assertFalse((self.project / preparation.LOCK).exists())

    def test_altered_lock_and_expected_digest_fail(self):
        self.result = self.prepare()
        raw = self.read_lock()
        with self.assertRaisesRegex(GuidanceError, "expected selection identity"):
            preparation.restore(self.project, raw, "0" * 64, self.cache, fixtures=self.fixtures)
        altered = json.loads(raw)
        altered["sources"][0]["commit"] = "a" * 40
        (self.project / preparation.LOCK).write_bytes(canonical(altered))
        with self.assertRaises(GuidanceError):
            self.verify()
        (self.project / preparation.LOCK).write_bytes(raw)
        self.verify()

    def test_publication_failure_and_concurrent_lock_edit_preserve_previous_bytes(self):
        self.result = self.prepare()
        old = self.read_lock()
        self.write("alpha", "one/NOTICE", b"new version\n")
        self.commit("alpha")
        original = storage.os.replace
        def fail_lock(source, destination):
            if Path(destination) == self.project / preparation.LOCK:
                raise OSError("injected lock publication failure")
            return original(source, destination)
        with patch.object(storage.os, "replace", side_effect=fail_lock):
            with self.assertRaises(OSError):
                self.prepare()
        self.assertEqual(self.read_lock(), old)
        self.verify()
        original_publish = preparation.publish
        def edit_then_publish(project, value, cache, preimage):
            (project / preparation.LOCK).write_bytes(b"owner edit\n")
            return original_publish(project, value, cache, preimage)
        with patch.object(preparation, "publish", side_effect=edit_then_publish):
            with self.assertRaisesRegex(GuidanceError, "changed during preparation"):
                self.prepare()
        self.assertEqual(self.read_lock(), b"owner edit\n")
        # An unrelated pre-existing lock is a collision, not permission to replace.
        with patch.object(git_source, "resolve", side_effect=AssertionError("early")):
            with self.assertRaises(GuidanceError):
                self.prepare()
