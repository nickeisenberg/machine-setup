from __future__ import annotations

from typing import Any

from ldap3 import ALL, Connection, Server


class LDAPClient:
    def __init__(
        self,
        *,
        uri: str,
        bind_dn: str,
        bind_password: str,
    ) -> None:
        self._server = Server(
            uri,
            get_info=ALL,
        )

        self._bind_dn = bind_dn
        self._bind_password = bind_password

        self._connection: Connection | None = None

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = Connection(
                self._server,
                user=self._bind_dn,
                password=self._bind_password,
                auto_bind=True,
            )

        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.unbind()
            self._connection = None

    def __enter__(self) -> LDAPClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    #
    # Generic LDAP operations
    #

    def search(
        self,
        *,
        base_dn: str,
        ldap_filter: str = "(objectClass=*)",
        attributes: list[str] | None = None,
    ):
        self.connection.search(
            search_base=base_dn,
            search_filter=ldap_filter,
            attributes=attributes,
        )

        return list(self.connection.entries)

    def get(
        self,
        *,
        dn: str,
        attributes: list[str] | None = None,
    ):
        entries = self.search(
            base_dn=dn,
            ldap_filter="(objectClass=*)",
            attributes=attributes,
        )

        if not entries:
            return None

        return entries[0]

    def exists(
        self,
        *,
        dn: str,
    ) -> bool:
        return self.get(dn=dn) is not None

    def add(
        self,
        *,
        dn: str,
        object_classes: list[str],
        attributes: dict[str, Any],
    ) -> None:
        ok = self.connection.add(
            dn=dn,
            object_class=object_classes,
            attributes=attributes,
        )

        if not ok:
            raise RuntimeError(self.connection.result)

    def modify(
        self,
        *,
        dn: str,
        changes: dict[str, Any],
    ) -> None:
        ok = self.connection.modify(
            dn,
            changes,
        )

        if not ok:
            raise RuntimeError(self.connection.result)

    def delete(
        self,
        *,
        dn: str,
    ) -> None:
        ok = self.connection.delete(dn)

        if not ok:
            raise RuntimeError(self.connection.result)

    def rename(
        self,
        *,
        dn: str,
        new_rdn: str,
        new_superior: str | None = None,
    ) -> None:
        ok = self.connection.modify_dn(
            dn,
            relative_dn=new_rdn,
            new_superior=new_superior,
        )

        if not ok:
            raise RuntimeError(self.connection.result)

    def compare(
        self,
        *,
        dn: str,
        attribute: str,
        value: str,
    ) -> bool:
        return self.connection.compare(
            dn,
            attribute,
            value,
        )
