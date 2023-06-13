from sqlalchemy import Column,Index, DateTime, and_
from .__base__ import SchemaBase,schema_to_dict,update_partlist_index,CurdOp,update_existing_props,MissingParamException, get_utc_datetime
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER
import uuid
from .iqvpage_roi_db import IqvpageroiDb
from .documenttables_db import DocTableHelper
from datetime import datetime


class DocumentpartslistDb(SchemaBase):
    __tablename__ = "documentpartslist_db"
    id = Column(VARCHAR(128),primary_key=True,nullable=False)
    doc_id = Column(TEXT)
    link_id = Column(TEXT)
    link_id_level2 = Column(TEXT, default='')
    link_id_level3 = Column(TEXT, default='')
    link_id_level4 = Column(TEXT, default='')
    link_id_level5 = Column(TEXT, default='')
    link_id_level6 = Column(TEXT, default='')
    link_id_subsection1 = Column(TEXT)
    link_id_subsection2 = Column(TEXT)
    link_id_subsection3 = Column(TEXT)
    hierarchy = Column(VARCHAR(128),nullable=False)
    iqv_standard_term = Column(TEXT)
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    sequence_id = Column(INTEGER,nullable=False)
    userId = Column(VARCHAR(100))
    last_updated = Column(DateTime(timezone=True), nullable=True)
    num_updates = Column(INTEGER, default=0)
   
    @staticmethod
    def create(session,data):
        """
        update document paragraph and childbox.
        data : prev data

        return : updated data that may be used in next stage update
        """
        if data.get('is_section_completely_new') == True:
            para_data = DocumentpartslistDb()
            _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
            data['uuid'] = para_data.id = para_data.link_id = _id
            para_data.sequence_id = 0
            para_data.doc_id = para_data.parent_id = data.get('doc_id')
            para_data.userId = data.get('userId')
        else:
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
                prev_data = session.query(IqvpageroiDb).filter(IqvpageroiDb.id == cid).first()
                if prev_data.hierarchy == 'table':
                    doc_table_helper = DocTableHelper()
                    table_id = doc_table_helper.get_table_roi_id(session, cid)
                    prev_data=session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == table_id).first()
                else:
                    raise MissingParamException(f'{cid} in document partlist db ')
            prev_dict=schema_to_dict(prev_data)
            para_data = DocumentpartslistDb(**prev_dict)
            _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
            data['uuid']=_id
            update_existing_props(para_data,data)
            para_data.id = _id
            para_data.sequence_id=prev_data.sequence_id-1 if is_next_elm else prev_data.sequence_id+1
            doc_id=prev_data.doc_id
            para_data.parent_id = doc_id
            update_partlist_index(session, DocumentpartslistDb.__tablename__, doc_id, para_data.link_id, para_data.sequence_id, CurdOp.CREATE) 
        para_data.hierarchy = 'document'
        para_data.group_type = 'IQVDocumentParts' 
        para_data.last_updated = get_utc_datetime()
        para_data.num_updates = 0
        session.add(para_data)
        return data
    
    @staticmethod
    def update(session,data):
        """
        """
        if data.get('type') == 'table':
            _id = data.get('table_roi_id','')
            data['id'] = _id
        else:
            _id=data.get('id','')
        obj = session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == _id).first()
        if not obj:
            raise MissingParamException(f'{_id} in document partlist db ')     
        update_existing_props(obj,data)
        obj.userId = data.get('userId')
        obj.last_updated = get_utc_datetime()
        obj.num_updates = obj.num_updates + 1
        session.add(obj)

    @staticmethod
    def delete(session, data):
        if data.get('type') == 'table':
            _id = data.get('table_roi_id','')
        else:
            _id=data.get('id','')
        obj = session.query(DocumentpartslistDb).filter(
            DocumentpartslistDb.id == _id).first()
        if not obj:
            raise MissingParamException(f'{_id} in document partlist db ')
        session.delete(obj)
