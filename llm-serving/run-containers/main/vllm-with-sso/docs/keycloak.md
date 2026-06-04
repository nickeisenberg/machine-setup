# Keycloak LDAP User Federation Configuration

Navigation:

```text
User Federation
→ LDAP
```

## General Options

| Setting | Value |
|----------|---------|
| UI display name | lsap |
| Vendor | Other |

## Connection and Authentication

| Setting | Value |
|----------|---------|
| Connection URL | ldap://ldap:389 |
| Enable StartTLS | Off |
| Use Truststore SPI | Always |
| Connection Pooling | On |
| Connection Timeout | Leave blank |
| Bind Type | simple |
| Bind DN | cn=admin,dc=company,dc=local |
| Bind Credentials | adminpassword |

## LDAP Searching and Updating

| Setting | Value |
|----------|---------|
| Edit Mode | READ_ONLY |
| Users DN | ou=people,dc=company,dc=local |
| Relative user creation DN | leave blank |
| Username LDAP Attribute | uid |
| RDN LDAP Attribute | uid |
| UUID LDAP Attribute | entryUUID |
| User Object Classes | inetOrgPerson, organizationalPerson |
| Search Scope | Subtree  |
| Read timeout | leave blank  |
| Pagination | On  |
| Referal | leave blank  |

## Synchronization Settings

| Setting | Value |
|----------|---------|
| Import Users | On |
| Sync Registrations | Off |
| Batch Size | leave blank |
| Periodic Full Sync | Off |
| Periodic Changed Users Sync | Off |
| Remove Invalid Users During Searches | On |

## Kerberos Integration

| Setting | Value |
|----------|---------|
| Allow Kerberos Authentication | Off |
| Use Kerberos for Password Authentication | Off |

## Cache Settings

| Setting | Value |
|----------|---------|
| Cache Policy | DEFAULT |

## Advanced Settings

| Setting | Value |
|----------|---------|
| Enable the LDAPv3 Password Modify Extended Operation | Off |
| Validate Password Policy | Off |
| Enable LDAP Password Policy | Off |
| Trust Email | Off |
| Connection Trace | Off |

## User Synchronization

After clicking:

```text
Synchronize all users
```

Expected imported users:

```text
nick
jane
```

## Notes

LDAP users authenticate against OpenLDAP through Keycloak.

Example LDAP user:

```ldif
dn: uid=jane,ou=people,dc=company,dc=local
objectClass: inetOrgPerson
cn: Jane
sn: Doe
uid: jane
mail: jane@company.local
userPassword: password123
```

The resulting authentication flow is:

```text
OpenLDAP
    ↓
Keycloak
    ↓ JWT
NGINX Auth Service
    ↓
vLLM
```
