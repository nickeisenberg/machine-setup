from __future__ import annotations

import argparse


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "status",
        help="Display project status.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    print("TODO: status")
