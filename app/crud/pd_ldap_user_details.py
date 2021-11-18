import ldap
from app.utilities.config import settings
from fastapi import HTTPException


def get_ldap_user_details(user_id):
    server = settings.LDAP_SERVER
    base = "dc=quintiles,dc=net"
    scope = ldap.SCOPE_SUBTREE
    l_filter = f"(&(objectClass=user)(EmployeeID={user_id}))"
    attrs = ["*"]

    l_init = ldap.initialize(server)
    l_init.protocol_version = 3
    l_init.set_option(ldap.OPT_REFERRALS, 0)

    l_init.simple_bind_s(settings.LDAP_USERNAME, settings.LDAP_PWD)
    r = l_init.search(base, scope, l_filter, attrs)
    _, user = l_init.result(r, 60)

    name, attrs = user[0]
    if type(attrs) is not dict:
        raise HTTPException(
            status_code=403,
            detail=f"No record found for userId: {user_id}"
        )

    default_value = [b""]
    user_details = {
        "userId": bytes.decode(attrs.get("sAMAccountName", default_value)[0]),
        "first_name": bytes.decode(attrs.get("givenName", default_value)[0]),
        "last_name": bytes.decode(attrs.get("sn", default_value)[0]),
        "email": bytes.decode(attrs.get("mail", default_value)[0]),
        "country": bytes.decode(attrs.get("co", default_value)[0])
    }
    return user_details
