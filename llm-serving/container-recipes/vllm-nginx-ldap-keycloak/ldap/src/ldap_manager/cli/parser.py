from __future__ import annotations

import argparse

from ldap_manager.cli.commands import (
    add_group,
    add_user,
    config,
    init,
    status,
    sync,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ldapman",
    )

    subparsers = parser.add_subparsers(
        required=True,
    )

    init.register(subparsers)
    config.register(subparsers)
    add_user.register(subparsers)
    add_group.register(subparsers)
    sync.register(subparsers)
    status.register(subparsers)

    return parser
