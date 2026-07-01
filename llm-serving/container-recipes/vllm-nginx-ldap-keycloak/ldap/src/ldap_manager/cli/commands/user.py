from __future__ import annotations

import argparse

from ldap_manager.managers.user_manager import UserManager
from ldap_manager.project import Project


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "user",
        help="Manage users.",
    )

    user_subparsers = parser.add_subparsers(
        dest="user_command",
        required=True,
    )

    #
    # ldapman user add
    #
    add_parser = user_subparsers.add_parser(
        "add",
        help="Add a new user.",
    )
    add_parser.add_argument("uid")
    add_parser.add_argument("first_name")
    add_parser.add_argument("last_name")
    add_parser.add_argument("email")
    add_parser.add_argument("password")
    add_parser.set_defaults(func=run)

    #
    # ldapman user remove
    #
    remove_parser = user_subparsers.add_parser(
        "remove",
        help="Remove a user.",
    )
    remove_parser.add_argument("uid")
    remove_parser.set_defaults(func=run)

    #
    # ldapman user update
    #
    update_parser = user_subparsers.add_parser(
        "update",
        help="Update a user.",
    )
    update_parser.add_argument("uid")
    update_parser.add_argument("--first-name")
    update_parser.add_argument("--last-name")
    update_parser.add_argument("--email")
    update_parser.add_argument("--password")

    enabled = update_parser.add_mutually_exclusive_group()
    enabled.add_argument(
        "--enable",
        action="store_true",
    )
    enabled.add_argument(
        "--disable",
        action="store_true",
    )

    update_parser.set_defaults(func=run)

    #
    # ldapman user list
    #
    list_parser = user_subparsers.add_parser(
        "list",
        help="List all users.",
    )
    list_parser.set_defaults(func=run)

    #
    # ldapman user show
    #
    show_parser = user_subparsers.add_parser(
        "show",
        help="Show user details.",
    )
    show_parser.add_argument("uid")
    show_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    project = Project.find()
    manager = UserManager(project.database)

    match args.user_command:
        case "add":
            manager.add(
                uid=args.uid,
                first_name=args.first_name,
                last_name=args.last_name,
                email=args.email,
                password=args.password,
            )

            print(f"Added user '{args.uid}'.")

        case "remove":
            manager.remove(args.uid)

            print(f"Removed user '{args.uid}'.")

        case "update":
            enabled = None

            if args.enable:
                enabled = True
            elif args.disable:
                enabled = False

            manager.update(
                args.uid,
                first_name=args.first_name,
                last_name=args.last_name,
                email=args.email,
                password=args.password,
                enabled=enabled,
            )

            print(f"Updated user '{args.uid}'.")

        case "list":
            users = manager.list()

            if not users:
                print("No users.")
                return

            print(f"{'UID':<16} {'Name':<30} {'Enabled'}")
            print("-" * 60)

            for user in users:
                print(
                    f"{user.uid:<16}"
                    f"{user.cn:<30}"
                    f"{'Yes' if user.enabled else 'No'}"
                )

        case "show":
            user = manager.get(args.uid)

            print(f"UID        : {user.uid}")
            print(f"Name       : {user.cn}")
            print(f"Email      : {user.email}")
            print(f"Enabled    : {'Yes' if user.enabled else 'No'}")
            print(f"DN         : {user.dn}")

            print("Groups:")

            if not user.groups:
                print("  (none)")
            else:
                for group in user.groups:
                    print(f"  {group.name}")
