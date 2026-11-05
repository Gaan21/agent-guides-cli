"""Explicit pre-session direct-work refresh. Never installs hooks or repairs a connection."""

from contextlib import ExitStack
import os
from pathlib import Path
import subprocess

from . import git_source, lifecycle, native, preparation
from .integrity import (GuidanceError, canonical, checked_path, fields, identifier,
                        parse_json, regular_bytes, require_digest)
from .storage import locked, save_bytes


def outside(project, path):
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise GuidanceError("refresh paths must be absolute operator-selected paths")
    path = checked_path(path)
    if path == project or project in path.parents:
        raise GuidanceError("refresh settings, expectation and mirrors must stay outside the project")
    return path


def settings_for(project, settings):
    settings = outside(project, str(settings))
    value = parse_json(regular_bytes(settings))
    fields(value, ("schema", "project", "selection_file", "mirrors"))
    if type(value["schema"]) is not int or value["schema"] != 1 or value["project"] != str(project):
        raise GuidanceError("refresh settings are not approved for this exact project root")
    expectation = outside(project, value["selection_file"])
    if expectation == settings:
        raise GuidanceError("refresh settings and expectation must be separate files")
    if not isinstance(value["mirrors"], dict) or not value["mirrors"]:
        raise GuidanceError("refresh requires explicit operator-maintained mirrors")
    mirrors = git_source.Mirrors({identifier(k): outside(project, v)
                                 for k, v in value["mirrors"].items()})
    if len(set(mirrors.values())) != len(mirrors):
        raise GuidanceError("refresh mirrors must be distinct")
    return expectation, mirrors


def fetch(source, mirror):
    """Use operator authentication, without interactive login, hooks or raw Git logs."""
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    environment.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never",
                       GIT_NO_REPLACE_OBJECTS="1")
    try:
        subprocess.run(
            ["git", "-c", "core.hooksPath=" + os.devnull,
             "-c", "credential.interactive=false", "-c", "protocol.ext.allow=never",
             "-c", "http.followRedirects=false", "--git-dir", str(mirror),
             "fetch", "--no-tags", "--no-recurse-submodules", "--",
             source["url"], f"+{source['ref']}:{source['ref']}"],
            env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=30, check=True)
    except (OSError, subprocess.SubprocessError) as error:
        raise GuidanceError("guide download failed or timed out; latest version not checked") from error


def untracked_surfaces(project):
    """Pre-session refresh must never overwrite versioned integration files."""
    paths = [preparation.LOCK, native.ENTRY, native.STATE, native.CLAUDE_LOCAL, native.CONFIG]
    rows = git_source.git("-C", project, "ls-files", "-z", "--", *paths)
    if rows:
        raise GuidanceError("pre-session refresh refuses versioned guidance integration files")


def run(project, settings):
    project = lifecycle.project_root(project)
    settings = checked_path(settings)
    expectation, mirrors = settings_for(project, settings)
    # The separate expectation remains operator-owned. Never derive approval from
    # the generated lock. Interrupted expectation publication requires explicit review.
    with locked(settings.parent / (settings.name + ".refresh"), operation="refresh", reclaim=True):
        expected_raw = regular_bytes(expectation)
        try:
            expected = require_digest(expected_raw.decode("ascii").strip())
        except UnicodeError as error:
            raise GuidanceError("retained expectation is not an ASCII digest") from error
        previous = lifecycle.verify(project, expected, fixtures=mirrors)
        if previous["status"] != "installed":
            raise GuidanceError("refresh requires an intact installed connection; connect explicitly")
        value = preparation.read_lock(regular_bytes(project / preparation.LOCK), expected, mirrors)
        if lifecycle.route_for(value)["route"] != "project":
            raise GuidanceError("direct-work refresh cannot change a managed connection")
        if value["connection"]["revisions"]:
            raise GuidanceError("latest refresh refuses explicitly pinned sources")
        if set(mirrors) != {s["id"] for s in value["sources"]}:
            raise GuidanceError("refresh mirrors must match the recorded sources exactly")
        untracked_surfaces(project)
        try:
            for source in value["sources"]:
                git_source.locator(source, mirrors)
            with ExitStack() as locks:
                for mirror in sorted(mirrors.values()):
                    locks.enter_context(locked(mirror / "agent-guides-refresh", operation="refresh", reclaim=True))
                # Validate every mirror before starting the first network operation.
                for source in value["sources"]:
                    git_source.locator(source, mirrors)
                for source in value["sources"]:
                    fetch(source, mirrors[source["id"]])
                result = lifecycle.update(project, expected, fixtures=mirrors)
                if regular_bytes(expectation) != expected_raw:
                    raise GuidanceError("retained expectation changed during refresh; inspect explicitly")
                if result["selection"] != expected:
                    save_bytes(expectation, (result["selection"] + "\n").encode())
                return dict(result, freshness="checked", warning=None)
        except (GuidanceError, OSError):
            # No blanket success on errors: tampering, incomplete journals, or a
            # completed update without its expectation must fail this verification.
            fallback = lifecycle.verify(project, expected, fixtures=mirrors)
            if fallback["status"] != "installed":
                raise GuidanceError("no intact installed copy available after refresh failure")
            return dict(fallback, changed=False, freshness="not_checked",
                        warning="Guides could not be refreshed. Using the last verified local copy; "
                                "it may be out of date. Tell the owner and report this limitation.")
