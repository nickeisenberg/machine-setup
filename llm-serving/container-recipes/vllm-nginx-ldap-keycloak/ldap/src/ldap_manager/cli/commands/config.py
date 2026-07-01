from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import fields

from ldap_manager.project import Project


def edit_config(project: Project) -> None:
    editor = os.environ.get("EDITOR", "vim")

    subprocess.run(
        [editor, str(project.config_path)],
        check=True,
    )


def register(
    subparsers: argparse._SubParsersAction,
) -> None:
    parser = subparsers.add_parser(
        "config",
        help="Manage project configuration.",
    )

    config_subparsers = parser.add_subparsers(
        dest="config_command",
        required=True,
    )

    list_parser = config_subparsers.add_parser(
        "list",
        help="List configuration.",
    )
    list_parser.set_defaults(func=run)

    edit_parser = config_subparsers.add_parser(
        "edit",
        help="Edit the project configuration.",
    )
    edit_parser.set_defaults(func=run)

    get_parser = config_subparsers.add_parser(
        "get",
        help="Get a configuration value.",
    )
    get_parser.add_argument("key")
    get_parser.set_defaults(func=run)

    set_parser = config_subparsers.add_parser(
        "set",
        help="Set a configuration value.",
    )
    set_parser.add_argument("key")
    set_parser.add_argument("value")
    set_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    project = Project.find()

    match args.config_command:
        case "list":
            print_config(project)

        case "get":
            print(get_config_value(project, args.key))

        case "set":
            set_config_value(
                project,
                args.key,
                args.value,
            )
            project.save()

        case "edit":
            edit_config(project)


def print_config(project: Project) -> None:
    for section in fields(project.config):
        print(f"[{section.name}]")

        obj = getattr(project.config, section.name)

        for option in fields(obj):
            value = getattr(obj, option.name)
            print(f"{option.name} = {value}")

        print()


def get_config_value(
    project: Project,
    key: str,
) -> str:
    section, option = key.split(".", 1)

    return getattr(
        getattr(project.config, section),
        option,
    )


def set_config_value(
    project: Project,
    key: str,
    value: str,
) -> None:
    section, option = key.split(".", 1)

    setattr(
        getattr(project.config, section),
        option,
        value,
    )
