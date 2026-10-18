"""Non-activating exact Git preparation and host evidence commands."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version
from pathlib import Path
import sys

from .integrity import GuidanceError, canonical, parse_json, regular_bytes
from . import preparation, task_identity


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-guides",
        description=(
            "Neutral guidance preparation. No native connection or consumer activation."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('agent-guides')}"
    )
    commands = parser.add_subparsers(dest="command")
    prepare = commands.add_parser("prepare", help="resolve approved sources once and prepare bundles")
    prepare.add_argument("--request", type=Path, required=True)
    restore = commands.add_parser("restore", help="restore exact recorded data, offline only")
    restore.add_argument("--lock", type=Path, required=True)
    restore.add_argument("--expected", required=True, help="independently retained selection SHA-256")
    for command in (prepare, restore):
        command.add_argument("--project", type=Path, required=True)
        command.add_argument("--cache", type=Path)
    verify = commands.add_parser("verify", help="compare prepared bytes with expected selection identity")
    capture = commands.add_parser("task-pin", help="retain host task identity once outside generated storage")
    for command in (verify, capture):
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
        if args.command == "prepare":
            result = preparation.prepare(args.project, parse_json(regular_bytes(args.request)), args.cache)
        elif args.command == "restore":
            result = preparation.restore(args.project, regular_bytes(args.lock), args.expected, args.cache)
        elif args.command == "verify":
            result = preparation.verify(args.project, args.expected)
        elif args.command == "task-pin":
            value = task_identity.capture(args.project, args.expected, args.policy, args.overlay)
            result = {"task": task_identity.retain(args.output, value, args.project), "selection": args.expected}
        else:
            result = task_identity.join(args.project, regular_bytes(args.identity), args.expected_task)
        print(canonical(result).decode(), end="")
    except (GuidanceError, OSError) as error:
        print(f"agent-guides: {error}", file=sys.stderr)
        return 1
    return 0
