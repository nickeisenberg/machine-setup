from __future__ import annotations

import argparse


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "sync",
        help="Synchronize the database with LDAP.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    print("TODO: sync")
