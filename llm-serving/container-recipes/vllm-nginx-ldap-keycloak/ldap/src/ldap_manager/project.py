from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ldap_manager.config import Config
from ldap_manager.database import Database
from ldap_manager.ldap.client import LDAPClient
from ldap_manager.ldap.directories.openldap import OpenLDAP
from ldap_manager.models import Group, User, UserGroup

PROJECT_DIRECTORY = ".ldapman"
CONFIG_FILE = "config.toml"
VERSION_FILE = "VERSION"
DATABASE_FILE = "ldap.db"

DEFAULT_MODELS = (
    Group,
    User,
    UserGroup,
)


@dataclass(slots=True)
class Project:
    root: Path
    config: Config

    _database: Database | None = field(
        init=False,
        default=None,
        repr=False,
    )

    _ldap_directory: OpenLDAP | None = field(
        init=False,
        default=None,
        repr=False,
    )

    @property
    def directory(self) -> Path:
        return self.root / PROJECT_DIRECTORY

    @property
    def config_path(self) -> Path:
        return self.directory / CONFIG_FILE

    @property
    def version_path(self) -> Path:
        return self.directory / VERSION_FILE

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = Database(
                self.config.database.url,
            )

        return self._database

    @property
    def ldap_directory(self) -> OpenLDAP:
        if self._ldap_directory is None:
            client = LDAPClient(
                uri=self.config.ldap.uri,
                bind_dn=self.config.ldap.bind_dn,
                bind_password=self.config.ldap.bind_password,
            )

            self._ldap_directory = OpenLDAP(
                client=client,
                base_dn=self.config.ldap.base_dn,
            )

        return self._ldap_directory

    @classmethod
    def initialize(
        cls,
        root: Path | None = None,
    ) -> Project:
        if root is None:
            root = Path.cwd()

        root = root.resolve()

        project = cls(
            root=root,
            config=Config(),
        )

        project.directory.mkdir(exist_ok=False)

        database_path = (project.directory / DATABASE_FILE).resolve()

        project.config.database.url = f"sqlite:///{database_path}"

        project.config.save(project.config_path)

        project.version_path.write_text("1\n")

        project.database.create()
        project.populate_defaults()

        return project

    @classmethod
    def find(
        cls,
        start: Path | None = None,
    ) -> Project:
        if start is None:
            start = Path.cwd()

        start = start.resolve()

        for directory in (start, *start.parents):
            project_directory = directory / PROJECT_DIRECTORY

            if project_directory.is_dir():
                return cls(
                    root=directory,
                    config=Config.load(
                        project_directory / CONFIG_FILE,
                    ),
                )

        raise RuntimeError("Not inside an ldapman project.")

    def save(self) -> None:
        self.config.save(self.config_path)

    def populate_defaults(self) -> None:
        with self.database.session() as session:
            for model in DEFAULT_MODELS:
                session.add_all(model.defaults())

            session.commit()
