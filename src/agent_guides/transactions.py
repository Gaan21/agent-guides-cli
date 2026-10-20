"""Durable before/after journals; individual renames are not a transaction.

Interrupted, uncommitted changes roll back on the next mutation. Unknown user
edits stop recovery before any restoration. Abandoned writer locks stay manual.
"""

import base64
import binascii
import stat
from .integrity import (GuidanceError, MAX_TOTAL, canonical, checked_path, digest, fields,
                        parse_json, regular_bytes, require_digest)
from .storage import make_directory, save_bytes, sync_directory
from .native import AGENTS, CLAUDE, CONFIG, ROOT_CONFIG, ENTRY, STATE
from .preparation import LOCK

JOURNAL = ".guidance/transaction.json"
SURFACES = (ENTRY, AGENTS, CLAUDE, CONFIG, ROOT_CONFIG, STATE, LOCK)


def encode(raw):
    return None if raw is None else base64.b64encode(raw).decode("ascii")


def decode(value):
    if value is None:
        return None
    try:
        if not isinstance(value, str):
            raise ValueError()
        raw = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as error:
        raise GuidanceError("invalid journal/ownership bytes") from error
    if len(raw) > 1024 * 1024 or encode(raw) != value:
        raise GuidanceError("noncanonical or oversized journal bytes")
    return raw


def read(project, name):
    path = checked_path(project / name)
    return regular_bytes(path, MAX_TOTAL if name == JOURNAL else 1024 * 1024) if path.exists() else None


def file_mode(project, name):
    path = checked_path(project / name)
    return stat.S_IMODE(path.stat().st_mode) if path.exists() else None


class Preimages(dict):
    """Freeze permission identity alongside bytes before preparation/verification."""

    def __init__(self, project, names):
        super().__init__((name, read(project, name)) for name in names)
        self.modes = {name: file_mode(project, name) for name in self}

    def plan(self, after):
        return [(name, before, after[name], self.modes[name]) for name, before in self.items()]


def write(project, name, raw, mode):
    path = checked_path(project / name)
    if raw is None:
        path.unlink(missing_ok=True)
        sync_directory(path.parent)
    else:
        make_directory(path.parent)
        save_bytes(path, raw, mode=mode)


def checkpoint(phase):
    """Fault-injection seam; no runtime callbacks are loaded."""


def load(project):
    raw = regular_bytes(project / JOURNAL, MAX_TOTAL)
    value = parse_json(raw, MAX_TOTAL)
    fields(value, ("schema", "phase", "changes", "transaction", "old", "new"))
    if (type(value["schema"]) is not int or value["schema"] != 1 or
            value["phase"] not in ("applying", "committed") or canonical(value) != raw):
        raise GuidanceError("unsupported transaction journal")
    changes = value["changes"]
    if not isinstance(changes, list) or not 1 <= len(changes) <= len(SURFACES):
        raise GuidanceError("invalid transaction change count")
    seen = set()
    for change in changes:
        fields(change, ("path", "before", "after", "mode"))
        if change["path"] not in SURFACES or change["path"] in seen:
            raise GuidanceError("invalid transaction target")
        seen.add(change["path"])
        decode(change["before"])
        decode(change["after"])
        if type(change["mode"]) is not int or not 0 <= change["mode"] <= 0o777:
            raise GuidanceError("invalid transaction file mode")
        if change["path"] == LOCK:
            for field, image in (("old", "before"), ("new", "after")):
                content = decode(change[image])
                if value[field] != (digest(content) if content is not None else None):
                    raise GuidanceError("journal selection identity mismatch")
    for name in ("old", "new"):
        if value[name] is not None:
            require_digest(value[name])
    if value["transaction"] != digest(canonical(changes)):
        raise GuidanceError("journal transaction identity mismatch")
    return value


