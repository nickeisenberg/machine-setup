from __future__ import annotations

from ldap_manager.database import Database
from ldap_manager.ldap.directories.base import Directory
from ldap_manager.managers.group_manager import GroupManager
from ldap_manager.managers.user_manager import UserManager


class Sync:
    def __init__(
        self,
        database: Database,
        directory: Directory,
    ) -> None:
        self._directory = directory

        self._user_manager = UserManager(database)
        self._group_manager = GroupManager(database)

    def sync(self) -> None:
        self._sync_users()
        self._sync_groups()

    def _sync_users(self) -> None:
        local = {user.uid: user for user in self._user_manager.list()}

        remote = {user.uid: user for user in self._directory.list_users()}

        #
        # Create / update
        #

        for uid, user in local.items():
            if uid not in remote:
                self._directory.add_user(user)
            else:
                self._directory.update_user(user)

        #
        # Delete
        #

        for uid in remote.keys() - local.keys():
            self._directory.delete_user(uid)

    def _sync_groups(self) -> None:
        local = {group.name: group for group in self._group_manager.list()}

        remote = {group.name: group for group in self._directory.list_groups()}

        #
        # Create / update
        #

        for name, group in local.items():
            if not group.users:
                print(
                    f"Warning: skipping empty group '{name}' "
                    "(OpenLDAP groupOfNames requires at least one member)."
                )
                continue

            if name not in remote:
                self._directory.add_group(group)
            else:
                self._directory.update_group(group)

        #
        # Delete
        #

        for name in remote.keys() - local.keys():
            self._directory.delete_group(name)
