from __future__ import annotations

import argparse


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "add-group",
        help="Add a group.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    print("TODO: add-group")
