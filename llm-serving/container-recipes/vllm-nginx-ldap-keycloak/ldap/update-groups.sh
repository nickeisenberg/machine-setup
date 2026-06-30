#!/bin/bash

LDAP_URI="ldap://localhost:1389"
BIND_DN="cn=admin,dc=nv,dc=doe,dc=gov"
ADMIN_PW="adminpassword"

echo "Updating group assignments..."
# Added -c flag so it doesn't stop on duplicates
ldapmodify -c -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -f ./groups/assign-members.ldif
echo "Group memberships processed!"
