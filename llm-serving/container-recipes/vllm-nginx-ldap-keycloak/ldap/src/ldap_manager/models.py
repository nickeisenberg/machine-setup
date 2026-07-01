from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    uid: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    password: Mapped[str] = mapped_column(String)

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    groups: Mapped[list[Group]] = relationship(
        secondary="user_groups",
        back_populates="users",
    )

    @classmethod
    def defaults(cls) -> list[User]:
        return []

    @property
    def cn(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def dn(self) -> str:
        return f"uid={self.uid},ou=people"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    users: Mapped[list[User]] = relationship(
        secondary="user_groups",
        back_populates="groups",
    )

    @classmethod
    def defaults(cls) -> list[Group]:
        return [
            cls(name="general"),
            cls(name="vip"),
        ]

    @property
    def dn(self) -> str:
        return f"cn={self.name},ou=groups"


class UserGroup(Base):
    __tablename__ = "user_groups"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )

    @classmethod
    def defaults(cls) -> list[UserGroup]:
        return []
