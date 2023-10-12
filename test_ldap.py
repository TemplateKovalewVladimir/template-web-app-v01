# pylint: disable-next=E0611
from ldap import INVALID_CREDENTIALS, LDAPError, initialize

username = "vea"
password = ""


try:
    ldap_server = "ldap://aa.aliter.spb.ru"
    ldap_domain = "aa"

    conn = initialize(ldap_server)
    conn.simple_bind_s(username + "@" + ldap_domain, password)
except INVALID_CREDENTIALS:
    print("Неверное имя пользователя или пароль")
except LDAPError as e:
    print("LDAPError")
finally:
    del conn

print("OK")
