"""Audited identity/path primitives adapted from flutter-agent-guidelines.

Apache-2.0; see NOTICE. Bounds and strict JSON parsing added for neutral inputs.
These checks are not a same-user sandbox or a publisher trust decision.
"""

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat

MAX_FILE = 1024 * 1024
MAX_TOTAL = 16 * MAX_FILE
MAX_FILES = 512
MAX_JSON = MAX_FILE


class GuidanceError(ValueError):
    """Invalid input, missing exact data or an integrity mismatch."""


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode()


def digest(content):
    return hashlib.sha256(content).hexdigest()


def require_digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise GuidanceError("expected lowercase SHA-256")
    return value


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value):
        raise GuidanceError("expected lowercase identifier (1–64 characters)")
    return value


def relative_name(name, *, root=False):
    if root and name == ".":
        return PurePosixPath(".")
    if not isinstance(name, str) or not name or len(name) > 240 or "\\" in name or ":" in name:
        raise GuidanceError("invalid relative path")
    path = PurePosixPath(name)
    if (path.is_absolute() or path.as_posix() != name or name == "." or
            any(part in (".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", part)
                for part in path.parts)):
        raise GuidanceError(f"unsafe relative path: {name}")
    return path


def checked_path(path):
    path = Path(path).absolute()
    if ".." in path.parts:
        raise GuidanceError("path traversal rejected")
    for part in (*reversed(path.parents), path):
        if part.is_symlink():
            raise GuidanceError(f"symlink rejected: {part}")
    return path


def regular_bytes(path, limit=MAX_FILE):
    path = checked_path(path)
    if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > limit:
        raise GuidanceError(f"expected bounded regular file: {path}")
    with path.open("rb") as stream:
        value = stream.read(limit + 1)
    if len(value) > limit:
        raise GuidanceError("file exceeds byte limit")
    return value


def parse_json(raw, limit=MAX_JSON):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise GuidanceError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    if len(raw) > limit:
        raise GuidanceError("JSON exceeds byte limit")
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(GuidanceError("nonfinite JSON")))
    except (ValueError, UnicodeError, RecursionError) as error:
        raise GuidanceError("invalid JSON") from error


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or set(value) - set(required) - set(optional):
        raise GuidanceError("unexpected or missing object fields")


def inventory(names, *, directories=False):
    """Reject ambiguous files/directories even on a case-sensitive host."""
    if not names or len(names) > MAX_FILES or len(set(names)) != len(names):
        raise GuidanceError("invalid inventory size or duplicate files")
    seen = {}
    files = set(names)
    for name in names:
        path = relative_name(name)
        for node in (path, *path.parents):
            if str(node) == ".":
                continue
            key = str(node).casefold()
            if key in seen and seen[key] != str(node):
                raise GuidanceError("case-colliding paths")
            seen[key] = str(node)
        if not directories and any(str(parent) in files for parent in path.parents):
            raise GuidanceError("file/directory collision")
