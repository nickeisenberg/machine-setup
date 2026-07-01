from __future__ import annotations

import argparse

from ldap_manager.project import Project


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    parser = subparsers.add_parser(
        "ldap",
        help="Inspect the configured LDAP directory.",
    )

    ldap_subparsers = parser.add_subparsers(
        required=True,
    )

    user = ldap_subparsers.add_parser(
        "user",
        help="LDAP users.",
    )

    user_subparsers = user.add_subparsers(
        required=True,
    )

    list_parser = user_subparsers.add_parser(
        "list",
        help="List LDAP users.",
    )
    list_parser.set_defaults(func=list_users)

    show_parser = user_subparsers.add_parser(
        "show",
        help="Show an LDAP user.",
    )
    show_parser.add_argument("uid")
    show_parser.set_defaults(func=show_user)

    group = ldap_subparsers.add_parser(
        "group",
        help="LDAP groups.",
    )

    group_subparsers = group.add_subparsers(
        required=True,
    )

    list_parser = group_subparsers.add_parser(
        "list",
        help="List LDAP groups.",
    )
    list_parser.set_defaults(func=list_groups)

    show_parser = group_subparsers.add_parser(
        "show",
        help="Show an LDAP group.",
    )
    show_parser.add_argument("name")
    show_parser.set_defaults(func=show_group)


def list_users(args) -> None:
    project = Project.find()

    users = project.ldap_directory.list_users()

    if not users:
        print("No users.")
        return

    for user in users:
        print(user.uid)


def show_user(args) -> None:
    project = Project.find()

    user = project.ldap_directory.get_user(args.uid)

    if user is None:
        raise RuntimeError(f"User '{args.uid}' does not exist.")

    print(f"UID        : {user.uid}")
    print(f"Name       : {user.cn}")
    print(f"Email      : {user.email}")
    print(f"Enabled    : {'Yes' if user.enabled else 'No'}")
    print(f"DN         : {user.dn}")

    print("Groups:")
    if user.groups:
        for group in user.groups:
            print(f"  {group.name}")
    else:
        print("  (none)")


def list_groups(args) -> None:
    project = Project.find()

    groups = project.ldap_directory.list_groups()

    if not groups:
        print("No groups.")
        return

    for group in groups:
        print(group.name)


def show_group(args) -> None:
    project = Project.find()

    group = project.ldap_directory.get_group(args.name)

    if group is None:
        raise RuntimeError(f"Group '{args.name}' does not exist.")

    print(f"Name        : {group.name}")
    print(f"Description : {group.description or ''}")
    print(f"DN          : {group.dn}")

    print("Users:")
    if group.users:
        for user in group.users:
            print(f"  {user.uid}")
    else:
        print("  (none)")
