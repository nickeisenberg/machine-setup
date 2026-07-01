from __future__ import annotations

from ldap3 import ALL, Connection, Server


class LDAP:
    def __init__(
        self,
        *,
        uri: str,
        bind_dn: str,
        bind_password: str,
        base_dn: str,
    ) -> None:
        self.uri = uri
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.base_dn = base_dn

        self._server = Server(
            uri,
            get_info=ALL,
        )

        self._connection: Connection | None = None

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = Connection(
                self._server,
                user=self.bind_dn,
                password=self.bind_password,
                auto_bind=True,
            )

        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.unbind()
            self._connection = None

    def __enter__(self) -> "LDAP":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
