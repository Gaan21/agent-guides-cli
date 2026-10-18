"""Exact Git objects only, never checkout/hooks/source commands.

Argument-array/environment/tree-mode primitives adapted from audited legacy
git_source.py (Apache-2.0, see NOTICE). Resolution and acquisition are separate.
"""

import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urlsplit

from .integrity import (GuidanceError, MAX_FILE, canonical, checked_path, digest,
                        fields, identifier, relative_name)


def git(*arguments, limit=2 * MAX_FILE):
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith("GIT_")}
    environment.update(GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1",
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_NO_REPLACE_OBJECTS="1")
    try:
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
            subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull,
                            "-c", "http.followRedirects=false", "-c", "protocol.ext.allow=never",
                            *map(str, arguments)], env=environment, stdout=output,
                           stderr=errors, timeout=30, check=True)
            output.seek(0)
            value = output.read(limit + 1)
            if len(value) > limit:
                raise GuidanceError("Git output byte limit")
            return value
    except (OSError, subprocess.SubprocessError) as error:
        raise GuidanceError("Git command failed; exact source/object unavailable") from error


def commit(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise GuidanceError("expected exact lowercase Git SHA-1 commit")
    return value


def reference(value):
    if (not isinstance(value, str) or not value.startswith("refs/heads/") or
            len(value) > 240 or re.search(r"[\s\x00-\x20\x7f~^:?*\[\\]", value) or
            any(token in value for token in ("..", "@{", "//")) or
            any(not p or p.startswith(".") or p.endswith((".", ".lock")) for p in value.split("/"))):
        raise GuidanceError("expected explicit refs/heads/... approval channel")
    return value


def source(value, fixtures=None, *, recorded=False):
    fields(value, ("id", "url", "ref", "commit") if recorded else ("id", "url"),
           () if recorded else ("ref", "revision"))
    identifier(value["id"])
    url = value["url"]
    if not isinstance(url, str) or len(url) > 2048 or re.search(r"[\s\x00-\x20\x7f\\]", url):
        raise GuidanceError("invalid Git locator")
    try:
        parsed = urlsplit(url)
        valid = (parsed.scheme == "https" and parsed.hostname and parsed.netloc == parsed.hostname
                 and parsed.path.startswith("/") and parsed.path != "/"
                 and not parsed.username and not parsed.password and not parsed.query and not parsed.fragment)
    except ValueError as error:
        raise GuidanceError("invalid Git locator") from error
    # Dependency injection for disposable tests only; never written as a machine path.
    fixture = fixtures is not None and url == f"fixture://{value['id']}" and value['id'] in fixtures
    if not valid and not fixture:
        raise GuidanceError("credential-free HTTPS Git locator required")
    ref = reference(value.get("ref", "refs/heads/develop"))
    result = dict(value, ref=ref)
    if recorded:
        commit(value["commit"])
    elif "revision" in value:
        commit(value["revision"])
    return result


def locator(value, fixtures):
    if value["url"].startswith("fixture://"):
        path = checked_path(fixtures[value["id"]])
        if not path.is_dir():
            raise GuidanceError("fixture directory unavailable")
        return str(path)
    return value["url"]


def resolve(value, fixtures=None):
    """Called once per selected source only for preparation, never restore/join."""
    if "revision" in value:
        return value["revision"]
    rows = git("ls-remote", "--refs", "--", locator(value, fixtures), value["ref"]).decode().splitlines()
    matches = [row.split()[0] for row in rows if len(row.split()) == 2 and row.split()[1] == value["ref"]]
    if len(matches) != 1:
        raise GuidanceError("approved branch missing or ambiguous")
    return commit(matches[0])


def acquire(value, cache, fixtures=None, *, offline=False):
    """Use the recorded exact commit. Complete cached objects need no network."""
    objects = checked_path(Path(cache) / "git" / digest(canonical(value["url"])))
    revision = commit(value["commit"])
    if objects.exists():
        try:
            if git("--git-dir", objects, "cat-file", "-t", revision).strip() == b"commit":
                return objects
        except GuidanceError:
            pass
    if offline:
        raise GuidanceError(f"missing cached exact commit: {value['id']} {revision}")
    if not objects.exists():
        objects.parent.mkdir(parents=True, exist_ok=True)
        git("init", "--bare", "--template=", objects)
    git("--git-dir", objects, "fetch", "--no-tags", "--depth=1", "--",
        locator(value, fixtures), revision)
    actual = git("--git-dir", objects, "rev-parse", "FETCH_HEAD^{commit}").decode().strip()
    if actual != revision or git("--git-dir", objects, "cat-file", "-t", revision).strip() != b"commit":
        raise GuidanceError("fetched object differs from recorded commit")
    return objects


def tree(objects, revision, bundle_path):
    relative_name(bundle_path, root=True)
    raw = git("--git-dir", objects, "ls-tree", "-rz", revision, "--", bundle_path)
    entries = {}
    prefix = "" if bundle_path == "." else bundle_path + "/"
    try:
        for entry in raw.split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            name = name.decode("utf-8")
            mode, kind, oid = header.decode("ascii").split()
            if not name.startswith(prefix) or mode != "100644" or kind != "blob":
                raise GuidanceError("bundle contains nonregular Git tree mode")
            local = name.removeprefix(prefix)
            relative_name(local)
            entries[local] = oid
    except GuidanceError:
        raise
    except (UnicodeError, ValueError) as error:
        raise GuidanceError("invalid Git bundle tree") from error
    return entries


def blob(objects, oid, limit=MAX_FILE):
    size = int(git("--git-dir", objects, "cat-file", "-s", oid, limit=100))
    if size > limit:
        raise GuidanceError("Git blob byte limit")
    return git("--git-dir", objects, "cat-file", "blob", oid, limit=limit)
