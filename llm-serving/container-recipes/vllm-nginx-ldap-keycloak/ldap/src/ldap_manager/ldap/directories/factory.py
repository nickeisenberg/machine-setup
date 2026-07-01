from __future__ import annotations

from ldap_manager.ldap.client import LDAPClient
from ldap_manager.ldap.directories.base import Directory
from ldap_manager.ldap.directories.openldap import OpenLDAP

DIRECTORIES: dict[str, type[Directory]] = {
    "openldap": OpenLDAP,
}


def make_directory(
    name: str,
    *,
    client: LDAPClient,
    base_dn: str,
) -> Directory:
    try:
        cls = DIRECTORIES[name]
    except KeyError:
        raise ValueError(f"Unknown directory type: {name!r}")

    return cls(
        client=client,
        base_dn=base_dn,
    )
