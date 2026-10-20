"""Bounded immutable snapshots and local atomic writes; no native integration.

Adapted from audited snapshots/runtime_io primitives; Apache-2.0, see NOTICE.
"""

from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import stat
import tempfile

from .integrity import (GuidanceError, MAX_TOTAL, canonical, checked_path, digest,
                        fields, inventory, parse_json, regular_bytes, require_digest)


def sync_directory(path):
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def make_directory(path):
    """Make each missing directory durable in its parent; reject path aliases."""
    path = checked_path(path)
    if path.is_dir():
        return
    if path.exists():
        raise GuidanceError(f"expected directory: {path}")
    make_directory(path.parent)
    try:
        path.mkdir()
    except FileExistsError:
        if not checked_path(path).is_dir():
            raise GuidanceError(f"expected directory: {path}")
    sync_directory(path.parent)


def save_bytes(path, content, *, mode=0o600):
    path = checked_path(path)
    descriptor, temporary = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def locked(directory):
    directory = checked_path(directory)
    make_directory(directory)
    lock = checked_path(directory / "writer-lock")
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise GuidanceError(f"writer lock exists; inspect before retry: {lock}") from error
    try:
        sync_directory(directory)
        yield
    finally:
        lock.rmdir()
        sync_directory(directory)


def verify_snapshot(path, expected):
    path = checked_path(path)
    require_digest(expected)
    raw = regular_bytes(path / "manifest.json")
    if digest(raw) != expected:
        raise GuidanceError("snapshot manifest identity mismatch")
    manifest = parse_json(raw)
    fields(manifest, ("schema", "metadata", "files"))
    if type(manifest["schema"]) is not int or manifest["schema"] != 1 or canonical(manifest) != raw:
        raise GuidanceError("invalid snapshot schema or encoding")
    if not isinstance(manifest["metadata"], dict) or not isinstance(manifest["files"], dict):
        raise GuidanceError("invalid snapshot metadata/inventory")
    inventory(list(manifest["files"]) + ["manifest.json"])
    files, directories, total = {}, set(), 0
    for name, expected_hash in manifest["files"].items():
        content = regular_bytes(path / name)
        total += len(content)
        if total > MAX_TOTAL or digest(content) != require_digest(expected_hash):
            raise GuidanceError(f"snapshot content mismatch or size limit: {name}")
        files[name] = content
        directories.update(str(p) for p in Path(name).parents if str(p) != ".")
    actual_files, actual_directories = set(), set()
    for entry in path.rglob("*"):
        checked_path(entry)
        name = entry.relative_to(path).as_posix()
        mode = entry.stat().st_mode
        if stat.S_ISDIR(mode):
            actual_directories.add(name)
        elif stat.S_ISREG(mode):
            actual_files.add(name)
        else:
            raise GuidanceError("nonregular snapshot entry")
        if len(actual_files) + len(actual_directories) > 4096:
            raise GuidanceError("snapshot inventory limit")
    if actual_files != set(files) | {"manifest.json"} or actual_directories != directories:
        raise GuidanceError("unexpected snapshot inventory")
    return manifest["metadata"], files


def write_snapshot(parent, files, metadata):
    parent = checked_path(parent)
    make_directory(parent)
    inventory(list(files) + ["manifest.json"])
    if sum(map(len, files.values())) > MAX_TOTAL:
        raise GuidanceError("snapshot size limit")
    manifest = {"schema": 1, "metadata": metadata,
                "files": {name: digest(data) for name, data in sorted(files.items())}}
    identity = digest(canonical(manifest))
    target = checked_path(parent / identity)
    if target.exists():
        verify_snapshot(target, identity)
        return identity
    temporary = Path(tempfile.mkdtemp(prefix=".candidate-", dir=parent))
    try:
        for name, content in files.items():
            output = checked_path(temporary / name)
            make_directory(output.parent)
            save_bytes(output, content)
            output.chmod(0o444)
        save_bytes(temporary / "manifest.json", canonical(manifest))
        (temporary / "manifest.json").chmod(0o444)
        verify_snapshot(temporary, identity)
        os.rename(temporary, target)
        sync_directory(parent)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return identity
