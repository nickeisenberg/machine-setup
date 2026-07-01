from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ldap_manager.database import Database
from ldap_manager.models import Group, User


@dataclass(slots=True)
class UserReference:
    uid: str
    name: str


@dataclass(slots=True)
class GroupInfo:
    name: str
    description: str | None
    dn: str
    users: list[UserReference]


class GroupManager:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(
        self,
        name: str,
        description: str | None = None,
    ) -> GroupInfo:
        with self._database.session() as session:
            existing = session.scalar(select(Group).where(Group.name == name))

            if existing is not None:
                raise ValueError(f"Group '{name}' already exists.")

            group = Group(
                name=name,
                description=description,
            )

            session.add(group)
            session.commit()
            session.refresh(group)

            return self._to_info(group)

    def remove(self, name: str) -> None:
        with self._database.session() as session:
            group = session.scalar(select(Group).where(Group.name == name))

            if group is None:
                raise ValueError(f"Group '{name}' does not exist.")

            session.delete(group)
            session.commit()

    def rename(
        self,
        old_name: str,
        new_name: str,
    ) -> GroupInfo:
        with self._database.session() as session:
            group = session.scalar(select(Group).where(Group.name == old_name))

            if group is None:
                raise ValueError(f"Group '{old_name}' does not exist.")

            existing = session.scalar(
                select(Group).where(Group.name == new_name)
            )

            if existing is not None:
                raise ValueError(f"Group '{new_name}' already exists.")

            group.name = new_name

            session.commit()
            session.refresh(group)

            return self._to_info(group)

    def get(self, name: str) -> GroupInfo:
        with self._database.session() as session:
            group = session.scalar(
                select(Group)
                .options(selectinload(Group.users))
                .where(Group.name == name)
            )

            if group is None:
                raise ValueError(f"Group '{name}' does not exist.")

            return self._to_info(group)

    def list(self) -> list[GroupInfo]:
        with self._database.session() as session:
            groups = session.scalars(
                select(Group)
                .options(selectinload(Group.users))
                .order_by(Group.name)
            )

            return [self._to_info(group) for group in groups]

    def add_user(
        self,
        group_name: str,
        user_uid: str,
    ) -> GroupInfo:
        with self._database.session() as session:
            group = session.scalar(
                select(Group)
                .options(selectinload(Group.users))
                .where(Group.name == group_name)
            )

            if group is None:
                raise ValueError(f"Group '{group_name}' does not exist.")

            user = session.scalar(select(User).where(User.uid == user_uid))

            if user is None:
                raise ValueError(f"User '{user_uid}' does not exist.")

            if user in group.users:
                raise ValueError(
                    f"User '{user_uid}' is already a member of '{group_name}'."
                )

            group.users.append(user)

            session.commit()
            session.refresh(group)

            return self._to_info(group)

    def remove_user(
        self,
        group_name: str,
        user_uid: str,
    ) -> GroupInfo:
        with self._database.session() as session:
            group = session.scalar(
                select(Group)
                .options(selectinload(Group.users))
                .where(Group.name == group_name)
            )

            if group is None:
                raise ValueError(f"Group '{group_name}' does not exist.")

            user = session.scalar(select(User).where(User.uid == user_uid))

            if user is None:
                raise ValueError(f"User '{user_uid}' does not exist.")

            if user not in group.users:
                raise ValueError(
                    f"User '{user_uid}' is not a member of '{group_name}'."
                )

            group.users.remove(user)

            session.commit()
            session.refresh(group)

            return self._to_info(group)

    def list_users(
        self,
        group_name: str,
    ) -> list[UserReference]:
        return self.get(group_name).users

    @staticmethod
    def _to_info(group: Group) -> GroupInfo:
        return GroupInfo(
            name=group.name,
            description=group.description,
            dn=group.dn,
            users=[
                UserReference(
                    uid=user.uid,
                    name=user.cn,
                )
                for user in sorted(
                    group.users,
                    key=lambda user: user.uid,
                )
            ],
        )
