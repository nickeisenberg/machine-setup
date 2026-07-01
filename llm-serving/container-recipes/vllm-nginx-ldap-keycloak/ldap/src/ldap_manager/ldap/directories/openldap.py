from __future__ import annotations

from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, Entry

from ldap_manager.dto import (
    GroupInfo,
    GroupReference,
    UserInfo,
    UserReference,
)
from ldap_manager.ldap.client import LDAPClient
from ldap_manager.ldap.directories.base import Directory


class OpenLDAP(Directory):
    def __init__(
        self,
        client: LDAPClient,
        *,
        base_dn: str,
    ) -> None:
        super().__init__(
            client,
            base_dn=base_dn,
        )

    def user_dn(
        self,
        uid: str,
    ) -> str:
        return f"uid={uid},{self.people_dn}"

    def group_dn(
        self,
        name: str,
    ) -> str:
        return f"cn={name},{self.groups_dn}"

    @property
    def user_object_classes(self) -> list[str]:
        return [
            "top",
            "person",
            "organizationalPerson",
            "inetOrgPerson",
        ]

    @property
    def group_object_classes(self) -> list[str]:
        return [
            "top",
            "groupOfNames",
        ]

    def user_attributes(
        self,
        user: UserInfo,
    ) -> dict[str, object]:
        return {
            "uid": user.uid,
            "cn": user.cn,
            "givenName": user.first_name,
            "sn": user.last_name,
            "mail": user.email,
            "userPassword": user.password,
        }

    def group_attributes(
        self,
        group: GroupInfo,
    ) -> dict[str, object]:
        return {
            "cn": group.name,
            "member": [self.user_dn(user.uid) for user in group.users],
        }

    def add_user(
        self,
        user: UserInfo,
    ) -> None:
        self.client.add(
            dn=self.user_dn(user.uid),
            object_classes=self.user_object_classes,
            attributes=self.user_attributes(user),
        )

    def add_user_to_group(
        self,
        uid: str,
        group: str,
    ) -> None:
        self.client.modify(
            dn=self.group_dn(group),
            changes={
                "member": [
                    (
                        MODIFY_ADD,
                        [self.user_dn(uid)],
                    ),
                ],
            },
        )

    def remove_user_from_group(
        self,
        uid: str,
        group: str,
    ) -> None:
        self.client.modify(
            dn=self.group_dn(group),
            changes={
                "member": [
                    (
                        MODIFY_DELETE,
                        [self.user_dn(uid)],
                    ),
                ],
            },
        )

    def update_user(
        self,
        user: UserInfo,
    ) -> None:
        self.client.modify(
            dn=self.user_dn(user.uid),
            changes={
                "cn": [
                    (
                        MODIFY_REPLACE,
                        [user.cn],
                    ),
                ],
                "sn": [
                    (
                        MODIFY_REPLACE,
                        [user.last_name],
                    ),
                ],
                "givenName": [
                    (
                        MODIFY_REPLACE,
                        [user.first_name],
                    ),
                ],
                "mail": [
                    (
                        MODIFY_REPLACE,
                        [user.email],
                    ),
                ],
                "userPassword": [
                    (
                        MODIFY_REPLACE,
                        [user.password],
                    ),
                ],
            },
        )

    def update_group(
        self,
        group: GroupInfo,
    ) -> None:
        self.client.modify(
            dn=self.group_dn(group.name),
            changes={
                "member": [
                    (
                        MODIFY_REPLACE,
                        [self.user_dn(user.uid) for user in group.users],
                    ),
                ],
            },
        )

    def list_groups(self) -> list[GroupInfo]:
        entries = self.client.search(
            base_dn=self.groups_dn,
            ldap_filter="(objectClass=groupOfNames)",
            attributes=[
                "cn",
                "member",
            ],
        )

        return [self._entry_to_group(entry) for entry in entries]

    def get_group(
        self,
        name: str,
    ) -> GroupInfo | None:
        return next(
            (group for group in self.list_groups() if group.name == name),
            None,
        )

    def delete_user(
        self,
        uid: str,
    ) -> None:
        self.client.delete(
            dn=self.user_dn(uid),
        )

    def add_group(
        self,
        group: GroupInfo,
    ) -> None:
        self.client.add(
            dn=self.group_dn(group.name),
            object_classes=self.group_object_classes,
            attributes=self.group_attributes(group),
        )

    def delete_group(
        self,
        name: str,
    ) -> None:
        self.client.delete(
            dn=self.group_dn(name),
        )

    def list_users(self) -> list[UserInfo]:
        group_map: dict[str, list[GroupReference]] = {}

        for group in self.list_groups():
            reference = GroupReference(
                name=group.name,
                dn=group.dn,
            )

            for user in group.users:
                group_map.setdefault(user.uid, []).append(reference)

        entries = self.client.search(
            base_dn=self.people_dn,
            ldap_filter="(objectClass=inetOrgPerson)",
            attributes=[
                "uid",
                "cn",
                "sn",
                "givenName",
                "mail",
                "userPassword",
            ],
        )

        return [
            self._entry_to_user(
                entry,
                group_map.get(str(entry.uid), []),
            )
            for entry in entries
        ]

    def _entry_to_user(
        self,
        entry: Entry,
        groups: list[GroupReference],
    ) -> UserInfo:
        uid = str(entry.uid) if "uid" in entry.entry_attributes else ""

        cn = str(entry.cn) if "cn" in entry.entry_attributes else ""

        first_name = (
            str(entry.givenName)
            if "givenName" in entry.entry_attributes
            else cn.split(" ", 1)[0]
        )

        last_name = str(entry.sn) if "sn" in entry.entry_attributes else ""

        email = str(entry.mail) if "mail" in entry.entry_attributes else ""

        password = (
            str(entry.userPassword)
            if "userPassword" in entry.entry_attributes
            else ""
        )

        return UserInfo(
            password=password,
            uid=uid,
            first_name=first_name,
            last_name=last_name,
            email=email,
            enabled=True,
            cn=cn,
            dn=str(entry.entry_dn),
            groups=groups,
        )

    def get_user(
        self,
        uid: str,
    ) -> UserInfo | None:
        return next(
            (user for user in self.list_users() if user.uid == uid),
            None,
        )

    def _entry_to_group(
        self,
        entry: Entry,
    ) -> GroupInfo:
        users: list[UserReference] = []

        if "member" in entry:
            for member_dn in entry.member.values:
                rdn = member_dn.split(",", 1)[0]

                if rdn.startswith("uid="):
                    uid = rdn[4:]

                    users.append(
                        UserReference(
                            uid=uid,
                            name=uid,
                        )
                    )

        return GroupInfo(
            name=str(entry.cn),
            description=None,
            dn=str(entry.entry_dn),
            users=users,
        )
