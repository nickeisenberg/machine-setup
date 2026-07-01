from __future__ import annotations

from ldap_manager.dto import GroupInfo, UserInfo, UserReference
from ldap_manager.ldap.client import LDAPClient
from ldap_manager.ldap.directories.openldap import OpenLDAP

BASE_DN = "dc=nv,dc=doe,dc=gov"

TEST_USER_INFO = UserInfo(
    password="password123",
    uid="asdf",
    first_name="asdf",
    last_name="fdsa",
    email="asdf@nv.doe.gov",
    enabled=True,
    cn="asdf fdsa",
    dn="",
    groups=[],
)


def directory() -> OpenLDAP:
    client = LDAPClient(
        uri="ldap://localhost:1389",
        bind_dn=f"cn=admin,{BASE_DN}",
        bind_password="adminpassword",
    )

    return OpenLDAP(
        client=client,
        base_dn=BASE_DN,
    )


def test_user_group_lifecycle() -> None:
    ldap = directory()

    ldap.add_user(TEST_USER_INFO)

    ldap.add_group(
        GroupInfo(
            name="developers",
            description=None,
            dn="",
            users=[
                UserReference(
                    uid=TEST_USER_INFO.uid,
                    name=TEST_USER_INFO.cn,
                ),
            ],
        )
    )

    loaded_user = ldap.get_user(TEST_USER_INFO.uid)
    loaded_group = ldap.get_group("developers")

    assert loaded_user is not None
    assert loaded_group is not None

    assert loaded_user.uid == TEST_USER_INFO.uid
    assert loaded_group.name == "developers"

    assert len(loaded_group.users) == 1
    assert loaded_group.users[0].uid == TEST_USER_INFO.uid

    assert any(group.name == "developers" for group in loaded_user.groups)

    ldap.delete_group("developers")

    assert ldap.get_group("developers") is None

    loaded_user = ldap.get_user(TEST_USER_INFO.uid)
    assert loaded_user is not None
    assert loaded_user.groups == []

    ldap.delete_user(TEST_USER_INFO.uid)

    assert ldap.get_user(TEST_USER_INFO.uid) is None
