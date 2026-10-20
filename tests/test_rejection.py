"""Adversarial Git/filesystem/link/manifest fixtures; preserve active selections."""

import json
import os
from unittest.mock import patch

from agent_guides_cli import bundles, git_source, preparation
from agent_guides_cli.integrity import (GuidanceError, MAX_FILE, canonical, digest,
                                    parse_json)
from fixtures import GitFixture


class RejectionTests(GitFixture):
    def change_declaration(self, **updates):
        name = self.fixtures["alpha"] / "one/guidance-bundle.json"
        value = json.loads(name.read_bytes())
        value.update(updates)
        name.write_bytes(canonical(value))

    def test_unsafe_links_inline_image_reference_and_encoded(self):
        files = {"README.md": b"", "detail/topic.md": b"", "NOTICE": b""}
        for target in ("../outside.md", "/absolute.md", "file:///tmp/private.md", "C:/private.md",
                       "//host/file", "detail/../../outside.md", "%2e%2e/outside.md",
                       "%252e%252e/outside.md", "detail%5ctopic.md", "missing.md", "Detail/topic.md",
                       "detail/topic.md?alternate=1", "javascript:alert", "%00bad.md"):
            for syntax in (f"[link]({target})", f"![image]({target})", f"[link][ref]\n[ref]: {target}"):
                with self.subTest(target=target, syntax=syntax), self.assertRaises(GuidanceError):
                    bundles.links(dict(files, **{"README.md": syntax.encode()}))
        for text in (b"[topic](detail/topic.md#part)", b"[topic](<detail/topic.md> \"Title\")",
                     b"[external](https://example.org/tutorial?q=a#part)", b"[mail](mailto:a@example.org)"):
            bundles.links(dict(files, **{"README.md": text}))
        for text in (b'<a href="../../outside.md">escape</a>', b"<file:///tmp/private.md>",
                     b"[escape](<../../bad path.md>)"):
            with self.subTest(text=text), self.assertRaises(GuidanceError):
                bundles.links(dict(files, **{"README.md": text}))

    def test_invalid_manifest_schema_inventory_notices_and_bounds(self):
        original = json.loads((self.fixtures["alpha"] / "one/guidance-bundle.json").read_bytes())
        changes = [{"schema": 2}, {"schema": True}, {"entry": "missing.md"}, {"notices": []},
                   {"notices": ["undeclared"]}, {"files": ["README.md", "README.md"]},
                   {"files": ["README.md", "readme.md"]}, {"files": ["README.md", "A/x", "a/y"]},
                   {"files": ["README.md", "dir", "dir/file"]}, {"files": ["README.md", "../NOTICE"]},
                   {"files": ["README.md", "manifest.json"]}, {"files": ["README.md", "guidance-bundle.json"]},
                   {"files": ["README.md", []]}, {"unknown": 1}]
        for updates in changes:
            with self.subTest(updates=updates), self.assertRaises(GuidanceError):
                bundles.declaration(canonical(dict(original, **updates)))
        with self.assertRaises(GuidanceError):
            parse_json(b'{"schema":1,"schema":2}')
        with self.assertRaises(GuidanceError):
            bundles.declaration(b" " * (bundles.MAX_MANIFEST + 1))
        with self.assertRaises(GuidanceError):
            bundles.declaration(canonical(dict(original, files=[f"f{i}" for i in range(513)])))

    def test_nested_and_escaped_labels_cannot_hide_link_or_image_destinations(self):
        for label in ("[outer [inner]]", r"[outer \] inner]"):
            for prefix in ("", "!"):
                for target in ("../../outside.md", "/absolute.png", "file:///tmp/private.md",
                               "detail/topic.md"):
                    text = f"{prefix}{label}({target})".encode()
                    with self.subTest(text=text), self.assertRaisesRegex(GuidanceError, "unsupported inline"):
                        bundles.links({"README.md": text, "detail/topic.md": b""})

    def test_nested_label_rejection_preserves_published_selection(self):
        self.result = self.prepare()
        old = self.read_lock()
        for text in (b"[outer [inner]](../../outside.md)\n",
                     b"![outer [inner]](/absolute.png)\n",
                     b"[outer [inner]](file:///tmp/private.md)\n"):
            self.write("alpha", "one/README.md", text)
            self.commit("alpha")
            with self.subTest(text=text), self.assertRaisesRegex(GuidanceError, "unsupported inline"):
                self.prepare()
            self.assertEqual(self.read_lock(), old)
            self.verify()

    def test_undeclared_missing_duplicate_id_and_oversized_blobs(self):
        self.result = self.prepare()
        original_lock = self.read_lock()
        for kind in ("extra", "missing", "duplicate-id", "oversized"):
            with self.subTest(kind=kind):
                if kind == "extra":
                    self.write("alpha", "one/extra.md", b"undeclared\n")
                elif kind == "missing":
                    (self.fixtures["alpha"] / "one/NOTICE").unlink()
                elif kind == "duplicate-id":
                    self.change_declaration(id="extra")
                else:
                    self.write("alpha", "one/NOTICE", b"x" * (MAX_FILE + 1))
                self.commit("alpha")
                with self.assertRaises(GuidanceError):
                    self.prepare()
                self.assertEqual(self.read_lock(), original_lock)
                self.verify()
                self.git("alpha", "reset", "--hard", self.commits["alpha"])

    def test_git_symlink_executable_and_submodule_modes(self):
        for mode in ("120000", "100755", "160000"):
            with self.subTest(mode=mode):
                blob = self.git("alpha", "rev-parse", "HEAD:one/README.md").decode().strip()
                oid = self.commits["alpha"] if mode == "160000" else blob
                self.git("alpha", "update-index", "--add", "--cacheinfo", f"{mode},{oid},one/attack")
                self.git("alpha", "-c", "user.name=Fixture", "-c", "user.email=f@example.invalid",
                         "-c", "commit.gpgsign=false", "commit", "-m", "tree mode attack")
                with self.assertRaisesRegex(GuidanceError, "nonregular Git tree mode"):
                    self.prepare()
                self.git("alpha", "reset", "--hard", self.commits["alpha"])

    def test_git_case_collisions_from_index_on_any_filesystem(self):
        oid = self.git("alpha", "rev-parse", "HEAD:one/README.md").decode().strip()
        self.git("alpha", "update-index", "--add", "--cacheinfo", f"100644,{oid},one/readme.md")
        self.git("alpha", "-c", "user.name=Fixture", "-c", "user.email=f@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "case attack")
        with self.assertRaisesRegex(GuidanceError, "case-colliding"):
            self.prepare()

    def test_symlink_project_cache_ancestor_lock_and_snapshot(self):
        alias = self.root / "alias"
        alias.symlink_to(self.project, target_is_directory=True)
        with self.assertRaisesRegex(GuidanceError, "symlink rejected"):
            preparation.prepare(alias, self.request, self.cache, fixtures=self.fixtures)
        cache_alias = self.root / "cache-alias"
        self.cache.mkdir()
        cache_alias.symlink_to(self.cache, target_is_directory=True)
        with self.assertRaises(GuidanceError):
            preparation.prepare(self.project, self.request, cache_alias / "nested", fixtures=self.fixtures)
        self.result = self.prepare()
        lock = self.project / preparation.LOCK
        original = lock.read_bytes()
        lock.unlink()
        lock.symlink_to(self.root / "unowned")
        with self.assertRaises(GuidanceError):
            self.prepare()
        self.assertFalse((self.root / "unowned").exists())
        lock.unlink()
        lock.write_bytes(original)
        snapshot = self.project / ".guidance/selections" / self.result["snapshot"]
        leaf = snapshot / "alpha/common/NOTICE"
        leaf.unlink()
        leaf.symlink_to(self.fixtures["alpha"] / "one/NOTICE")
        with self.assertRaises(GuidanceError):
            self.verify()

    def test_missing_extra_tampered_and_rehashed_snapshot_fail_expected_identity(self):
        self.result = self.prepare()
        snapshot = self.project / ".guidance/selections" / self.result["snapshot"]
        leaf = snapshot / "alpha/common/NOTICE"
        old = leaf.read_bytes()
        leaf.unlink()
        with self.assertRaises(OSError):
            self.verify()
        leaf.write_bytes(old)
        (snapshot / "extra.md").write_bytes(b"extra")
        with self.assertRaisesRegex(GuidanceError, "inventory"):
            self.verify()
        (snapshot / "extra.md").unlink()
        leaf.write_bytes(b"tampered")
        with self.assertRaisesRegex(GuidanceError, "content mismatch"):
            self.verify()
        manifest_path = snapshot / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["files"]["alpha/common/NOTICE"] = digest(b"tampered")
        manifest_path.chmod(0o644)
        manifest_path.write_bytes(canonical(manifest))
        with self.assertRaisesRegex(GuidanceError, "manifest identity mismatch"):
            self.verify()
        forged = snapshot.with_name(digest(canonical(manifest)))
        snapshot.rename(forged)
        with self.assertRaisesRegex(GuidanceError, "prepared bundle identity mismatch"):
            self.verify()

    def test_tampered_cache_is_not_repaired_or_switched(self):
        self.result = self.prepare()
        old = self.read_lock()
        item = json.loads(old)["bundles"][0]
        path = self.cache / "bundles" / item["snapshot"]
        leaf = path / "NOTICE"
        leaf.chmod(0o644)
        leaf.write_bytes(b"changed")
        with self.assertRaises(GuidanceError):
            preparation.restore(self.project, old, self.result["selection"], self.cache, fixtures=self.fixtures)
        self.assertEqual(self.read_lock(), old)
        self.assertEqual(leaf.read_bytes(), b"changed")
        self.verify()

    def test_unsupported_selection_schema_rejected_even_with_new_digest(self):
        self.result = self.prepare()
        lock = json.loads(self.read_lock())
        for schema in (2, True):
            lock["schema"] = schema
            raw = canonical(lock)
            with self.assertRaisesRegex(GuidanceError, "unsupported selection schema"):
                preparation.restore(self.project, raw, digest(raw), self.cache, fixtures=self.fixtures)

    def test_git_environment_ignores_injected_options(self):
        with patch.dict(os.environ, {"GIT_DIR": "/missing", "GIT_CONFIG_COUNT": "1",
                                   "GIT_CONFIG_KEY_0": "alias.evil", "GIT_CONFIG_VALUE_0": "!exit 99"}):
            self.result = self.prepare()
        self.verify()
