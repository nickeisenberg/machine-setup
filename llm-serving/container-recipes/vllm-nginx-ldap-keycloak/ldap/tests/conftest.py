from __future__ import annotations

from pathlib import Path

import pytest

from ldap_manager.managers.group_manager import GroupManager
from ldap_manager.managers.user_manager import UserManager
from ldap_manager.project import Project


@pytest.fixture
def project(tmp_path: Path) -> Project:
    """
    Create a brand-new ldapman project in a temporary directory.
    """

    return Project.initialize(tmp_path)


@pytest.fixture
def database(project: Project):
    """
    Database associated with the temporary project.
    """

    return project.database


@pytest.fixture
def group_manager(database) -> GroupManager:
    """
    Group manager backed by the temporary database.
    """

    return GroupManager(database)


@pytest.fixture
def user_manager(database) -> UserManager:
    """
    User manager backed by the temporary database.
    """

    return UserManager(database)
