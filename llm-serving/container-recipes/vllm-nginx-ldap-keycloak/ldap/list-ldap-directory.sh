#!/bin/bash

LDAP_URI="ldap://localhost:1389"
BIND_DN="cn=admin,dc=nv,dc=doe,dc=gov"
ADMIN_PW="adminpassword"
BASE_DN="dc=nv,dc=doe,dc=gov"

# Color formatting for beautiful output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}========================================================================${NC}"
echo -e " ${GREEN}LDAP Directory Registry (nv.doe.gov)${NC}"
echo -e "${BOLD}========================================================================${NC}"
printf "%-15s | %-20s | %-30s\n" "Username (UID)" "Groups" "Email"
echo "------------------------------------------------------------------------"

# 1. Get all users from ou=people (now authenticated using -D and -w)
USERS=$(ldapsearch -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -b "ou=people,$BASE_DN" -s one "(objectClass=inetOrgPerson)" uid mail -LLL)

# 2. Iterate through each user and find their group memberships
while read -r line; do
    if [[ $line =~ ^uid:\ (.*) ]]; then
        UID_VAL="${BASH_REMATCH[1]}"
        # Strip trailing carriage returns
        UID_VAL=$(echo "$UID_VAL" | tr -d '\r')
    elif [[ $line =~ ^mail:\ (.*) ]]; then
        MAIL_VAL="${BASH_REMATCH[1]}"
        MAIL_VAL=$(echo "$MAIL_VAL" | tr -d '\r')
        
        # Now search which groups contain this user's DN (also authenticated)
        USER_DN="uid=${UID_VAL},ou=people,${BASE_DN}"
        GROUPS=$(ldapsearch -x -H "$LDAP_URI" -D "$BIND_DN" -w "$ADMIN_PW" -b "ou=groups,${BASE_DN}" "(member=${USER_DN})" cn -LLL | grep '^cn:' | awk '{print $2}' | paste -sd, -)
        
        # If no groups found, mark as None
        if [ -z "$GROUPS" ]; then
            GROUPS="None"
        fi
        
        # Print formatted row
        printf "%-15s | %-20s | %-30s\n" "${UID_VAL}" "${GROUPS}" "${MAIL_VAL}"
    fi
done <<< "$USERS"

echo -e "${BOLD}========================================================================${NC}"
