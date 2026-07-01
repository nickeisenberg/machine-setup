from __future__ import annotations

import argparse

from ldap_manager.cli.commands import (
    config,
    group,
    init,
    ldap,
    status,
    sync,
    user,
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
    user.register(subparsers)
    group.register(subparsers)
    sync.register(subparsers)
    ldap.register(subparsers)
    status.register(subparsers)

    return parser
