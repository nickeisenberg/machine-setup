from __future__ import annotations

import pytest

from ldap_manager.managers.group_manager import GroupManager
from ldap_manager.managers.user_manager import UserManager


@pytest.fixture
def user(user_manager: UserManager):
    return user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )


def test_default_groups_exist(group_manager: GroupManager) -> None:
    groups = group_manager.list()

    assert [g.name for g in groups] == [
        "general",
        "vip",
    ]


def test_add_group(group_manager: GroupManager) -> None:
    group = group_manager.add(
        "engineering",
        "Engineering Group",
    )

    assert group.name == "engineering"
    assert group.description == "Engineering Group"
    assert group.users == []


def test_add_duplicate_group(group_manager: GroupManager) -> None:
    group_manager.add("engineering")

    with pytest.raises(ValueError):
        group_manager.add("engineering")


def test_remove_group(group_manager: GroupManager) -> None:
    group_manager.add("engineering")

    group_manager.remove("engineering")

    with pytest.raises(ValueError):
        group_manager.get("engineering")


def test_remove_missing_group(group_manager: GroupManager) -> None:
    with pytest.raises(ValueError):
        group_manager.remove("engineering")


def test_rename_group(group_manager: GroupManager) -> None:
    group_manager.add("engineering")

    group = group_manager.rename(
        "engineering",
        "dev",
    )

    assert group.name == "dev"

    with pytest.raises(ValueError):
        group_manager.get("engineering")

    assert group_manager.get("dev").name == "dev"


def test_rename_missing_group(group_manager: GroupManager) -> None:
    with pytest.raises(ValueError):
        group_manager.rename(
            "engineering",
            "dev",
        )


def test_rename_duplicate_group(group_manager: GroupManager) -> None:
    group_manager.add("engineering")
    group_manager.add("dev")

    with pytest.raises(ValueError):
        group_manager.rename(
            "engineering",
            "dev",
        )


def test_get_group(group_manager: GroupManager) -> None:
    group_manager.add(
        "engineering",
        "Engineering",
    )

    group = group_manager.get("engineering")

    assert group.name == "engineering"
    assert group.description == "Engineering"
    assert group.users == []


def test_get_missing_group(group_manager: GroupManager) -> None:
    with pytest.raises(ValueError):
        group_manager.get("engineering")


def test_list_groups(group_manager: GroupManager) -> None:
    group_manager.add("engineering")
    group_manager.add("admins")

    groups = group_manager.list()

    assert [g.name for g in groups] == [
        "admins",
        "engineering",
        "general",
        "vip",
    ]


def test_add_user_to_group(
    group_manager: GroupManager,
    user,
) -> None:
    group = group_manager.add_user(
        "general",
        "eisenbnt",
    )

    assert len(group.users) == 1
    assert group.users[0].uid == "eisenbnt"


def test_add_user_twice(
    group_manager: GroupManager,
    user,
) -> None:
    group_manager.add_user(
        "general",
        "eisenbnt",
    )

    with pytest.raises(ValueError):
        group_manager.add_user(
            "general",
            "eisenbnt",
        )


def test_add_missing_user(
    group_manager: GroupManager,
) -> None:
    with pytest.raises(ValueError):
        group_manager.add_user(
            "general",
            "bob",
        )


def test_add_user_to_missing_group(
    group_manager: GroupManager,
    user,
) -> None:
    with pytest.raises(ValueError):
        group_manager.add_user(
            "engineering",
            "eisenbnt",
        )


def test_remove_user_from_group(
    group_manager: GroupManager,
    user,
) -> None:
    group_manager.add_user(
        "general",
        "eisenbnt",
    )

    group = group_manager.remove_user(
        "general",
        "eisenbnt",
    )

    assert group.users == []


def test_remove_user_not_in_group(
    group_manager: GroupManager,
    user,
) -> None:
    with pytest.raises(ValueError):
        group_manager.remove_user(
            "general",
            "eisenbnt",
        )


def test_remove_missing_user(
    group_manager: GroupManager,
) -> None:
    with pytest.raises(ValueError):
        group_manager.remove_user(
            "general",
            "bob",
        )


def test_remove_user_from_missing_group(
    group_manager: GroupManager,
    user,
) -> None:
    with pytest.raises(ValueError):
        group_manager.remove_user(
            "engineering",
            "eisenbnt",
        )


def test_list_users(
    group_manager: GroupManager,
    user,
) -> None:
    group_manager.add_user(
        "general",
        "eisenbnt",
    )

    users = group_manager.list_users("general")

    assert len(users) == 1
    assert users[0].uid == "eisenbnt"
    assert users[0].name == "Nicholas Eisenberg"


def test_list_users_empty(
    group_manager: GroupManager,
) -> None:
    users = group_manager.list_users("general")

    assert users == []
