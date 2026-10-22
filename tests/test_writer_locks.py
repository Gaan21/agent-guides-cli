"""Dead-holder recovery is explicit, identity based and independent of lock age."""

import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from agent_guides_cli import lifecycle, storage
from agent_guides_cli.integrity import GuidanceError, canonical, parse_json


class WriterLockTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name).resolve()
        self.directory = self.project / ".guidance"

    def owner(self):
        return {"schema": 1, "pid": os.getpid(), "host": storage.host_identity(),
                "start": storage.process_start(os.getpid()), "operation": "update", "token": "test"}

    def abandoned(self, owner):
        lock = self.directory / "writer-lock"
        lock.mkdir(parents=True)
        (lock / "owner.json").write_bytes(canonical(owner))
        return lock

    def test_live_lock_never_reclaimed_even_with_old_mtime(self):
        lock = self.abandoned(self.owner())
        os.utime(lock, (1, 1))
        with self.assertRaisesRegex(GuidanceError, "inspect before retry"):
            lifecycle.recover(self.project)
        self.assertTrue(lock.exists())

    def test_foreign_and_unknown_metadata_preserved(self):
        owner = self.owner()
        owner["host"] = "another-host"
        lock = self.abandoned(owner)
        with self.assertRaises(GuidanceError):
            lifecycle.recover(self.project)
        (lock / "owner.json").write_bytes(b"invalid")
        with self.assertRaises(GuidanceError):
            lifecycle.recover(self.project)
        self.assertTrue(lock.exists())

    def test_unknown_process_lookup_and_permission_denial_refuse(self):
        owner = self.owner()
        with patch.object(storage, "process_start", return_value=None):
            self.assertFalse(storage.dead_holder(owner))
        with patch.object(storage.os, "kill", side_effect=PermissionError):
            self.assertFalse(storage.dead_holder(owner))

    def test_pid_generation_mismatch_is_dead_but_same_generation_is_not(self):
        owner = self.owner()
        with patch.object(storage, "process_start", return_value="different generation"):
            self.assertTrue(storage.dead_holder(owner))
        self.assertFalse(storage.dead_holder(owner))

    def test_generation_does_not_depend_on_timezone_and_malformed_is_unknown(self):
        before = storage.process_start(os.getpid())
        with patch.dict(os.environ, {"TZ": "Pacific/Honolulu"}):
            self.assertEqual(storage.process_start(os.getpid()), before)
        owner = dict(self.owner(), start="not a generation")
        with patch.object(storage.os, "kill", side_effect=ProcessLookupError):
            self.assertFalse(storage.dead_holder(owner))

    def test_cut_after_retirement_does_not_leave_active_empty_lock(self):
        with self.assertRaisesRegex(OSError, "cut"):
            with patch.object(storage.shutil, "rmtree", side_effect=OSError("cut")):
                with storage.locked(self.directory):
                    pass
        self.assertFalse((self.directory / "writer-lock").exists())
        self.assertEqual(len(list(self.directory.glob(".lock-retired-*"))), 1)
        lifecycle.recover(self.project)

    def test_concurrent_recoverers_do_not_delete_successor_lock(self):
        script = """
import sys, time
from pathlib import Path
from agent_guides_cli.storage import locked
with locked(Path(sys.argv[1]), operation='recover', reclaim=True):
    print('acquired', flush=True)
    sys.stdin.read()
"""
        with subprocess.Popen([sys.executable, "-I", "-c", script, str(self.directory)],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as first:
            try:
                self.assertEqual(first.stdout.readline().strip(), "acquired")
                with self.assertRaisesRegex(GuidanceError, "inspect before retry"):
                    lifecycle.recover(self.project)
                owner = parse_json((self.directory / "writer-lock/owner.json").read_bytes())
                self.assertEqual(owner["pid"], first.pid)
            finally:
                first.stdin.close()
                first.wait(timeout=10)
        lifecycle.recover(self.project)

    def test_symlink_metadata_is_not_followed(self):
        lock = self.directory / "writer-lock"
        lock.mkdir(parents=True)
        outside = self.project / "outside.json"
        outside.write_bytes(canonical(self.owner()))
        (lock / "owner.json").symlink_to(outside)
        with self.assertRaises(GuidanceError):
            lifecycle.recover(self.project)
        self.assertTrue(outside.exists())

    def test_successor_metadata_not_removed_on_release(self):
        with self.assertRaisesRegex(GuidanceError, "lock changed"):
            with storage.locked(self.directory):
                (self.directory / "writer-lock/owner.json").write_bytes(canonical(self.owner()))
        self.assertTrue((self.directory / "writer-lock").exists())

    def test_sigkill_both_locks_recovered_without_manual_removal(self):
        cache = self.project / "external-cache"
        script = """
import sys
from pathlib import Path
from agent_guides_cli.storage import locked
with locked(Path(sys.argv[1]), operation='update'):
    with locked(Path(sys.argv[2]), operation='fetch'):
        print('ready', flush=True)
        sys.stdin.read()
"""
        process = subprocess.Popen([sys.executable, "-I", "-c", script,
                                    str(self.directory), str(cache)],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.poll() is None and process.kill())
        self.assertEqual(process.stdout.readline().strip(), "ready")
        metadata = parse_json((cache / "writer-lock/owner.json").read_bytes())
        self.assertEqual(metadata["operation"], "fetch")
        os.kill(process.pid, signal.SIGKILL)
        process.wait(timeout=10)
        process.stdin.close()
        process.stdout.close()
        self.assertEqual(lifecycle.recover(self.project, cache)["recovered"], False)
        lifecycle.recover(self.project, cache)
        self.assertFalse((cache / "writer-lock").exists())
        self.assertFalse((self.directory / "writer-lock").exists())
