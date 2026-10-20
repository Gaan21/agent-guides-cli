"""Managed prerequisites and root/worktree isolation without launching clients."""

from contextlib import contextmanager
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from unittest.mock import patch

from agent_guides import cli, git_source, host, lifecycle, native, transactions as tx
from agent_guides.integrity import GuidanceError, canonical, parse_json
from fixtures import GitFixture


class ManagedTests(GitFixture):
    def setUp(self):
        super().setUp()
        self.config = self.root / "approved-host.json"
        self.host_bytes = canonical({"instructions": [host.INSTRUCTION],
                                     "policies": [{"action": "tool.use", "resource": "shell:git push *", "effect": "deny"}]})
        self.config.write_bytes(self.host_bytes)
        self.config.chmod(0o444)

    @contextmanager
    def launch(self, project):
        before = os.getcwd()
        try:
            os.chdir(project)
            with patch.dict(os.environ, {"OPENCODE_DISABLE_PROJECT_CONFIG": "1",
                                         "OPENCODE_CONFIG": str(self.config), "PWD": str(project)}):
                yield
        finally:
            os.chdir(before)

    def install(self, project=None, selected=None):
        return lifecycle.install(project or self.project, self.request, selected or ["claude", "opencode"],
                                 self.cache, host_config=self.config, fixtures=self.fixtures)

    def test_managed_route_preserves_host_jsonc_guards_and_shared_claude_import(self):
        original_agents = b"# Local authority\r\nKeep local exceptions.\r\n"
        original_claude = b"# Local Claude policy\r\n@./AGENTS.md\r\n"
        (self.project / "AGENTS.md").write_bytes(original_agents)
        (self.project / "CLAUDE.md").write_bytes(original_claude)
        (self.project / ".opencode").mkdir()
        settings = self.project / ".opencode/opencode.jsonc"
        settings.write_bytes(b'{ // Existing unrelated settings remain bytes\n "model":"user/model"\n}\n')
        root_settings = self.project / "opencode.jsonc"
        root_settings.write_bytes(b'{"permissions":[{"action":"shell","effect":"deny","resource":"*"}]}\n')
        with self.launch(self.project):
            result = self.install()
            self.assertEqual(result["launcher_binding"], "operation_cwd_pwd_checked")
            no_op = lifecycle.install(self.project, self.request, ["claude", "opencode"], self.cache,
                                      expected=result["selection"], fixtures=self.fixtures)
            self.assertFalse(no_op["changed"])
        lock = parse_json(self.read_lock())
        self.assertEqual(lock["connection"]["route"], "managed")
        self.assertIsNone(lock["connection"]["config"])
        agents = (self.project / "AGENTS.md").read_bytes()
        self.assertTrue(agents.startswith(original_agents))
        self.assertIn(b".guidance/selections/", agents)
        self.assertNotIn(b"\r\r\n", agents)
        self.assertEqual(agents.count(native.BEGIN), 1)
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), original_claude)
        self.assertEqual(self.config.read_bytes(), self.host_bytes)
        self.assertIn(b"// Existing", settings.read_bytes())
        self.assertFalse((self.project / native.CONFIG).exists())
        self.assertFalse((self.project / native.ROOT_CONFIG).exists())
        # Offline verification/removal can run outside the launcher environment.
        lifecycle.verify(self.project, result["selection"], fixtures=self.fixtures)
        (self.project / "AGENTS.md").write_bytes(agents + b"New unrelated user policy.\r\n")
        lifecycle.remove(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), original_agents + b"New unrelated user policy.\r\n")
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), original_claude)
        self.assertEqual(self.config.read_bytes(), self.host_bytes)

    def test_root_prerequisites_reject_missing_stale_and_unapproved_environment(self):
        with self.launch(self.project), patch.object(git_source, "resolve", side_effect=AssertionError("no acquisition")):
            for changes in ({"PWD": ""}, {"PWD": "."}, {"PWD": str(self.root)},
                            {"OPENCODE_DISABLE_PROJECT_CONFIG": "0"}, {"OPENCODE_CONFIG": ""}):
                with self.subTest(changes=changes), patch.dict(os.environ, changes):
                    with self.assertRaises(GuidanceError):
                        self.install(selected=["opencode"])
            self.config.chmod(0o644)
            with self.assertRaisesRegex(GuidanceError, "read-only"):
                self.install(selected=["opencode"])
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / "guidance.lock.json").exists())

    def test_exact_managed_restore_requires_approved_local_host_and_stays_offline(self):
        with self.launch(self.project):
            result = self.install()
        raw = self.read_lock()
        second = self.root / "second"
        second.mkdir()
        with self.launch(second), patch.object(git_source, "git", side_effect=AssertionError("offline")):
            with self.assertRaisesRegex(GuidanceError, "host-config"):
                lifecycle.restore(second, raw, result["selection"], self.cache, fixtures=self.fixtures)
            restored = lifecycle.restore(second, raw, result["selection"], self.cache,
                                         host_config=self.config, fixtures=self.fixtures)
        self.assertEqual(restored["selection"], result["selection"])
        self.assertEqual((second / "AGENTS.md").read_bytes(), (self.project / "AGENTS.md").read_bytes())
        self.assertEqual(self.config.read_bytes(), self.host_bytes)

    def test_changed_host_identity_or_owned_entry_is_not_repaired(self):
        with self.launch(self.project):
            result = self.install()
        agents = (self.project / "AGENTS.md").read_bytes()
        self.config.chmod(0o644)
        self.config.write_bytes(canonical({"instructions": [host.INSTRUCTION], "model": "changed/model"}))
        self.config.chmod(0o444)
        changed = self.config.read_bytes()
        with self.assertRaisesRegex(GuidanceError, "identity changed"):
            lifecycle.verify(self.project, result["selection"], fixtures=self.fixtures)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), agents)
        self.assertEqual(self.config.read_bytes(), changed)

    def test_real_linked_worktree_rejects_parent_pwd_then_uses_its_own_index(self):
        worktree = self.root / "linked"
        git_source.git("-C", self.fixtures["alpha"], "worktree", "add", "--detach", worktree, self.commits["alpha"])
        with self.launch(worktree):
            with patch.dict(os.environ, {"PWD": str(self.fixtures["alpha"])}):
                with self.assertRaisesRegex(GuidanceError, "selected project/worktree root"):
                    self.install(worktree, ["opencode"])
            result = self.install(worktree, ["opencode"])
        self.assertEqual(lifecycle.verify(worktree, result["selection"], fixtures=self.fixtures)["status"], "installed")
        self.assertTrue((worktree / "AGENTS.md").is_file())
        self.assertFalse((self.fixtures["alpha"] / "AGENTS.md").exists())

    def test_managed_transaction_faults_recover_without_writing_host_settings(self):
        for index, name in enumerate((native.ENTRY, native.AGENTS, native.CLAUDE, native.STATE, "guidance.lock.json")):
            project = self.root / f"fault-{index}"
            project.mkdir()
            def fail(phase):
                if phase == "write:" + name:
                    raise OSError("simulated managed interruption")
            with self.launch(project), patch.object(tx, "checkpoint", side_effect=fail):
                with self.assertRaises(OSError):
                    self.install(project)
            lifecycle.recover(project)
            for surface in (native.ENTRY, native.AGENTS, native.CLAUDE, native.STATE, "guidance.lock.json"):
                self.assertIsNone(tx.read(project, surface), surface)
            self.assertEqual(self.config.read_bytes(), self.host_bytes)

    def test_managed_update_and_shared_import_removal_restore_preserve_user_bytes(self):
        (self.project / "CLAUDE.md").write_bytes(b"@AGENTS.md\n")
        with self.launch(self.project):
            first = self.install()
            old_raw = self.read_lock()
            self.write("alpha", "one/detail/topic.md", b"Changed guidance.\n")
            self.commit("alpha")
            with patch.object(git_source, "resolve", wraps=git_source.resolve) as resolve:
                updated = lifecycle.update(self.project, first["selection"], self.cache, fixtures=self.fixtures)
            self.assertEqual(resolve.call_count, 2)
            self.assertNotEqual(updated["selection"], first["selection"])
            self.assertEqual((self.project / "CLAUDE.md").read_bytes(), b"@AGENTS.md\n")
            restored = lifecycle.restore(self.project, old_raw, first["selection"], self.cache,
                                         current=updated["selection"], fixtures=self.fixtures)
            self.assertEqual(restored["selection"], first["selection"])
        lifecycle.remove(self.project, first["selection"], fixtures=self.fixtures)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), b"@AGENTS.md\n")
        with self.launch(self.project):
            lifecycle.restore(self.project, old_raw, first["selection"], self.cache,
                              host_config=self.config, fixtures=self.fixtures)
        self.assertEqual(self.config.read_bytes(), self.host_bytes)

    def test_managed_cli_install_remove_and_connected_restore(self):
        for source in self.request["sources"]:
            source["url"] = f"https://example.invalid/{source['id']}.git"
        request = self.root / "request.json"
        request.write_bytes(canonical(self.request))
        def invoke(*args):
            output, errors = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                code = cli.main(list(args))
            self.assertEqual((code, errors.getvalue()), (0, ""))
            return json.loads(output.getvalue())
        common = ["--project", str(self.project)]
        with self.launch(self.project), patch.object(git_source, "locator", side_effect=lambda s, _: str(self.fixtures[s["id"]])):
            result = invoke("install", *common, "--request", str(request), "--client", "opencode",
                            "--host-config", str(self.config), "--cache", str(self.cache))
            raw = self.root / "saved.json"
            raw.write_bytes(self.read_lock())
            invoke("remove", *common, "--expected", result["selection"])
            restored = invoke("restore", *common, "--lock", str(raw), "--expected", result["selection"],
                               "--host-config", str(self.config), "--cache", str(self.cache))
            self.assertEqual(restored["selection"], result["selection"])
