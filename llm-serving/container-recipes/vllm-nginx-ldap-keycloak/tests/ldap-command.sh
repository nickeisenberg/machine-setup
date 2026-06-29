ldapsearch -x \
  -H ldap://localhost:1389 \
  -D "cn=admin,dc=nv,dc=doe,dc=gov" \
  -w adminpassword \
  -b "dc=company,dc=nv,dc=doe,dc=gov"
