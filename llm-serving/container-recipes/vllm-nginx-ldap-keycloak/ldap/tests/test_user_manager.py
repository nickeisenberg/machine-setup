from __future__ import annotations

import pytest

from ldap_manager.managers.group_manager import GroupManager
from ldap_manager.managers.user_manager import UserManager


def test_add_user(user_manager: UserManager) -> none:
    user = user_manager.add(
        uid="eisenbnt",
        first_name="nicholas",
        last_name="eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    assert user.uid == "eisenbnt"
    assert user.first_name == "nicholas"
    assert user.last_name == "eisenberg"
    assert user.email == "eisenbnt@nv.doe.gov"
    assert user.enabled is True
    assert user.cn == "nicholas eisenberg"
    assert user.dn == "uid=eisenbnt,ou=people"
    assert user.groups == []


def test_add_duplicate_uid(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    with pytest.raises(ValueError):
        user_manager.add(
            uid="eisenbnt",
            first_name="Nick",
            last_name="Smith",
            email="nick@example.com",
            password="password123",
        )


def test_add_duplicate_email(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    with pytest.raises(ValueError):
        user_manager.add(
            uid="nick",
            first_name="Nick",
            last_name="Smith",
            email="eisenbnt@nv.doe.gov",
            password="password123",
        )


def test_remove_user(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    user_manager.remove("eisenbnt")

    with pytest.raises(ValueError):
        user_manager.get("eisenbnt")


def test_remove_missing_user(user_manager: UserManager) -> None:
    with pytest.raises(ValueError):
        user_manager.remove("missing")


def test_get_user(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    user = user_manager.get("eisenbnt")

    assert user.uid == "eisenbnt"
    assert user.first_name == "Nicholas"
    assert user.last_name == "Eisenberg"
    assert user.email == "eisenbnt@nv.doe.gov"
    assert user.enabled is True
    assert user.groups == []


def test_get_missing_user(user_manager: UserManager) -> None:
    with pytest.raises(ValueError):
        user_manager.get("missing")


def test_list_users(user_manager: UserManager) -> None:
    user_manager.add(
        uid="charlie",
        first_name="Charlie",
        last_name="Brown",
        email="charlie@example.com",
        password="password123",
    )

    user_manager.add(
        uid="alice",
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        password="password123",
    )

    user_manager.add(
        uid="bob",
        first_name="Bob",
        last_name="Jones",
        email="bob@example.com",
        password="password123",
    )

    users = user_manager.list()

    assert [user.uid for user in users] == [
        "alice",
        "bob",
        "charlie",
    ]


def test_update_first_name(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nick",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    user = user_manager.update(
        "eisenbnt",
        first_name="Nicholas",
    )

    assert user.first_name == "Nicholas"
    assert user.cn == "Nicholas Eisenberg"


def test_update_last_name(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Smith",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    user = user_manager.update(
        "eisenbnt",
        last_name="Eisenberg",
    )

    assert user.last_name == "Eisenberg"
    assert user.cn == "Nicholas Eisenberg"


def test_update_email(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="old@example.com",
        password="password123",
    )

    user = user_manager.update(
        "eisenbnt",
        email="new@example.com",
    )

    assert user.email == "new@example.com"


def test_update_duplicate_email(user_manager: UserManager) -> None:
    user_manager.add(
        uid="one",
        first_name="One",
        last_name="User",
        email="one@example.com",
        password="password123",
    )

    user_manager.add(
        uid="two",
        first_name="Two",
        last_name="User",
        email="two@example.com",
        password="password123",
    )

    with pytest.raises(ValueError):
        user_manager.update(
            "two",
            email="one@example.com",
        )


def test_update_password(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="old-password",
    )

    user = user_manager.update(
        "eisenbnt",
        password="new-password",
    )

    assert user.uid == "eisenbnt"


def test_update_enabled(user_manager: UserManager) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    user = user_manager.update(
        "eisenbnt",
        enabled=False,
    )

    assert user.enabled is False


def test_update_missing_user(user_manager: UserManager) -> None:
    with pytest.raises(ValueError):
        user_manager.update(
            "missing",
            first_name="Bob",
        )


def test_user_groups(
    user_manager: UserManager,
    group_manager: GroupManager,
) -> None:
    user_manager.add(
        uid="eisenbnt",
        first_name="Nicholas",
        last_name="Eisenberg",
        email="eisenbnt@nv.doe.gov",
        password="password123",
    )

    if "general" not in group_manager.list():
        group_manager.add("general")

    if "vip" not in group_manager.list():
        group_manager.add("vip")

    group_manager.add_user(
        "general",
        "eisenbnt",
    )

    group_manager.add_user(
        "vip",
        "eisenbnt",
    )

    user = user_manager.get("eisenbnt")

    assert [group.name for group in user.groups] == [
        "general",
        "vip",
    ]
