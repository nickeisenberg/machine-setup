ldapadd -x \
  -H ldap://localhost:1389 \
  -D "cn=admin,dc=company,dc=local" \
  -w adminpassword \
  -f ./jane.ldif
