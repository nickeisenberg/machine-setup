#!/bin/bash

LDAP_URI="ldap://localhost:1389"
BIND_DN="cn=admin,dc=nv,dc=doe,dc=gov"
ADMIN_PW="adminpassword"

echo "Checking for new users to add..."

# Loop through all .ldif files in the users/ folder
for user_file in ./users/*.ldif; do
    # Extract DN, strip "dn: ", strip carriage returns (\r), and remove trailing spaces
    USER_DN=$(grep -i '^dn:' "$user_file" | sed -e 's/^[Dd][Nn]: //' -e 's/\r//g' -e 's/[[:space:]]*$//')
    
    # If USER_DN is empty, skip to next file
    if [ -z "$USER_DN" ]; then
        continue
    fi

    # Check if the DN is already in LDAP
    if ldapsearch -x -H "$LDAP_URI" -b "$USER_DN" -s base >/dev/null 2>&1; then
        echo "  [Skipping] User already exists in LDAP: $USER_DN"
    else
        echo "  [Adding] New user found! Importing: $user_file"
        # Run ldapadd. If it fails, print error but don't halt the loop
        if ! ldapadd -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -f "$user_file"; then
            echo "  [Error] Failed to import $user_file"
        fi
    fi
done

echo "Done checking users!"
