from sqlalchemy import Column, Index
from .__base__ import SchemaBase, MissingParamException
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN, BIGINT, JSONB, BYTEA, TIMESTAMP


class User(SchemaBase):
    __tablename__ = "user"
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(VARCHAR(200))
    last_name = Column(VARCHAR(100))
    country = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    username = Column(VARCHAR(100))
    date_of_registration = Column(TIMESTAMP, nullable=False)
    login_id = Column(INTEGER)
    user_type = Column(VARCHAR(100))
    lastUpdated = Column(TIMESTAMP)
    reason_for_change = Column(VARCHAR(1000))
    new_document_version = Column(BOOLEAN)
    edited = Column(BOOLEAN)
    qc_complete = Column(BOOLEAN)


def get_user_name(session, user_id):
    user_name = ''
    obj = session.query(User).filter(
        User.username.ilike("%" + user_id + "%")).first()
    if not obj:
        MissingParamException("{0} user_id in User DB".format(user_id))
    user_name = obj.first_name + ' ' + obj.last_name
    return user_name
