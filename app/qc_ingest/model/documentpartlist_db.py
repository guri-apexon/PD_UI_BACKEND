from sqlalchemy import Column,Index
from .__base__ import SchemaBase,schema_to_dict,update_partlist_index,CurdOp,update_existing_props
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER
import uuid

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
   
    @staticmethod
    def create(session,data):
        """
        update document paragraph and childbox.
        data : prev data

        return : updated data that may be used in next stage update
        """
        cid,is_top_elm=None,False
        #if at top next element props are taken
       
        if data['prev_id']:
            cid=data['prev_id']
        else:
            cid=data.get('id','')
            is_top_elm=True
        if not cid and data['is_link']:
            return data
        
        prev_data=session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == cid).first()
        if not prev_data:
            _id=data['prev_id']
            raise Exception(f'{_id} is missing from partlist db')
        prev_dict=schema_to_dict(prev_data)
        para_data = DocumentpartslistDb(**prev_dict)
        _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
        data['uuid']=_id
        update_existing_props(para_data,data)
        para_data.hierarchy = 'document'
        para_data.group_type = 'DocumentPartsList'
        para_data.id = _id
        para_data.sequence_id=0 if is_top_elm else prev_data.sequence_id+1
        doc_id=prev_data.doc_id
        para_data.parent_id = doc_id
        update_partlist_index(session, DocumentpartslistDb.__tablename__,doc_id,prev_data.sequence_id, CurdOp.CREATE)  
        session.add(para_data)
        return data
    
    @staticmethod
    def update(session,data):
        """
        """
        obj = session.query(DocumentpartslistDb).filter(DocumentpartslistDb.id == data['id']).first()
        if not obj:
            _id=data['id']
            raise Exception(f'{_id} is missing from partlist db ')      
        update_existing_props(obj,data)
        session.add(obj)

    @staticmethod
    def delete(session, data):
        obj = session.query(DocumentpartslistDb).filter(
            DocumentpartslistDb.id == data['id']).first()
        if not obj:
            _id=data['id']
            raise Exception(f'{_id} is missing from partlist db')
        sequence_id = obj.sequence_id
        doc_id=obj.doc_id
        session.delete(obj)
        update_partlist_index(session, DocumentpartslistDb.__tablename__,doc_id,
                        sequence_id, CurdOp.DELETE)
