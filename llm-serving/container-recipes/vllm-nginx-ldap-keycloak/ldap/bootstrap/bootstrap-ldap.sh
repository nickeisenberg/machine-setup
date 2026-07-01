#!/usr/bin/env bash
set -euo pipefail

LDAP_URI="ldap://localhost:1389"
BASE_DN="dc=nv,dc=doe,dc=gov"
ADMIN_DN="cn=admin,$BASE_DN"
ADMIN_PASSWORD="adminpassword"

cat <<EOF | ldapadd \
    -x \
    -H "$LDAP_URI" \
    -D "$ADMIN_DN" \
    -w "$ADMIN_PASSWORD"

###############################################################################
# Organizational Units
###############################################################################

dn: ou=people,$BASE_DN
objectClass: organizationalUnit
ou: people

dn: ou=groups,$BASE_DN
objectClass: organizationalUnit
ou: groups

###############################################################################
# Dummy User
###############################################################################

dn: uid=dummy,ou=people,$BASE_DN
objectClass: inetOrgPerson
cn: Dummy User
sn: User
uid: dummy
mail: dummy@nv.doe.gov
userPassword: dummy

###############################################################################
# Groups
###############################################################################

dn: cn=general,ou=groups,$BASE_DN
objectClass: groupOfNames
cn: general
member: uid=dummy,ou=people,$BASE_DN

dn: cn=vip,ou=groups,$BASE_DN
objectClass: groupOfNames
cn: vip
member: uid=dummy,ou=people,$BASE_DN

EOF

echo "LDAP initialization complete."
