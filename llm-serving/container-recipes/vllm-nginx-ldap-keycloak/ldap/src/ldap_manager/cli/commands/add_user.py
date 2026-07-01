from __future__ import annotations

import argparse


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "add-user",
        help="Add a user.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    print("TODO: add-user")
