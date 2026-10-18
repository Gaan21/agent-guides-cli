"""Identity/help entry point for the bootstrap package."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-guides",
        description=(
            "Neutral guidance delivery tooling (development scaffold). "
            "Only help and version are available; preparation and integration "
            "operations are not implemented yet."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('agent-guides')}"
    )
    parser.parse_args(argv)
    parser.print_help()
    return 0
