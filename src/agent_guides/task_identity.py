"""Host-retained role evidence; no leases, task registry or model enforcement."""

import os

from .integrity import (GuidanceError, canonical, checked_path, digest, fields,
                        inventory, parse_json, regular_bytes, relative_name)
from .preparation import LOCK, engine_identity, read_lock, verify


def policy_names(project):
    # Native root policies only. Nested/indirect imports/configuration must be
    # supplied explicitly; do not claim exhaustive native loader discovery.
    return [name for name in ("AGENTS.md", "CLAUDE.md")
            if (project / name).exists() or (project / name).is_symlink()]


def hashes(project, names):
    if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        raise GuidanceError("policy/overlay inputs must be relative path lists")
    if not names:
        return {}
    inventory(names)
    result = {}
    for name in sorted(names):
        relative_name(name)
        if name.split("/")[0] in (".guidance", "guidance.lock.json"):
            raise GuidanceError("generated files cannot be independent policy/overlay inputs")
        result[name] = digest(regular_bytes(project / name))
    return result


def capture(project, expected, policies=(), overlays=(), *, fixtures=None):
    project = checked_path(project)
    verify(project, expected, fixtures=fixtures)
    selection = read_lock(regular_bytes(project / LOCK), expected, fixtures)
    policy = sorted(set(policy_names(project)) | set(policies))
    return {"schema": 1, "selection": expected, "engine": engine_identity(),
            "sources": selection["sources"], "bundles": selection["bundles"],
            "policy": hashes(project, policy), "overlays": hashes(project, list(overlays))}


def retain(path, value, project):
    """Exclusive output: never silently replace a role's expected identity."""
    path, project = checked_path(path), checked_path(project)
    if path.is_relative_to(project / ".guidance") or path == project / "guidance.lock.json":
        raise GuidanceError("retain expected task identity independently of generated storage")
    # Expected evidence is host-owned, explicitly located, and deliberately not
    # automatically copied into a portable lock or consumer instructions.
    with path.open("xb") as stream:
        stream.write(canonical(value))
        stream.flush()
        os.fsync(stream.fileno())
    return digest(canonical(value))


def join(project, raw, expected_task, *, fixtures=None):
    if digest(raw) != expected_task:
        raise GuidanceError("expected task identity mismatch")
    value = parse_json(raw)
    fields(value, ("schema", "selection", "sources", "bundles", "engine", "policy", "overlays"))
    if type(value["schema"]) is not int or value["schema"] != 1 or canonical(value) != raw:
        raise GuidanceError("unsupported task identity schema/encoding")
    if not isinstance(value["policy"], dict) or not isinstance(value["overlays"], dict):
        raise GuidanceError("invalid policy/overlay identity")
    actual = capture(project, value["selection"], list(value["policy"]),
                     list(value["overlays"]), fixtures=fixtures)
    if actual != value:
        raise GuidanceError("task engine/policy/overlay identity mismatch; preserve expected evidence")
    return {"task": expected_task, "selection": value["selection"]}
