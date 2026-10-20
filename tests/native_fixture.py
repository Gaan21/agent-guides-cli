"""Disposable native-loader spike; no model calls or live-project registration.

The caller supplies an already retained exact lock, digest and offline cache.
This is test arrangement, not an installation command or a client-load assertion.
"""

import json
import os
from pathlib import Path

from agent_guides_cli import preparation, task_identity


def arrange(project, raw_lock, expected, cache, *, fixtures):
    """Restore one selection and add root/two-scope native candidate bridges.

    Must be called only on a new disposable directory. Returns all policy names
    for independent task capture before launching either installed client.
    """
    project = Path(project)
    project.mkdir()
    result = preparation.restore(project, raw_lock, expected, cache, fixtures=fixtures)
    selection = project / ".guidance" / "selections" / result["snapshot"]
    lock = json.loads(raw_lock)
    policies = []
    for binding in (".", "mobile", "web"):
        directory = project / binding
        directory.mkdir(exist_ok=True)
        label = "root" if binding == "." else binding
        selected = [b for b in lock["bundles"] if b["binding"] == binding]
        entries = [selection / b["source"] / b["id"] / "README.md" for b in selected]
        local = (
            f"# Synthetic {label} policy\n\n"
            f"NATIVE_SCOPE_{label.upper()}. Local exceptions are authoritative.\n"
            "Do not change protected.txt. Do not execute commands or access networks.\n"
        )
        agents = local + "\n<!-- agent-guides-cli:begin -->\n"
        for entry in entries:
            relative = os.path.relpath(entry, directory)
            agents += f"Read the prepared short entry at `{relative}` before applicable work.\n"
        agents += "<!-- agent-guides-cli:end -->\n"
        claude = local + "\n@./local-policy.md\n\n<!-- agent-guides-cli:begin -->\n"
        for entry in entries:
            claude += "@" + os.path.relpath(entry, directory) + "\n"
        claude += "<!-- agent-guides-cli:end -->\n"
        for name, text in {"AGENTS.md": agents, "CLAUDE.md": claude,
                           "local-policy.md": f"Local exception: {label} label is LOCAL_{label.upper()}.\n",
                           "sample.txt": f"Synthetic {label} work item.\n",
                           "protected.txt": "Unrelated protected fixture bytes.\n"}.items():
            path = directory / name
            path.write_text(text)
            policies.append(path.relative_to(project).as_posix())
    return result, policies


def retain(project, expected, output, policies, *, fixtures):
    """Capture once outside generated storage; reviewers join this same record."""
    value = task_identity.capture(project, expected, policies=policies, fixtures=fixtures)
    return task_identity.retain(output, value, project)
