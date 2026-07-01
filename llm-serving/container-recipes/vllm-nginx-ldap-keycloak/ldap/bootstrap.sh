#!/usr/bin/env bash

set -euo pipefail

ldapman init

ldapman config set ldap.directory openldap
ldapman config set ldap.uri ldap://localhost:1389
ldapman config set ldap.base_dn dc=nv,dc=doe,dc=gov
ldapman config set ldap.bind_dn cn=admin,dc=nv,dc=doe,dc=gov
ldapman config set ldap.bind_password adminpassword

ldapman ldap init

ldapman user add \
    admin \
    Admin \
    User \
    admin@nv.doe.gov \
    password123

ldapman user add \
    eisenbnt \
    Nicholas \
    Eisenberg \
    eisenbnt@nv.doe.gov \
    password123

ldapman group add general
ldapman group add vip

ldapman group add-user general admin
ldapman group add-user general eisenbnt
ldapman group add-user vip admin

ldapman sync
