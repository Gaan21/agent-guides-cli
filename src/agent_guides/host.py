"""Approved read-only managed configuration; never register or launch a host.

The host owner supplies the accepted JSON overlay and binds cwd/PWD. No managed
settings, permissions, project-discovery flags or launchers are modified here.
"""

import os
from pathlib import Path

from .integrity import GuidanceError, checked_path, digest, parse_json, regular_bytes

INSTRUCTION = "{env:PWD}/AGENTS.md"


def disabled():
    return os.environ.get("OPENCODE_DISABLE_PROJECT_CONFIG", "").lower() not in ("", "0", "false")


def root_binding(project):
    pwd = os.environ.get("PWD")
    if not pwd or not Path(pwd).is_absolute():
        raise GuidanceError("managed launch requires an absolute PWD bound to the selected root")
    try:
        valid = checked_path(os.getcwd()).samefile(project) and checked_path(pwd).samefile(project)
    except OSError as error:
        raise GuidanceError("managed cwd/PWD root is unavailable") from error
    if not valid:
        raise GuidanceError("managed cwd and PWD must identify the selected project/worktree root")


def configuration(project, path, expected=None, *, launch=False):
    if not isinstance(path, (str, Path)) or not str(path):
        raise GuidanceError("managed OpenCode requires an explicitly approved --host-config; host settings were not changed")
    path = checked_path(path)
    if path.is_relative_to(project):
        raise GuidanceError("managed configuration must be host-controlled outside the selected project")
    if path.stat().st_mode & 0o222:
        raise GuidanceError("approved host configuration must be read-only")
    raw = regular_bytes(path)
    value = parse_json(raw)
    instructions = value.get("instructions") if isinstance(value, dict) else None
    if (not isinstance(instructions, list) or not all(isinstance(v, str) for v in instructions) or
            instructions.count(INSTRUCTION) != 1 or
            any(".guidance/entry.md" in item for item in instructions)):
        raise GuidanceError("approved host JSON must include the single PWD-bound AGENTS.md instruction")
    identity = digest(raw)
    if expected is not None and identity != expected:
        raise GuidanceError("approved host configuration identity changed; retain the expected identity")
    if launch:
        if not disabled():
            raise GuidanceError("managed route requires the host's existing disabled project discovery; no settings changed")
        configured = os.environ.get("OPENCODE_CONFIG")
        if not configured or not checked_path(configured).samefile(path):
            raise GuidanceError("host must bind OPENCODE_CONFIG to the approved read-only configuration")
        root_binding(project)
    return {"path": str(path), "identity": identity}
