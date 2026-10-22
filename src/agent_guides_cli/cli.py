"""Exact Git preparation, project-local lifecycle and host evidence commands."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version
from pathlib import Path
import sys

from .integrity import GuidanceError, canonical, identifier, parse_json, regular_bytes
from . import git_source, lifecycle, preparation, task_identity


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-guides-cli",
        description=(
            "Neutral guidance preparation and explicit project-local native connection."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('agent-guides-cli')}"
    )
    commands = parser.add_subparsers(dest="command")
    prepare = commands.add_parser("prepare", help="resolve approved sources once and prepare bundles")
    prepare.add_argument("--request", type=Path, required=True)
    restore = commands.add_parser("restore", help="restore exact recorded data, offline only")
    restore.add_argument("--lock", type=Path, required=True)
    restore.add_argument("--expected", required=True, help="independently retained selection SHA-256")
    restore.add_argument("--current", help="expected existing selection when restoring a connected lock")
    restore.add_argument("--host-config", type=Path, help="approved external read-only managed JSON; never edited")
    for command in (prepare, restore):
        command.add_argument("--project", type=Path, required=True)
        command.add_argument("--cache", type=Path)
    install = commands.add_parser("install", help="prepare and connect selected clients in one operation")
    install.add_argument("--request", type=Path, required=True)
    install.add_argument("--client", choices=("claude", "opencode"), action="append", required=True)
    install.add_argument("--expected", help="expected existing selection, if any")
    install.add_argument("--host-config", type=Path, help="approved external read-only managed JSON; never edited")
    update = commands.add_parser("update", help="explicitly update the recorded selection and connection")
    for command in (install, update):
        command.add_argument("--project", type=Path, required=True)
        command.add_argument("--cache", type=Path)
    update.add_argument("--expected", required=True)
    for command in (prepare, install, update):
        command.add_argument("--mirror", action="append", default=[], metavar="SOURCE=PATH",
                             help="resolve/fetch that source from an operator-maintained local Git copy")
    remove = commands.add_parser("remove", help="remove only owned integration; retain lock and content")
    status = commands.add_parser("status", help="offline integrity and connection status; no repair")
    recovery = commands.add_parser("recover", help="recover interrupted writes without overwriting unknown edits")
    recovery.add_argument("--project", type=Path, required=True)
    recovery.add_argument("--cache", type=Path, help="original cache if external; only provably dead local locks are cleared")
    verify = commands.add_parser("verify", help="compare local content and connection with expected identity")
    capture = commands.add_parser("task-pin", help="retain host task identity once outside generated storage")
    for command in (verify, capture, remove, status):
        command.add_argument("--project", type=Path, required=True)
        command.add_argument("--expected", required=True)
    capture.add_argument("--output", type=Path, required=True)
    capture.add_argument("--policy", action="append", default=[])
    capture.add_argument("--overlay", action="append", default=[])
    join = commands.add_parser("task-join", help="compare reviewer identity with retained host evidence")
    join.add_argument("--project", type=Path, required=True)
    join.add_argument("--identity", type=Path, required=True)
    join.add_argument("--expected-task", required=True)
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        mirrors = _mirrors(getattr(args, "mirror", []))
        if args.command == "prepare":
            result = preparation.prepare(args.project, parse_json(regular_bytes(args.request)), args.cache,
                                         fixtures=mirrors)
        elif args.command == "restore":
            raw = regular_bytes(args.lock)
            if "connection" in preparation.read_lock(raw, args.expected):
                result = lifecycle.restore(args.project, raw, args.expected, args.cache,
                                           current=args.current, host_config=args.host_config)
            else:
                if args.current is not None or args.host_config is not None:
                    raise GuidanceError("--current/--host-config apply only to connected restore")
                result = preparation.restore(args.project, raw, args.expected, args.cache)
        elif args.command == "install":
            result = lifecycle.install(args.project, parse_json(regular_bytes(args.request)), args.client,
                                       args.cache, expected=args.expected, host_config=args.host_config,
                                       fixtures=mirrors)
        elif args.command == "update":
            result = lifecycle.update(args.project, args.expected, args.cache, fixtures=mirrors)
        elif args.command == "remove":
            result = lifecycle.remove(args.project, args.expected)
        elif args.command == "recover":
            result = lifecycle.recover(args.project, args.cache)
        elif args.command == "status":
            result = lifecycle.verify(args.project, args.expected)
        elif args.command == "verify":
            result = preparation.verify(args.project, args.expected)
        elif args.command == "task-pin":
            value = task_identity.capture(args.project, args.expected, args.policy, args.overlay)
            result = {"task": task_identity.retain(args.output, value, args.project), "selection": args.expected}
        else:
            result = task_identity.join(args.project, regular_bytes(args.identity), args.expected_task)
        print(canonical(result).decode(), end="")
    except (GuidanceError, OSError) as error:
        print(f"agent-guides-cli: {error}", file=sys.stderr)
        return 1
    return 0


def _mirrors(values):
    """Parse repeated SOURCE=PATH; None keeps the default HTTPS transport."""
    if not values:
        return None
    mirrors = git_source.Mirrors()
    for value in values:
        source, separator, path = value.partition("=")
        if not separator or not path:
            raise GuidanceError("--mirror expects SOURCE=PATH")
        if identifier(source) in mirrors:
            raise GuidanceError(f"duplicate mirror: {source}")
        mirrors[source] = Path(path)
    return mirrors
