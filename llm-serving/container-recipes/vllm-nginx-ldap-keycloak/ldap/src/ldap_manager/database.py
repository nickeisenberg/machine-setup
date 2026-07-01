from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class Database:
    def __init__(
        self,
        database_url: str,
        *,
        echo: bool = False,
    ) -> None:
        self._engine: Engine = create_engine(
            database_url,
            echo=echo,
        )

        self._sessionmaker = sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    def create(self) -> None:
        """
        Create all database tables.
        """
        Base.metadata.create_all(self._engine)

    def session(self) -> Session:
        """
        Return a new SQLAlchemy session.
        """
        return self._sessionmaker()
