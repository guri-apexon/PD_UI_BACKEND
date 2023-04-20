from sqlalchemy import Column,Index, DateTime
from .__base__ import SchemaBase,schema_to_dict,update_partlist_index,CurdOp,update_existing_props,MissingParamException, update_link_update_details
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER
import uuid
from datetime import datetime


class DocumentpartslistDb(SchemaBase):
    __tablename__ = "documentpartslist_db"
    id = Column(VARCHAR(128),primary_key=True,nullable=False)
    doc_id = Column(TEXT)
    link_id = Column(TEXT)
    link_id_level2 = Column(TEXT)
    link_id_level3 = Column(TEXT)
    link_id_level4 = Column(TEXT)
    link_id_level5 = Column(TEXT)
    link_id_level6 = Column(TEXT)
    link_id_subsection1 = Column(TEXT)
    link_id_subsection2 = Column(TEXT)
    link_id_subsection3 = Column(TEXT)
    hierarchy = Column(VARCHAR(128),nullable=False)
    iqv_standard_term = Column(TEXT)
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    sequence_id = Column(INTEGER,nullable=False)
    userId = Column(VARCHAR(100))
    last_updated = Column(DateTime(timezone=True),
                            default=datetime.utcnow, nullable=False)
    num_updates = Column(INTEGER, default=1)
   
    @staticmethod
    def create(session,data):
        """
        update document paragraph and childbox.
        data : prev data

        return : updated data that may be used in next stage update
        """
        cid,is_next_elm=None,False

        if data['prev_id']:
            cid=data['prev_id']
        else:
            cid=data.get('next_id','')
            is_next_elm=True
        if not cid and data['is_link']:
            return data
        
        prev_data=session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == cid).first()
        if not prev_data:
            raise MissingParamException(f'{cid} in document partlist db ')
        prev_dict=schema_to_dict(prev_data)
        para_data = DocumentpartslistDb(**prev_dict)
        _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
        data['uuid']=_id
        update_existing_props(para_data,data)
        para_data.hierarchy = 'document'
        para_data.group_type = 'DocumentPartsList'
        para_data.id = _id
        para_data.sequence_id=prev_data.sequence_id-1 if is_next_elm else prev_data.sequence_id+1
        doc_id=prev_data.doc_id
        para_data.parent_id = doc_id
        update_partlist_index(session, DocumentpartslistDb.__tablename__,doc_id,para_data.sequence_id, CurdOp.CREATE) 
        if data.get('type') != 'header' and data.get('link_level') != '1':
            update_link_update_details(session, para_data.link_id, para_data.userId, para_data.last_updated) 
        session.add(para_data)
        return data
    
    @staticmethod
    def update(session,data):
        """
        """
        obj = session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == data['id']).first()
        if not obj:
            _id=data['id']
            raise MissingParamException(f'{_id} in document partlist db ')     
        update_existing_props(obj,data)
        obj.userId = data.get('userId')
        obj.last_updated = datetime.utcnow()
        obj.num_updates = obj.num_updates + 1
        session.add(obj)
        if data.get('type') != 'header' and data.get('link_level') != '1':
            update_link_update_details(session, obj.link_id, obj.userId, obj.last_updated)

    @staticmethod
    def delete(session, data):
        obj = session.query(DocumentpartslistDb).filter(
            DocumentpartslistDb.id == data['id']).first()
        if not obj:
            _id=data['id']
            raise MissingParamException(f'{_id} in document partlist db ')
        sequence_id = obj.sequence_id
        doc_id=obj.doc_id
        if data.get('type') != 'header' and data.get('link_level') != '1':
            update_link_update_details(session, obj.link_id, data.get('userId'), datetime.utcnow())
        session.delete(obj)
        update_partlist_index(session, DocumentpartslistDb.__tablename__,doc_id,
                        sequence_id, CurdOp.DELETE)
