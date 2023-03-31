from sqlalchemy import Column, DateTime
from datetime import datetime
from .__base__ import SchemaBase, schema_to_dict, MissingParamException
from .user import get_user_name
from sqlalchemy.dialects.postgresql import TEXT


class IqvsectionlockDb(SchemaBase):
    __tablename__ = "iqvsectionlock_db"
    link_id = Column(TEXT, primary_key=True, nullable=False)
    doc_id = Column(TEXT)
    userId = Column(TEXT)
    user_name = Column(TEXT)
    last_updated = Column(DateTime(timezone=True),
                          default=datetime.utcnow, nullable=False)

    @staticmethod
    def get_record(session, data):
        """
        get existing section loked info
        """
        if not data.get('link_id', None):
            raise MissingParamException(f'link_id ')
        
        obj = session.query(IqvsectionlockDb).filter(
            IqvsectionlockDb.link_id == data['link_id']).first()
        if not obj:
            data['section_lock'] = True
            data['userId'] = ''
            data['user_name'] = ''
            data['last_updated'] = ''
        else:
            obj_dict = schema_to_dict(obj)
            data['section_lock'] = False
            data['userId'] = obj_dict['userId']
            data['user_name'] = obj_dict['user_name']
            data['last_updated'] = obj_dict['last_updated']
        return data

    @staticmethod
    def update_record(session, data):
        """
        update section locked info
        """
        if not data.get('link_id', None):
            raise MissingParamException(f'link_id ')
        
        if data.get('section_lock') == False:
            section_info = IqvsectionlockDb()
            section_info.link_id = data.get('link_id')
            section_info.doc_id = data.get('doc_id','')
            section_info.userId = user_id = data.get('userId','')
            user_name = get_user_name(session, user_id)
            section_info.user_name = user_name
            section_info.last_updated = data['last_updated'] = datetime.utcnow()
            session.add(section_info)
        else:
            obj = session.query(IqvsectionlockDb).filter(
                IqvsectionlockDb.link_id == data['link_id']).first()
            if not obj:
                MissingParamException("{0} in iqv section lock DB".format(data['link_id']))
            session.delete(obj)
        return data