def finish(project, value, phase):
    """Retain exact transaction evidence; never garbage-collect recovery bytes."""
    raw = canonical(dict(value, phase=phase))
    parent = checked_path(project / ".guidance/transactions")
    make_directory(parent)
    archive = parent / (digest(raw) + ".json")
    if archive.exists():
        if regular_bytes(archive, MAX_TOTAL) != raw or stat.S_IMODE(archive.stat().st_mode) != 0o400:
            raise GuidanceError("archived transaction modified or unsafe permissions; preserve evidence")
    else:
        save_bytes(archive, raw, mode=0o400)
    checkpoint("archived:" + phase)
    (project / JOURNAL).unlink()
    sync_directory(project / ".guidance")


def recover(project):
    if read(project, JOURNAL) is None:
        return False
    value = load(project)
    current_lock = read(project, LOCK)
    if (digest(current_lock) if current_lock is not None else None) not in (value["old"], value["new"]):
        raise GuidanceError("recovery conflict; selection lock changed")
    # Preflight every path first. Never half-rollback around known unknown edits.
    for change in value["changes"]:
        current = (read(project, change["path"]), file_mode(project, change["path"]))
        after = decode(change["after"])
        allowed = [(after, change["mode"] if after is not None else None)]
        if value["phase"] == "applying":
            before = decode(change["before"])
            allowed.append((before, change["mode"] if before is not None else None))
        if current not in allowed:
            raise GuidanceError(f"recovery conflict; preserve edits: {change['path']}")
    if value["phase"] == "applying":
        for change in reversed(value["changes"]):
            before, after = decode(change["before"]), decode(change["after"])
            current = read(project, change["path"])
            mode = file_mode(project, change["path"])
            before_image = (before, change["mode"] if before is not None else None)
            after_image = (after, change["mode"] if after is not None else None)
            if (current, mode) not in (before_image, after_image):
                raise GuidanceError(f"recovery preimage changed: {change['path']}")
            if current != before:
                write(project, change["path"], before, change["mode"])
                checkpoint("rollback:" + change["path"])
    finish(project, value, "rolled_back" if value["phase"] == "applying" else "committed")
    return True


def apply(project, planned, verify):
    changes = []
    for image in planned:
        name, before, after = image[:3]
        original_mode = image[3] if len(image) == 4 else file_mode(project, name)
        if name not in SURFACES or (read(project, name), file_mode(project, name)) != (before, original_mode):
            raise GuidanceError(f"transaction preimage changed: {name}")
        if before != after:
            mode = original_mode if before is not None else 0o644
            if type(mode) is not int or not 0 <= mode <= 0o777:
                raise GuidanceError(f"unsupported special permission bits; resolve explicitly: {name}")
            changes.append({"path": name, "before": encode(before), "after": encode(after), "mode": mode})
    if not changes:
        verify()
        return False
    lock = next((change for change in planned if change[0] == LOCK), None)
    if lock is None:
        raise GuidanceError("transaction needs an explicit selection lock preimage")
    journal = {"schema": 1, "phase": "applying", "changes": changes,
               "transaction": digest(canonical(changes)),
               "old": digest(lock[1]) if lock[1] is not None else None,
               "new": digest(lock[2]) if lock[2] is not None else None}
    raw = canonical(journal)
    if len(raw) > MAX_TOTAL:
        raise GuidanceError("transaction journal exceeds byte limit")
    save_bytes(project / JOURNAL, raw)
    checkpoint("journal")
    for change in changes:
        before = decode(change["before"])
        mode = change["mode"] if before is not None else None
        if (read(project, change["path"]), file_mode(project, change["path"])) != (before, mode):
            raise GuidanceError(f"transaction preimage changed: {change['path']}")
        write(project, change["path"], decode(change["after"]), change["mode"])
        checkpoint("write:" + change["path"])
    verify()
    journal["phase"] = "committed"
    save_bytes(project / JOURNAL, canonical(journal))
    checkpoint("committed")
    finish(project, journal, "committed")
    return True
