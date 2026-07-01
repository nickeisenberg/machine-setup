from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UserReference:
    uid: str
    name: str


@dataclass(slots=True)
class GroupReference:
    name: str
    dn: str


@dataclass(slots=True)
class UserInfo:
    password: str
    uid: str
    first_name: str
    last_name: str
    email: str
    enabled: bool
    cn: str
    dn: str
    groups: list[GroupReference]


@dataclass(slots=True)
class GroupInfo:
    name: str
    description: str | None
    dn: str
    users: list[UserReference]
