ldapsearch -x \
  -H ldap://localhost:1389 \
  -D "cn=admin,dc=company,dc=local" \
  -w adminpassword \
  -b "dc=company,dc=local"
