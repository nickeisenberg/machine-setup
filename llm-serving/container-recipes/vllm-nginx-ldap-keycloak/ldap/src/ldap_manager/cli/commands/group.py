from __future__ import annotations

import argparse

from ldap_manager.managers.group_manager import GroupManager
from ldap_manager.project import Project


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "group",
        help="Manage groups.",
    )

    group_subparsers = parser.add_subparsers(
        dest="group_command",
        required=True,
    )

    #
    # ldapman group add <name>
    #
    add_parser = group_subparsers.add_parser(
        "add",
        help="Add a new group.",
    )
    add_parser.add_argument(
        "name",
        help="Group name.",
    )
    add_parser.add_argument(
        "-d",
        "--description",
        default="",
        help="Optional group description.",
    )
    add_parser.set_defaults(func=run)

    #
    # ldapman group remove <name>
    #
    remove_parser = group_subparsers.add_parser(
        "remove",
        help="Remove a group.",
    )
    remove_parser.add_argument(
        "name",
        help="Group name.",
    )
    remove_parser.set_defaults(func=run)

    #
    # ldapman group rename <old> <new>
    #
    rename_parser = group_subparsers.add_parser(
        "rename",
        help="Rename a group.",
    )
    rename_parser.add_argument(
        "old_name",
        help="Current group name.",
    )
    rename_parser.add_argument(
        "new_name",
        help="New group name.",
    )
    rename_parser.set_defaults(func=run)

    #
    # ldapman group list
    #
    list_parser = group_subparsers.add_parser(
        "list",
        help="List all groups.",
    )
    list_parser.set_defaults(func=run)

    #
    # ldapman group show <name>
    #
    show_parser = group_subparsers.add_parser(
        "show",
        help="Show group details.",
    )
    show_parser.add_argument(
        "name",
        help="Group name.",
    )
    show_parser.set_defaults(func=run)

    #
    # ldapman group add-user <group> <user>
    #
    add_user_parser = group_subparsers.add_parser(
        "add-user",
        help="Add a user to a group.",
    )
    add_user_parser.add_argument(
        "group",
        help="Group name.",
    )
    add_user_parser.add_argument(
        "user",
        help="User UID.",
    )
    add_user_parser.set_defaults(func=run)

    #
    # ldapman group remove-user <group> <user>
    #
    remove_user_parser = group_subparsers.add_parser(
        "remove-user",
        help="Remove a user from a group.",
    )
    remove_user_parser.add_argument(
        "group",
        help="Group name.",
    )
    remove_user_parser.add_argument(
        "user",
        help="User UID.",
    )
    remove_user_parser.set_defaults(func=run)

    #
    # ldapman group list-users <group>
    #
    list_users_parser = group_subparsers.add_parser(
        "list-users",
        help="List users in a group.",
    )
    list_users_parser.add_argument(
        "group",
        help="Group name.",
    )
    list_users_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    project = Project.find()
    manager = GroupManager(project.database)

    match args.group_command:
        case "add":
            manager.add(
                name=args.name,
                description=args.description,
            )
            print(f"Added group '{args.name}'.")

        case "remove":
            manager.remove(args.name)
            print(f"Removed group '{args.name}'.")

        case "rename":
            manager.rename(
                old_name=args.old_name,
                new_name=args.new_name,
            )
            print(f"Renamed group '{args.old_name}' -> '{args.new_name}'.")

        case "list":
            for group in manager.list():
                print(group.name)

        case "show":
            group = manager.get(args.name)

            print(f"Name        : {group.name}")
            print(f"Description : {group.description or ''}")
            print(f"DN          : {group.dn}")

            print("Users:")

            if not group.users:
                print("  (none)")
            else:
                for user in group.users:
                    print(f"  {user.uid:<16}{user.name}")

        case "add-user":
            manager.add_user(
                group_name=args.group,
                user_uid=args.user,
            )
            print(f"Added user '{args.user}' to group '{args.group}'.")

        case "remove-user":
            manager.remove_user(
                group_name=args.group,
                user_uid=args.user,
            )
            print(f"Removed user '{args.user}' from group '{args.group}'.")

        case "list-users":
            users = manager.list_users(args.group)

            if not users:
                print("(none)")
            else:
                for user in users:
                    print(f"{user.uid:<16}{user.name}")
