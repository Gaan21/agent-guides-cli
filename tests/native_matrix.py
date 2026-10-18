"""Additional disposable loader arrangements over retained, exact fixture bytes.

These helpers neither resolve sources nor run clients. Callers retain any changed
policy as a separately named candidate before invoking an installed client.
"""

from pathlib import Path
import shutil


def replica(retained, destination, *, conflicts=False):
    """Copy a retained fixture to a new root, optionally adding local conflicts."""
    retained, destination = Path(retained), Path(destination)
    shutil.copytree(retained, destination, ignore=shutil.ignore_patterns(".git"))
    if conflicts:
        for scope in (".", "mobile", "web"):
            directory = destination / scope
            label = "ROOT" if scope == "." else scope.upper()
            rule = (
                f"\nLocal exception: NATIVE_CHOICE is {label}_CHOICE here. "
                "A nearer folder's explicit NATIVE_CHOICE overrides an ancestor's "
                "value only for work inside that folder.\n"
            )
            for name in ("AGENTS.md", "local-policy.md"):
                path = directory / name
                path.write_text(path.read_text() + rule)
    return destination
