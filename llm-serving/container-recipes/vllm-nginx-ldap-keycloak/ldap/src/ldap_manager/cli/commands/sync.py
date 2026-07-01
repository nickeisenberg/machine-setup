from __future__ import annotations

import argparse

from ldap_manager.project import Project
from ldap_manager.sync import Sync


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    parser = subparsers.add_parser(
        "sync",
        help="Synchronize the local database to the LDAP directory.",
    )

    parser.set_defaults(func=sync)


def sync(args: argparse.Namespace) -> None:
    project = Project.find()

    Sync(
        database=project.database,
        directory=project.ldap_directory,
    ).sync()

    print("Synchronization complete.")
