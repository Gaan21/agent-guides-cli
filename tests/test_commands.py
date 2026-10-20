"""CLI orchestration against synthetic Git, without real network or consumers."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from unittest.mock import patch

from agent_guides_cli import cli, git_source
from agent_guides_cli.integrity import canonical
from fixtures import GitFixture


class CommandTests(GitFixture):
    def invoke(self, *args):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = cli.main(list(args))
        return code, output.getvalue(), errors.getvalue()

    def test_prepare_verify_restore_and_shared_role_commands(self):
        for source in self.request["sources"]:
            source["url"] = f"https://example.invalid/{source['id']}.git"
        request = self.root / "request.json"
        request.write_bytes(canonical(self.request))
        # Substitute only transport locators: exercise real resolution, exact
        # acquisition, CLI parsing, disk publication and role identity together.
        with patch.object(git_source, "locator", side_effect=lambda s, _: str(self.fixtures[s["id"]])):
            code, output, errors = self.invoke("prepare", "--project", str(self.project),
                                                "--request", str(request), "--cache", str(self.cache))
        self.assertEqual((code, errors), (0, ""))
        selection = json.loads(output)["selection"]
        code, output, errors = self.invoke("verify", "--project", str(self.project), "--expected", selection)
        self.assertEqual((code, errors), (0, ""))
        second = self.root / "second"
        second.mkdir()
        with patch.object(git_source, "git", side_effect=AssertionError("offline")):
            code, _, errors = self.invoke("restore", "--project", str(second), "--lock",
                                          str(self.project / "guidance.lock.json"), "--expected", selection,
                                          "--cache", str(self.cache))
        self.assertEqual((code, errors), (0, ""))
        evidence = self.root / "task.json"
        code, output, errors = self.invoke("task-pin", "--project", str(self.project),
                                           "--expected", selection, "--output", str(evidence))
        self.assertEqual((code, errors), (0, ""))
        task = json.loads(output)["task"]
        code, _, errors = self.invoke("task-join", "--project", str(second),
                                      "--identity", str(evidence), "--expected-task", task)
        self.assertEqual((code, errors), (0, ""))
        code, output, errors = self.invoke("verify", "--project", str(self.project), "--expected", "0" * 64)
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("expected selection identity mismatch", errors)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_missing_required_options_and_invalid_input_are_failures(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            cli.main(["prepare"])
        self.assertEqual(caught.exception.code, 2)
        bad = self.root / "bad.json"
        bad.write_bytes(b"{not json}")
        code, output, errors = self.invoke("prepare", "--project", str(self.project), "--request", str(bad))
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("invalid JSON", errors)

    def test_complete_lifecycle_cli_and_connected_restore_dispatch(self):
        for source in self.request["sources"]:
            source["url"] = f"https://example.invalid/{source['id']}.git"
        request = self.root / "install-request.json"
        request.write_bytes(canonical(self.request))
        project = ["--project", str(self.project)]
        with patch.dict("os.environ", {"OPENCODE_DISABLE_PROJECT_CONFIG": ""}), \
                patch.object(git_source, "locator", side_effect=lambda s, _: str(self.fixtures[s["id"]])):
            code, output, errors = self.invoke("install", *project, "--request", str(request),
                                               "--client", "claude", "--client", "opencode",
                                               "--cache", str(self.cache))
            self.assertEqual((code, errors), (0, ""))
            first = json.loads(output)["selection"]
            retained = self.root / "old-lock.json"
            retained.write_bytes((self.project / "guidance.lock.json").read_bytes())
            self.write("alpha", "one/NOTICE", b"Changed source notice.\n")
            self.commit("alpha")
            code, output, errors = self.invoke("update", *project, "--expected", first, "--cache", str(self.cache))
            self.assertEqual((code, errors), (0, ""))
            updated = json.loads(output)["selection"]
            self.assertNotEqual(updated, first)
            for operation in ("status", "verify"):
                code, output, errors = self.invoke(operation, *project, "--expected", updated)
                self.assertEqual((code, errors), (0, ""))
                self.assertEqual(json.loads(output)["status"], "installed")
            with patch.object(git_source, "git", side_effect=AssertionError("offline")):
                code, output, errors = self.invoke("restore", *project, "--lock", str(retained),
                                                   "--expected", first, "--current", updated,
                                                   "--cache", str(self.cache))
            self.assertEqual((code, errors), (0, ""))
            self.assertEqual(json.loads(output)["selection"], first)
            code, output, errors = self.invoke("remove", *project, "--expected", first)
            self.assertEqual((code, errors), (0, ""))
            self.assertEqual(json.loads(output)["status"], "removed")
            code, output, errors = self.invoke("recover", *project)
            self.assertEqual((code, errors), (0, ""))
            self.assertFalse(json.loads(output)["recovered"])
