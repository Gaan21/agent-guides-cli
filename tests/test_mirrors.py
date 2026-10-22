"""Operator-maintained local mirrors: approved HTTPS identity, credential-free transport."""

import json
import os
import shutil
import subprocess
import sys
from unittest.mock import patch

from agent_guides_cli import cli, git_source, lifecycle, preparation
from agent_guides_cli.integrity import GuidanceError
from fixtures import GitFixture


class MirrorTests(GitFixture):
    def setUp(self):
        super().setUp()
        environment = patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": ""})
        environment.start()
        self.addCleanup(environment.stop)
        self.mirrors = git_source.Mirrors()
        for source in self.request["sources"]:
            alias = source["id"]
            source["url"] = f"https://example.invalid/{alias}.git"
            mirror = self.root / f"{alias}.git"
            git_source.git("clone", "--quiet", "--mirror", "--", self.fixtures[alias], mirror)
            git_source.git("--git-dir", mirror, "config", "remote.origin.url", source["url"])
            self.mirrors[alias] = mirror

    def refresh(self, alias):
        git_source.git("--git-dir", self.mirrors[alias], "fetch", "--quiet", "--",
                       self.fixtures[alias], "+refs/heads/*:refs/heads/*")

    def assert_no_mirror_path(self):
        files = [self.project / preparation.LOCK, *(self.project / ".guidance").rglob("*")]
        for path in filter(lambda p: p.is_file(), files):
            for mirror in self.mirrors.values():
                self.assertNotIn(str(mirror).encode(), path.read_bytes(), path)

    def test_mirror_records_approved_locator_and_restores_offline(self):
        result = preparation.prepare(self.project, self.request, self.cache, fixtures=self.mirrors)
        self.assertIn("https://example.invalid/alpha.git", self.read_lock().decode())
        self.assert_no_mirror_path()
        second = self.root / "second"
        second.mkdir()
        with patch.object(git_source, "resolve", side_effect=AssertionError("no resolver")):
            restored = preparation.restore(second, self.read_lock(), result["selection"], self.cache)
        self.assertEqual(restored, result)

    def test_install_and_update_follow_refreshed_mirror_once(self):
        result = lifecycle.install(self.project, self.request, ["claude", "opencode"], self.cache,
                                   fixtures=self.mirrors)
        self.write("alpha", "one/NOTICE", b"changed upstream\n")
        moved = self.commit("alpha")
        stale = lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.mirrors)
        self.assertEqual(stale["selection"], result["selection"])  # Stale copy: older commit kept.
        self.refresh("alpha")
        with patch.object(git_source, "resolve", wraps=git_source.resolve) as resolve:
            updated = lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.mirrors)
        self.assertEqual(resolve.call_count, 2)
        lock = preparation.read_lock(self.read_lock(), updated["selection"])
        self.assertEqual({s["id"]: s["commit"] for s in lock["sources"]}["alpha"], moved)
        self.assertEqual(lifecycle.verify(self.project, updated["selection"])["selection"], updated["selection"])
        self.assert_no_mirror_path()

    def test_revision_pin_survives_mirrored_update(self):
        self.request["sources"][0]["revision"] = self.commits["alpha"]
        result = lifecycle.install(self.project, self.request, ["claude"], self.cache, fixtures=self.mirrors)
        self.write("alpha", "one/NOTICE", b"changed upstream\n")
        self.commit("alpha")
        self.refresh("alpha")
        updated = lifecycle.update(self.project, result["selection"], self.cache, fixtures=self.mirrors)
        lock = preparation.read_lock(self.read_lock(), updated["selection"])
        self.assertEqual({s["id"]: s["commit"] for s in lock["sources"]}["alpha"], self.commits["alpha"])

    def test_added_mirrored_source_is_accepted_with_existing_lock(self):
        full = json.loads(json.dumps(self.request))
        self.request["sources"] = self.request["sources"][:1]
        self.request["bundles"] = [b for b in self.request["bundles"] if b["source"] == "alpha"]
        preparation.prepare(self.project, self.request, self.cache,
                            fixtures=git_source.Mirrors(alpha=self.mirrors["alpha"]))
        result = preparation.prepare(self.project, full, self.cache, fixtures=self.mirrors)
        self.assertEqual(len(preparation.read_lock(self.read_lock(), result["selection"])["sources"]), 2)

    def test_rejects_swapped_nonbare_symlinked_missing_or_unselected_mirrors(self):
        link = self.root / "link.git"
        link.symlink_to(self.mirrors["alpha"])
        git_source.git("-C", self.fixtures["alpha"], "config", "remote.origin.url", "https://example.invalid/alpha.git")
        cases = [
            ("mirror origin is not the approved source: alpha", dict(alpha=self.mirrors["beta"], beta=self.mirrors["alpha"])),
            ("not a readable bare Git repository: alpha", dict(alpha=self.fixtures["alpha"])),
            ("not a readable bare Git repository: alpha", dict(alpha=self.fixtures["alpha"] / ".git")),
            ("symlink rejected", dict(alpha=link)),
            ("mirror directory unavailable: beta", dict(alpha=self.mirrors["alpha"], beta=self.root / "missing.git")),
            ("mirror names an unselected source", dict(gamma=self.mirrors["alpha"])),
        ]
        for message, mapping in cases:
            with self.subTest(mapping=mapping), self.assertRaisesRegex(GuidanceError, message):
                preparation.prepare(self.project, self.request, self.cache, fixtures=git_source.Mirrors(mapping))
        self.assertFalse((self.project / preparation.LOCK).exists())
        self.request["sources"][0]["url"] = "fixture://alpha"
        with self.assertRaisesRegex(GuidanceError, "credential-free HTTPS Git locator required"):
            preparation.prepare(self.project, self.request, self.cache, fixtures=self.mirrors)

    def test_cli_mirror_arguments_and_end_to_end_prepare(self):
        isolated = subprocess.run([sys.executable, "-I", "-c", "import agent_guides_cli"], capture_output=True)
        if isolated.returncode:
            self.skipTest("end-to-end CLI needs an installed package (python -I)")
        self.assertIsNone(cli._mirrors([]))
        self.assertEqual(cli._mirrors(["alpha=/a"])["alpha"].as_posix(), "/a")
        for values in (["alpha"], ["alpha="], ["Alpha=/a"], ["alpha=/a", "alpha=/b"]):
            with self.subTest(values=values), self.assertRaises(GuidanceError):
                cli._mirrors(values)
        request = self.root / "request.json"
        request.write_text(json.dumps(self.request))
        command = [sys.executable, "-I", "-m", "agent_guides_cli", "prepare", "--project", self.project,
                   "--request", request, "--cache", self.cache,
                   *(f"--mirror={alias}={path}" for alias, path in self.mirrors.items())]
        output = subprocess.run(command, check=True, capture_output=True, text=True).stdout
        self.assertIn("selection", json.loads(output))
        self.assert_no_mirror_path()
