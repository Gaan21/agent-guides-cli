"""Build from sdist, inspect exact wheel resources, and test a clean install."""

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import venv
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd):
    subprocess.run(args, cwd=cwd, check=True)


class DistributionTests(unittest.TestCase):
    def test_clean_distribution(self):
        with tempfile.TemporaryDirectory(prefix="agent-guides-dist-") as temporary:
            work = Path(temporary)
            artifacts = work / "artifacts"
            run(sys.executable, "-m", "build", "--sdist", "--outdir",
                str(artifacts), str(ROOT), cwd=work)
            sdist, = artifacts.glob("*.tar.gz")
            with tarfile.open(sdist) as archive:
                members = archive.getmembers()
                prefix = members[0].name.split("/")[0]
                names = {m.name.removeprefix(prefix + "/") for m in members if m.isfile()}
                required = {
                    "LICENSE", "NOTICE", "README.md", "AGENTS.md", "pyproject.toml",
                    "MANIFEST.in", "docs/delivery-scope.md",
                    "docs/delivery-implementation-plan.md", "docs/tasks/README.md",
                    "tests/test_cli.py", "tests/check_distribution.py",
                }
                required.update(str(p.relative_to(ROOT)) for p in (ROOT / "docs/tasks").glob("*.md"))
                self.assertTrue(required <= names, required - names)
                self.assertFalse(any("flutter_agent_guidelines" in n for n in names))
                for member in members:
                    self.assertFalse(member.issym() or member.islnk())
                    self.assertFalse(Path(member.name).is_absolute())
                    self.assertNotIn("..", Path(member.name).parts)
                    if member.isfile() and member.name.endswith(("/LICENSE", "/NOTICE")):
                        self.assertEqual(archive.extractfile(member).read(),
                                         (ROOT / Path(member.name).name).read_bytes())
                archive.extractall(work / "source", filter="data")
            source = work / "source" / prefix
            run(sys.executable, "-m", "build", "--wheel", "--outdir",
                str(artifacts), str(source), cwd=work)
            wheel, = artifacts.glob("*.whl")
            with zipfile.ZipFile(wheel) as archive:
                names = set(archive.namelist())
                metadata, = (n.rsplit("/", 1)[0] for n in names if n.endswith("/METADATA"))
                expected = {
                    "agent_guides/__init__.py", "agent_guides/__main__.py", "agent_guides/cli.py",
                    *(f"{metadata}/{name}" for name in (
                        "METADATA", "WHEEL", "entry_points.txt", "top_level.txt", "RECORD",
                        "licenses/LICENSE", "licenses/NOTICE",
                    )),
                }
                self.assertEqual(names, expected)
                for notice in ("LICENSE", "NOTICE"):
                    self.assertEqual(archive.read(f"{metadata}/licenses/{notice}"),
                                     (ROOT / notice).read_bytes())
                text = archive.read(f"{metadata}/METADATA").decode()
                self.assertIn("Requires-Python: >=3.11", text)
                self.assertNotIn("Requires-Dist:", text)
            environment = work / "tools"
            venv.EnvBuilder(with_pip=True).create(environment)
            python = environment / "bin/python"
            run(str(python), "-I", "-m", "pip", "install", "--no-deps", str(wheel), cwd=work)
            run(str(environment / "bin/agent-guides"), "--help", cwd=work)
            run(str(environment / "bin/agent-guides"), "--version", cwd=work)
            # The tests come from the sdist; isolated Python imports only the installed wheel.
            run(str(python), "-I", str(source / "tests/test_cli.py"), "-v", cwd=work)
            retention = os.environ.get("AGENT_GUIDES_ARTIFACT_DIR")
            if retention:
                destination = Path(retention)
                self.assertTrue(destination.is_dir(), "Create the artifact directory explicitly first")
                for artifact in (sdist, wheel):
                    target = destination / artifact.name
                    with target.open("xb") as handle:
                        handle.write(artifact.read_bytes())
            for artifact in (sdist, wheel):
                print(f"{artifact.name} SHA256 {hashlib.sha256(artifact.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    unittest.main()
