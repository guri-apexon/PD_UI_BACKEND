import ldap
from app import config
from fastapi import HTTPException


def get_ldap_user_details(user_id):
    server = config.LDAP_SERVER
    base = "dc=quintiles,dc=net"
    scope = ldap.SCOPE_SUBTREE
    l_filter = f"(&(objectClass=user)(sAMAccountName={user_id}))"
    attrs = ["*"]

    l = ldap.initialize(server)
    l.protocol_version = 3
    l.set_option(ldap.OPT_REFERRALS, 0)

    l.simple_bind_s(config.LDAP_USERNAME, config.LDAP_PWD)
    r = l.search(base, scope, l_filter, attrs)
    _, user = l.result(r, 60)

    name, attrs = user[0]
    if type(attrs) is not dict:
        raise HTTPException(
            status_code=403,
            detail=f"No record found for userId: {user_id}"
        )

    default_value = [b""]
    user_details = {
        "userId": user_id,
        "first_name": bytes.decode(attrs.get("givenName", default_value)[0]),
        "last_name": bytes.decode(attrs.get("sn", default_value)[0]),
        "email": bytes.decode(attrs.get("mail", default_value)[0]),
        "country": bytes.decode(attrs.get("co", default_value)[0])
    }
    return user_details
