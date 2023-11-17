class AuthorizationKerberosException(Exception):
    def __init__(self, msg=""):
        super().__init__(f"Authorization Kerberos Exception: {msg}")


class AuthorizationLDAPException(Exception):
    def __init__(self, msg=""):
        super().__init__(f"Authorization LDAP Exception: {msg}")
