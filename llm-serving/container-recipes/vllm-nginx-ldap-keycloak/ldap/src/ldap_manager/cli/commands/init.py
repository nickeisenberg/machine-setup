from __future__ import annotations

import argparse

from ldap_manager.project import Project


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "init",
        help="Initialize a new ldapman project.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    Project.initialize()
    print("Initialized ldapman project.")
