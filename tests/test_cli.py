"""Public CLI contract, also run against a clean wheel outside the checkout."""

import subprocess
import sys
import unittest
from importlib.metadata import version


class CliTests(unittest.TestCase):
    def test_help_and_identity(self):
        for args in (["--help"], ["--version"], []):
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, "-I", "-m", "agent_guides", *args],
                    capture_output=True, text=True, check=True,
                )
                self.assertIn("agent-guides", result.stdout)
                self.assertFalse(result.stderr)
                if args == ["--version"]:
                    self.assertEqual(
                        result.stdout.strip(), f"agent-guides {version('agent-guides')}"
                    )

    def test_lifecycle_operations_require_explicit_inputs(self):
        for operation in ("install", "update", "status", "remove", "recover"):
            with self.subTest(operation=operation):
                result = subprocess.run(
                    [sys.executable, "-I", "-m", "agent_guides", operation],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("required", result.stderr)


if __name__ == "__main__":
    unittest.main()
