"""Public CLI contract, also run against a clean wheel outside the checkout."""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

from agent_guides_cli import cli, refresh


class CliTests(unittest.TestCase):
    def test_help_and_identity(self):
        for args in (["--help"], ["--version"], []):
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, "-I", "-m", "agent_guides_cli", *args],
                    capture_output=True, text=True, check=True,
                )
                self.assertIn("agent-guides-cli", result.stdout)
                self.assertFalse(result.stderr)
                if args == ["--version"]:
                    self.assertEqual(
                        result.stdout.strip(), f"agent-guides-cli {version('agent-guides-cli')}"
                    )

    def test_lifecycle_operations_require_explicit_inputs(self):
        for operation in ("install", "update", "status", "remove", "recover"):
            with self.subTest(operation=operation):
                result = subprocess.run(
                    [sys.executable, "-I", "-m", "agent_guides_cli", operation],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("required", result.stderr)

    def test_refresh_guides_targets_the_enclosing_git_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / ".git").mkdir()
            (root / "a" / "b").mkdir(parents=True)
            previous = Path.cwd()
            self.addCleanup(os.chdir, previous)
            os.chdir(root / "a" / "b")
            with patch.object(refresh, "run", return_value={"freshness": "checked"}) as run, \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(cli.refresh_guides([]), 0)
            project, settings = run.call_args.args
            self.assertEqual(project, root)
            self.assertEqual(settings.name, root.name + ".refresh.json")
            self.assertIn('"freshness":"checked"', output.getvalue())
            (root / ".git").rmdir()
            with patch.object(refresh, "run") as run, \
                    contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(cli.refresh_guides([]), 1)
            run.assert_not_called()
            self.assertIn("not inside a Git project", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
