from __future__ import annotations

import sqlite3

from sqlalchemy import select

from ldap_manager.models import Group
from ldap_manager.project import (
    CONFIG_FILE,
    DATABASE_FILE,
    PROJECT_DIRECTORY,
    VERSION_FILE,
    Project,
)


def test_initialize_creates_project(project: Project) -> None:
    project_directory = project.directory

    assert project_directory.is_dir()

    assert (project_directory / CONFIG_FILE).is_file()
    assert (project_directory / VERSION_FILE).is_file()
    assert (project_directory / DATABASE_FILE).is_file()


def test_initialize_writes_version(project: Project) -> None:
    version = project.version_path.read_text().strip()

    assert version == "1"


def test_initialize_writes_database_url(project: Project) -> None:
    assert project.config.database.url.startswith("sqlite:///")


def test_find_project(project: Project) -> None:
    found = Project.find(project.root)

    assert found.root == project.root
    assert found.directory == project.directory


def test_find_project_from_subdirectory(project: Project) -> None:
    subdirectory = project.root / "a" / "b" / "c"
    subdirectory.mkdir(parents=True)

    found = Project.find(subdirectory)

    assert found.root == project.root


def test_find_outside_project(tmp_path) -> None:
    try:
        Project.find(tmp_path)
    except RuntimeError:
        pass
    else:
        assert False, "Expected RuntimeError."


def test_database_created(project: Project) -> None:
    database_path = project.directory / DATABASE_FILE

    connection = sqlite3.connect(database_path)

    tables = {
        row[0]
        for row in connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        )
    }

    connection.close()

    assert "users" in tables
    assert "groups" in tables
    assert "user_groups" in tables


def test_default_groups_exist(database) -> None:
    with database.session() as session:
        groups = list(session.scalars(select(Group).order_by(Group.name)))

    assert [group.name for group in groups] == [
        "general",
        "vip",
    ]
