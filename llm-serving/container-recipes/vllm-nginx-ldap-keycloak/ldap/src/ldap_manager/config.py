from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import tomli_w
import tomllib


@dataclass(slots=True)
class DatabaseConfig:
    url: str = ""


@dataclass(slots=True)
class LDAPConfig:
    uri: str = ""

    base_dn: str = ""

    bind_dn: str = ""
    bind_password: str = ""


@dataclass(slots=True)
class Config:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)

    ldap: LDAPConfig = field(default_factory=LDAPConfig)

    @classmethod
    def load(cls, path: Path) -> Config:
        with path.open("rb") as f:
            data = tomllib.load(f)

        return cls(
            database=DatabaseConfig(**data.get("database", {})),
            ldap=LDAPConfig(**data.get("ldap", {})),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as f:
            tomli_w.dump(asdict(self), f)
