from pydantic import BaseModel


class LdapUserDetails(BaseModel):
    userId: str
    first_name: str
    last_name: str
    email: str
    country: str


class LdapUserRequest(BaseModel):
    userId: str


