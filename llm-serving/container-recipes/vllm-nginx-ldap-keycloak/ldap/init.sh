#!/bin/bash
set -e

LDAP_URI="ldap://localhost:1389"
BIND_DN="cn=admin,dc=nv,dc=doe,dc=gov"
ADMIN_PW="adminpassword"

echo "1. Checking and creating OUs and initial Groups..."
# Check if ou=people already exists
if ldapsearch -x -H "$LDAP_URI" -b "ou=people,dc=nv,dc=doe,dc=gov" -s base >/dev/null 2>&1; then
    echo "  [Skipping] OUs and Groups already exist."
else
    echo "  [Adding] Creating OUs and initial Groups..."
    ldapadd -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -f ./bootstrap/01-init-structure.ldif
fi

echo "2. Adding all users from the users directory..."
# Temporarily turn off 'exit on error' so we don't crash if some users already exist
set +e
for user_file in ./users/*.ldif; do
    # Extract DN and clean it up
    USER_DN=$(grep -i '^dn:' "$user_file" | sed -e 's/^[Dd][Nn]: //' -e 's/\r//g' -e 's/[[:space:]]*$//')
    
    if ldapsearch -x -H "$LDAP_URI" -b "$USER_DN" -s base >/dev/null 2>&1; then
        echo "  [Skipping] User already exists: $USER_DN"
    else
        echo "  [Adding] Adding new user: $user_file"
        ldapadd -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -f "$user_file"
    fi
done
set -e # Turn 'exit on error' back on

echo "3. Assigning users to groups..."
# Turn off 'set -e' for groups in case some group associations already exist
set +e
ldapmodify -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -f ./groups/assign-members.ldif
set -e

echo "=== LDAP initialized successfully! ==="
