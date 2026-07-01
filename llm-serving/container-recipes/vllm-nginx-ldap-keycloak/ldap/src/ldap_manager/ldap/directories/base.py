from __future__ import annotations

from abc import ABC, abstractmethod

from ldap_manager.dto import GroupInfo, UserInfo
from ldap_manager.ldap.client import LDAPClient


class Directory(ABC):
    def __init__(
        self,
        client: LDAPClient,
        *,
        base_dn: str,
    ) -> None:
        self.client = client
        self.base_dn = base_dn

    @property
    def people_dn(self) -> str:
        return f"ou=people,{self.base_dn}"

    @property
    def groups_dn(self) -> str:
        return f"ou=groups,{self.base_dn}"

    @abstractmethod
    def list_users(self) -> list[UserInfo]: ...

    @abstractmethod
    def get_user(
        self,
        uid: str,
    ) -> UserInfo | None: ...

    @abstractmethod
    def add_user(
        self,
        user: UserInfo,
    ) -> None: ...

    @abstractmethod
    def update_user(
        self,
        user: UserInfo,
    ) -> None: ...

    @abstractmethod
    def delete_user(
        self,
        uid: str,
    ) -> None: ...

    #
    # Groups
    #

    @abstractmethod
    def list_groups(self) -> list[GroupInfo]: ...

    @abstractmethod
    def get_group(
        self,
        name: str,
    ) -> GroupInfo | None: ...

    @abstractmethod
    def add_group(
        self,
        group: GroupInfo,
    ) -> None: ...

    @abstractmethod
    def update_group(
        self,
        group: GroupInfo,
    ) -> None: ...

    @abstractmethod
    def delete_group(
        self,
        name: str,
    ) -> None: ...

    #
    # Membership
    #

    @abstractmethod
    def add_user_to_group(
        self,
        uid: str,
        group: str,
    ) -> None: ...

    @abstractmethod
    def remove_user_from_group(
        self,
        uid: str,
        group: str,
    ) -> None: ...
