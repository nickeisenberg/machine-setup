ldapadd -x \
  -H ldap://localhost:1389 \
  -D "cn=admin,dc=company" \
  -w adminpassword \
  -f ./users/admin.ldif
