"""Bounded immutable snapshots and local atomic writes; no native integration.

Adapted from audited snapshots/runtime_io primitives; Apache-2.0, see NOTICE.
"""

from contextlib import contextmanager
import ctypes
import fcntl
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import uuid

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


def process_start(pid):
    """Observed process generation, never elapsed lock age. Unknown means refusal."""
    try:
        if sys.platform == "linux":
            # comm may contain spaces/parentheses; fields after its final ')' start
            # at stat field 3. Field 22 is a boot-relative, non-wall-clock tick.
            value = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
            return "linux:" + value if value.isdecimal() else None
        if sys.platform == "darwin":
            class BsdInfo(ctypes.Structure):
                _fields_ = ([("ids", ctypes.c_uint32 * 12), ("comm", ctypes.c_char * 16),
                             ("name", ctypes.c_char * 32), ("details", ctypes.c_uint32 * 5),
                             ("nice", ctypes.c_int32), ("seconds", ctypes.c_uint64),
                             ("microseconds", ctypes.c_uint64)])
            value = BsdInfo()
            libproc = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
            count = libproc.proc_pidinfo(pid, 3, ctypes.c_uint64(0), ctypes.byref(value), ctypes.sizeof(value))
            if count == ctypes.sizeof(value) and value.seconds > 0 and value.microseconds < 1000000:
                return f"darwin:{value.seconds}:{value.microseconds}"
    except (OSError, UnicodeError, ValueError, IndexError):
        return None
    return None


def host_identity():
    """Include machine identity: a shared cache must not trust hostname alone."""
    try:
        machine = Path("/etc/machine-id")
        if machine.is_file():
            identity = machine.read_text().strip()
            # Same machine is not the same PID visibility domain in containers.
            identity += ":" + Path("/proc/sys/kernel/random/boot_id").read_text().strip()
            identity += ":" + os.readlink("/proc/self/ns/pid")
        else:
            output = subprocess.check_output(
                ["/usr/sbin/ioreg", "-rd1", "-c", "IOPlatformExpertDevice"], timeout=5).decode()
            match = re.search(r'"IOPlatformUUID"\s*=\s*"([A-Fa-f0-9-]+)"', output)
            identity = match.group(1) if match else None
        if identity:
            return socket.gethostname() + ":" + identity
    except (OSError, UnicodeError, subprocess.SubprocessError):
        pass
    raise GuidanceError("host identity unavailable; writer lock cannot be verified")


@contextmanager
def lock_guard(directory):
    """Serialize publication/reclamation, including concurrent recoverers."""
    path = checked_path(directory / ".writer-guard")
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise GuidanceError("nonregular writer guard")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def dead_holder(owner):
    fields(owner, ("schema", "pid", "host", "start", "operation", "token"))
    if (type(owner["schema"]) is not int or owner["schema"] != 1 or
            type(owner["pid"]) is not int or owner["pid"] <= 0 or
            not all(isinstance(owner[k], str) and owner[k] for k in
                    ("host", "start", "operation", "token")) or owner["host"] != host_identity()):
        return False
    if not re.fullmatch(r"(?:linux:[0-9]+|darwin:[0-9]+:[0-9]{1,6})", owner["start"]):
        return False
    try:
        os.kill(owner["pid"], 0)
    except ProcessLookupError:
        return True
    except OSError:
        return False
    start = process_start(owner["pid"])
    return start is not None and start != owner["start"]


def clear_lock(lock, expected):
    """Caller holds guard; never remove an unknown or replacement holder."""
    if regular_bytes(lock / "owner.json") != expected or set(p.name for p in lock.iterdir()) != {"owner.json"}:
        raise GuidanceError("writer lock changed; inspect before retry")
    retired = lock.with_name(".lock-retired-" + uuid.uuid4().hex)
    os.rename(lock, retired)
    sync_directory(lock.parent)
    # A cut now leaves inert retained debris, never an empty active writer lock.
    shutil.rmtree(retired)


@contextmanager
def locked(directory, *, operation="prepare", reclaim=False):
    directory = checked_path(directory)
    make_directory(directory)
    lock = checked_path(directory / "writer-lock")
    start = process_start(os.getpid())
    if start is None:
        raise GuidanceError("process identity unavailable; refusing unverifiable writer lock")
    owner = canonical({"schema": 1, "pid": os.getpid(), "host": host_identity(),
                       "start": start, "operation": operation, "token": uuid.uuid4().hex})
    with lock_guard(directory):
        if lock.exists():
            try:
                previous = regular_bytes(lock / "owner.json")
                if not reclaim or not dead_holder(parse_json(previous)):
                    raise GuidanceError("holder is live, foreign or unverifiable")
                clear_lock(lock, previous)
            except (GuidanceError, OSError) as error:
                raise GuidanceError(f"writer lock exists; inspect before retry: {lock}") from error
        # Publish complete metadata, so SIGKILL cannot leave an empty writer lock.
        candidate = Path(tempfile.mkdtemp(prefix=".lock-candidate-", dir=directory))
        try:
            save_bytes(candidate / "owner.json", owner)
            os.rename(candidate, lock)
            sync_directory(directory)
        finally:
            if candidate.exists():
                shutil.rmtree(candidate)
    try:
        sync_directory(directory)
        yield
    finally:
        with lock_guard(directory):
            clear_lock(lock, owner)
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
