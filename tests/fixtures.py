"""Disposable local Git sources; fixture:// injection never becomes a disk locator."""

from pathlib import Path
import tempfile
import unittest

from agent_guides import git_source, preparation
from agent_guides.integrity import canonical


class GitFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="agent-guides-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        self.cache = self.root / "cache"
        self.fixtures = {}
        for alias in ("alpha", "beta"):
            repo = self.root / alias
            repo.mkdir()
            git_source.git("init", "--template=", "--initial-branch=develop", repo)
            self.fixtures[alias] = repo
        self.bundle("alpha", "one", "common")
        self.bundle("alpha", "two", "extra")
        self.bundle("beta", "one", "private")
        self.commits = {alias: self.commit(alias) for alias in self.fixtures}
        self.request = {
            "schema": 1,
            "sources": [{"id": a, "url": f"fixture://{a}"} for a in self.fixtures],
            "bundles": [
                {"source": "alpha", "path": "one", "binding": "."},
                {"source": "alpha", "path": "two", "binding": "mobile"},
                {"source": "beta", "path": "one", "binding": "web"},
            ],
        }

    def bundle(self, alias, path, identifier):
        directory = self.fixtures[alias] / path
        directory.mkdir(parents=True, exist_ok=True)
        declaration = {"schema": 1, "id": identifier, "entry": "README.md",
                       "files": ["README.md", "detail/topic.md", "NOTICE"], "notices": ["NOTICE"]}
        self.write(alias, f"{path}/guidance-bundle.json", canonical(declaration))
        self.write(alias, f"{path}/README.md", b"Read [topic](detail/topic.md). [External](https://example.org/guide).\n")
        self.write(alias, f"{path}/detail/topic.md", b"[Entry](../README.md)\n")
        self.write(alias, f"{path}/NOTICE", b"Synthetic test content; no product data.\n")

    def write(self, alias, name, data):
        path = self.fixtures[alias] / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def git(self, alias, *args):
        return git_source.git("-C", self.fixtures[alias], *args)

    def commit(self, alias):
        self.git(alias, "add", "--all")
        self.git(alias, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "synthetic fixture")
        return self.git(alias, "rev-parse", "HEAD").decode().strip()

    def prepare(self):
        return preparation.prepare(self.project, self.request, self.cache, fixtures=self.fixtures)

    def verify(self, identity=None):
        return preparation.verify(self.project, identity or self.result["selection"], fixtures=self.fixtures)

    def read_lock(self):
        return (self.project / preparation.LOCK).read_bytes()
