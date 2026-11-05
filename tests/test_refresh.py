"""Opt-in startup update with synthetic mirrors; no live consumers or network."""

import os
import subprocess
from unittest.mock import patch

from agent_guides_cli import git_source, lifecycle, native, preparation, refresh
from agent_guides_cli.integrity import GuidanceError, canonical, parse_json
from fixtures import GitFixture


class RefreshTests(GitFixture):
    def setUp(self):
        super().setUp()
        environment = patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": ""})
        environment.start()
        self.addCleanup(environment.stop)
        git_source.git("init", "--template=", "--initial-branch=main", self.project)
        self.mirrors = git_source.Mirrors()
        for source in self.request["sources"]:
            name = source["id"]
            source["url"] = f"https://example.invalid/{name}.git"
            mirror = self.root / (name + " mirror ' .git")
            git_source.git("clone", "--mirror", self.fixtures[name], mirror)
            git_source.git("--git-dir", mirror, "config", "remote.origin.url", source["url"])
            self.mirrors[name] = mirror
        self.first = lifecycle.install(self.project, self.request, ["claude", "opencode"],
                                       fixtures=self.mirrors)
        self.expectation = self.root / "selection"
        self.expectation.write_text(self.first["selection"] + "\n")
        self.settings = self.root / "refresh.json"
        self.config = {"schema": 1, "project": str(self.project),
                       "selection_file": str(self.expectation),
                       "mirrors": {k: str(v) for k, v in self.mirrors.items()}}
        self.save_settings()

    def save_settings(self):
        self.settings.write_bytes(canonical(self.config))

    def local_fetch(self, source, mirror):
        git_source.git("--git-dir", mirror, "fetch", "--no-tags", "--",
                       self.fixtures[source["id"]], f"+{source['ref']}:{source['ref']}")

    def run_refresh(self):
        with patch.object(refresh, "fetch", side_effect=self.local_fetch):
            return refresh.run(self.project, self.settings)

    def test_refresh_takes_new_commits_once_and_retains_previous_snapshot(self):
        old_lock = self.read_lock()
        self.write("alpha", "one/detail/topic.md", b"New guide text.\n")
        commit = self.commit("alpha")
        result = self.run_refresh()
        self.assertEqual(result["freshness"], "checked")
        self.assertTrue(result["changed"])
        self.assertNotEqual(result["selection"], self.first["selection"])
        self.assertEqual(self.expectation.read_text().strip(), result["selection"])
        self.assertEqual(parse_json(self.read_lock())["sources"][0]["commit"], commit)
        self.assertTrue((self.project / ".guidance/selections" / self.first["snapshot"]).is_dir())
        self.assertNotEqual(self.read_lock(), old_lock)
        again = self.run_refresh()
        self.assertEqual(again["selection"], result["selection"])
        self.assertFalse(again["changed"])

    def test_tool_upgrade_verifies_old_copy_then_records_new_engine(self):
        original = self.read_lock()
        newer_engine = {"version": "newer-development-tool", "digest": "1" * 64}
        with patch.object(preparation, "engine_identity", return_value=newer_engine):
            self.assertEqual(lifecycle.verify(self.project, self.first["selection"],
                                             fixtures=self.mirrors)["status"], "installed")
            self.assertEqual(self.read_lock(), original)
            result = self.run_refresh()
        self.assertEqual(result["freshness"], "checked")
        self.assertEqual(parse_json(self.read_lock())["engine"], newer_engine)
        self.assertEqual(self.expectation.read_text().strip(), result["selection"])
        self.assertNotEqual(result["selection"], self.first["selection"])
        # Exact offline restoration keeps original preparation provenance; it does
        # not need to install the historical tool or resolve new source commits.
        with patch.object(git_source, "git", side_effect=AssertionError("offline restore")):
            restored = lifecycle.restore(self.project, original, self.first["selection"],
                                         current=result["selection"], fixtures=self.mirrors)
        self.assertEqual(restored["selection"], self.first["selection"])
        self.assertEqual(self.read_lock(), original)

    def test_tool_upgrade_does_not_accept_an_altered_prepared_index(self):
        (self.project / native.ENTRY).write_text("Altered local guide index\n")
        with patch.object(preparation, "engine_identity", return_value={"version": "new", "digest": "1" * 64}), \
                patch.object(refresh, "fetch") as fetch, self.assertRaises(GuidanceError):
            refresh.run(self.project, self.settings)
        fetch.assert_not_called()

    def test_changed_provenance_cannot_replace_the_retained_expectation(self):
        value = parse_json(self.read_lock())
        value["engine"]["digest"] = "1" * 64
        (self.project / preparation.LOCK).write_bytes(canonical(value))
        with self.assertRaisesRegex(GuidanceError, "expected selection"):
            self.run_refresh()

    def test_failed_fetch_keeps_intact_copy_and_warns(self):
        old_lock = self.read_lock()
        with patch.object(refresh, "fetch", side_effect=GuidanceError("offline")):
            result = refresh.run(self.project, self.settings)
        self.assertEqual(result["freshness"], "not_checked")
        self.assertIn("may be out of date", result["warning"])
        self.assertEqual(self.read_lock(), old_lock)
        self.assertEqual(self.expectation.read_text().strip(), self.first["selection"])

    def test_partial_download_does_not_publish_mixed_selection(self):
        self.write("alpha", "one/detail/topic.md", b"New guide.\n")
        self.commit("alpha")
        old_lock = self.read_lock()
        def partial(source, mirror):
            if source["id"] == "beta":
                raise GuidanceError("offline")
            self.local_fetch(source, mirror)
        with patch.object(refresh, "fetch", side_effect=partial):
            result = refresh.run(self.project, self.settings)
        self.assertEqual(result["freshness"], "not_checked")
        self.assertEqual(self.read_lock(), old_lock)

    def test_tampered_copy_never_uses_offline_fallback_or_fetches(self):
        (self.project / native.ENTRY).write_text("Altered index\n")
        with patch.object(refresh, "fetch") as fetch, self.assertRaises(GuidanceError):
            refresh.run(self.project, self.settings)
        fetch.assert_not_called()

    def test_removed_connection_is_not_reinstalled(self):
        lifecycle.remove(self.project, self.first["selection"], fixtures=self.mirrors)
        with patch.object(refresh, "fetch") as fetch, self.assertRaisesRegex(GuidanceError, "connect explicitly"):
            refresh.run(self.project, self.settings)
        fetch.assert_not_called()

    def test_other_checkout_rejected_without_creating_storage(self):
        self.config["project"] = str(self.root / "other")
        self.save_settings()
        with self.assertRaisesRegex(GuidanceError, "exact project root"):
            self.run_refresh()

    def test_wrong_mirror_origin_never_fetches(self):
        git_source.git("--git-dir", self.mirrors["beta"], "config", "remote.origin.url",
                       "https://example.invalid/unapproved.git")
        with patch.object(refresh, "fetch") as fetch:
            result = refresh.run(self.project, self.settings)
        fetch.assert_not_called()
        self.assertEqual(result["freshness"], "not_checked")

    def test_extra_mirrors_rejected_without_fetch(self):
        self.config["mirrors"]["extra"] = str(self.root / "extra.git")
        self.save_settings()
        with self.assertRaisesRegex(GuidanceError, "exactly"):
            self.run_refresh()

    def test_automatic_refresh_refuses_tracked_surfaces(self):
        git_source.git("-C", self.project, "add", "--force", "guidance.lock.json")
        with patch.object(refresh, "fetch") as fetch, self.assertRaisesRegex(GuidanceError, "versioned"):
            refresh.run(self.project, self.settings)
        fetch.assert_not_called()

    def test_external_settings_and_expectation_reject_symlinks_or_project_paths(self):
        for location in (self.project / "selection", self.root / "link"):
            if location.name == "link":
                location.symlink_to(self.expectation)
            self.config["selection_file"] = str(location)
            self.save_settings()
            with self.subTest(location=location), self.assertRaises(GuidanceError):
                self.run_refresh()

    def test_failed_expectation_publication_is_not_false_offline_success(self):
        self.write("alpha", "one/detail/topic.md", b"New guide.\n")
        self.commit("alpha")
        with patch.object(refresh, "fetch", side_effect=self.local_fetch), \
                patch.object(refresh, "save_bytes", side_effect=OSError("write failed")), \
                self.assertRaises(GuidanceError):
            refresh.run(self.project, self.settings)
        self.assertEqual(self.expectation.read_text().strip(), self.first["selection"])

    def test_real_fetch_uses_operator_config_without_network(self):
        home = self.root / "operator-home"
        home.mkdir()
        config = ""
        for source in self.request["sources"]:
            config += f'[url "{self.fixtures[source["id"]].as_uri()}"]\n\tinsteadOf = {source["url"]}\n'
        (home / ".gitconfig").write_text(config)
        self.write("alpha", "one/detail/topic.md", b"Real fetch fixture.\n")
        expected_commit = self.commit("alpha")
        with patch.dict(os.environ, {"HOME": str(home)}):
            result = refresh.run(self.project, self.settings)
        self.assertEqual(result["freshness"], "checked")
        self.assertEqual(parse_json(self.read_lock())["sources"][0]["commit"], expected_commit)

    def test_missing_mirror_does_not_create_a_replacement_directory(self):
        missing = self.root / "does-not-exist.git"
        self.config["mirrors"]["beta"] = str(missing)
        self.save_settings()
        with patch.object(refresh, "fetch") as fetch:
            result = refresh.run(self.project, self.settings)
        self.assertFalse(missing.exists())
        self.assertEqual(result["freshness"], "not_checked")
        fetch.assert_not_called()

    def test_fetch_is_bounded_noninteractive_and_has_no_shell_or_raw_logs(self):
        source = dict(self.request["sources"][0], ref="refs/heads/develop")
        with patch.object(refresh.subprocess, "run") as run:
            refresh.fetch(source, self.mirrors["alpha"])
        args, kwargs = run.call_args
        self.assertEqual(args[0][-2:], [source["url"], "+refs/heads/develop:refs/heads/develop"])
        self.assertNotIn("shell", kwargs)
        self.assertEqual(kwargs["env"]["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(kwargs["timeout"], 30)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
        with patch.object(refresh.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 30)), \
                self.assertRaisesRegex(GuidanceError, "timed out"):
            refresh.fetch(source, self.mirrors["alpha"])
