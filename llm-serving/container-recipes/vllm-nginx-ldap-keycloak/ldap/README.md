# ldapman

`ldapman` is a lightweight command-line tool for managing LDAP users and groups
using a local SQLite database as the source of truth.

Instead of editing LDAP directly, users and groups are managed locally and then
synchronized to a remote LDAP directory.

---

# Philosophy

`ldapman` separates administration into two stages:

1. Manage users and groups locally.
2. Synchronize the desired state to LDAP.

```
        Local Database (SQLite)
                │
                │ ldapman sync
                ▼
         Remote LDAP Directory
```

The local project database is always considered the authoritative source.

---

# Creating a Project

Create a new ldapman project.

```bash
ldapman init
```

This creates:

```
.ldapman/
├── config.toml
├── ldap.db
└── VERSION
```

---

# Configuration

View the current configuration.

```bash
ldapman config list
```

Example:

```toml
[database]
url = sqlite:///.../.ldapman/ldap.db

[ldap]
directory = openldap
uri = ldap://localhost:1389
base_dn = dc=nv,dc=doe,dc=gov
bind_dn = cn=admin,dc=nv,dc=doe,dc=gov
bind_password = adminpassword
```

Edit the configuration.

```bash
ldapman config edit
```

Get a configuration value.

```bash
ldapman config get ldap.uri
```

Set a configuration value.

```bash
ldapman config set ldap.uri ldap://localhost:1389
ldapman config set ldap.base_dn dc=nv,dc=doe,dc=gov
ldapman config set ldap.bind_dn cn=admin,dc=nv,dc=doe,dc=gov
ldapman config set ldap.bind_password adminpassword
```

---

# User Commands

## Add a User

```bash
ldapman user add <uid> <first_name> <last_name> <email> <password>
```

Example:

```bash
ldapman user add eisenbnt Nicholas Eisenberg eisenbnt@nv.doe.gov password123
```

---

## Remove a User

```bash
ldapman user remove <uid>
```

---

## Update a User

```bash
ldapman user update <uid> [options]
```

Options:

```
--first-name
--last-name
--email
--password
--enable
--disable
```

Example:

```bash
ldapman user update eisenbnt \
    --email nick@nv.doe.gov \
    --disable
```

---

## List Users

```bash
ldapman user list
```

Example output:

```
UID              Name                           Enabled
------------------------------------------------------------
eisenbnt         Nicholas Eisenberg            Yes
```

---

## Show User

```bash
ldapman user show <uid>
```

Example:

```
UID        : eisenbnt
Name       : Nicholas Eisenberg
Email      : eisenbnt@nv.doe.gov
Enabled    : Yes
DN         : uid=eisenbnt,ou=people,...

Groups:
  developers
  admins
```

---

# Group Commands

## Add a Group

```bash
ldapman group add <name>
```

Optional description:

```bash
ldapman group add developers \
    --description "Software Developers"
```

---

## Remove a Group

```bash
ldapman group remove <name>
```

---

## Rename a Group

```bash
ldapman group rename <old_name> <new_name>
```

---

## List Groups

```bash
ldapman group list
```

---

## Show Group

```bash
ldapman group show <name>
```

Example:

```
Name        : developers
Description : Software Developers
DN          : cn=developers,...

Users:
  eisenbnt        Nicholas Eisenberg
```

---

## Add a User to a Group

```bash
ldapman group add-user <group> <uid>
```

Example:

```bash
ldapman group add-user developers eisenbnt
```

---

## Remove a User from a Group

```bash
ldapman group remove-user <group> <uid>
```

---

## List Users in a Group

```bash
ldapman group list-users <group>
```

---

# Synchronizing LDAP

Push the current SQLite database to the configured LDAP directory.

```bash
ldapman sync
```

Synchronization performs the following:

- Creates missing users.
- Updates existing users.
- Removes users that no longer exist locally.
- Creates missing groups.
- Updates group membership.
- Removes groups that no longer exist locally.

SQLite is always treated as the source of truth.

Empty groups are skipped when synchronizing to OpenLDAP because the
`groupOfNames` object class requires at least one member.

---

# Inspecting the LDAP Directory

These commands read directly from the configured LDAP server.

## List LDAP Users

```bash
ldapman ldap user list
```

---

## Show LDAP User

```bash
ldapman ldap user show <uid>
```

---

## List LDAP Groups

```bash
ldapman ldap group list
```

---

## Show LDAP Group

```bash
ldapman ldap group show <name>
```

---

# Typical Workflow

Initialize a project.

```bash
ldapman init
```

Configure the LDAP server.

```bash
ldapman config edit
```

Create a user.

```bash
ldapman user add \
    eisenbnt \
    Nicholas \
    Eisenberg \
    eisenbnt@nv.doe.gov \
    password123
```

Create a group.

```bash
ldapman group add developers
```

Add the user to the group.

```bash
ldapman group add-user developers eisenbnt
```

Synchronize the database to LDAP.

```bash
ldapman sync
```

Verify the remote directory.

```bash
ldapman ldap user list

ldapman ldap group list

ldapman ldap user show eisenbnt

ldapman ldap group show developers
```

---

# Supported Directory Types

Current:

- OpenLDAP

Planned:

- Microsoft Active Directory

Additional directory implementations can be added without changing the CLI by
implementing the common directory interface.
