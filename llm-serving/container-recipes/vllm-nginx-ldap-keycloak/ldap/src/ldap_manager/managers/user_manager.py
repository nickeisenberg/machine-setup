from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ldap_manager.database import Database
from ldap_manager.models import User


@dataclass(slots=True)
class GroupReference:
    name: str
    dn: str


@dataclass(slots=True)
class UserInfo:
    uid: str
    first_name: str
    last_name: str
    email: str
    enabled: bool
    cn: str
    dn: str
    groups: list[GroupReference]


class UserManager:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(
        self,
        uid: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        *,
        enabled: bool = True,
    ) -> UserInfo:
        with self._database.session() as session:
            if session.scalar(select(User).where(User.uid == uid)):
                raise ValueError(f"User '{uid}' already exists.")

            if session.scalar(select(User).where(User.email == email)):
                raise ValueError(f"Email '{email}' already exists.")

            user = User(
                uid=uid,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                enabled=enabled,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return self._to_info(user)

    def remove(self, uid: str) -> None:
        with self._database.session() as session:
            user = session.scalar(select(User).where(User.uid == uid))

            if user is None:
                raise ValueError(f"User '{uid}' does not exist.")

            session.delete(user)
            session.commit()

    def update(
        self,
        uid: str,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        enabled: bool | None = None,
    ) -> UserInfo:
        with self._database.session() as session:
            user = session.scalar(
                select(User)
                .options(selectinload(User.groups))
                .where(User.uid == uid)
            )

            if user is None:
                raise ValueError(f"User '{uid}' does not exist.")

            if email is not None and email != user.email:
                existing = session.scalar(
                    select(User).where(User.email == email)
                )

                if existing is not None:
                    raise ValueError(f"Email '{email}' already exists.")

            if first_name is not None:
                user.first_name = first_name

            if last_name is not None:
                user.last_name = last_name

            if email is not None:
                user.email = email

            if password is not None:
                user.password = password

            if enabled is not None:
                user.enabled = enabled

            session.commit()
            session.refresh(user)

            return self._to_info(user)

    def get(self, uid: str) -> UserInfo:
        with self._database.session() as session:
            user = session.scalar(
                select(User)
                .options(selectinload(User.groups))
                .where(User.uid == uid)
            )

            if user is None:
                raise ValueError(f"User '{uid}' does not exist.")

            return self._to_info(user)

    def list(self) -> list[UserInfo]:
        with self._database.session() as session:
            users = session.scalars(
                select(User)
                .options(selectinload(User.groups))
                .order_by(User.uid)
            )

            return [self._to_info(user) for user in users]

    @staticmethod
    def _to_info(user: User) -> UserInfo:
        return UserInfo(
            uid=user.uid,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            enabled=user.enabled,
            cn=user.cn,
            dn=user.dn,
            groups=[
                GroupReference(
                    name=group.name,
                    dn=group.dn,
                )
                for group in user.groups
            ],
        )
