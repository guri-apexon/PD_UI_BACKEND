

from sqlalchemy import Column, Index
from .__base__ import SchemaBase, schema_to_dict, update_link_index, CurdOp, update_existing_props
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER
import uuid

class IqvdocumentlinkDb(SchemaBase):
    __tablename__ = "iqvdocumentlink_db"
    id = Column(VARCHAR(128), primary_key=True, nullable=False)
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
    hierarchy = Column(VARCHAR(128), nullable=False)
    iqv_standard_term = Column(TEXT)
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    LinkType = Column(TEXT)
    DocumentSequenceIndex = Column(INTEGER, nullable=False)
    LinkPage = Column(INTEGER, nullable=False)
    LinkLevel = Column(INTEGER, nullable=False)
    LinkText = Column(TEXT)
    LinkPrefix = Column(TEXT)

    @staticmethod
    def create(session, data):
        """
        update document paragraph and childbox.
        data : prev data

        """
        cid, is_top_elm = None, False
        # if at top next element props are taken
        if data['prev_link_record_uid']:
            cid = data['prev_link_record_uid']
        else:
            cid = data['link_record_uid']
            is_top_elm = True
        if not cid:
            raise Exception("Missing previous or current Id ")
        prev_data = session.query(IqvdocumentlinkDb).filter(
            IqvdocumentlinkDb.id == cid).first()
        if not prev_data:
            _id = data['prev_id']
            raise Exception(f'{_id} is missing from paragraph db')
        prev_dict = schema_to_dict(prev_data)
        para_data = IqvdocumentlinkDb(**prev_dict)
        _id = data['uuid'] if data.get('uuid', None) else str(uuid.uuid4())
        data['uuid'] = _id
        para_data.link_id = str(uuid.uuid4())
        update_existing_props(para_data, data)
        para_data.hierarchy = 'document'
        para_data.group_type = 'DocumentLinks'
        para_data.LinkType = 'toc'
        para_data.LinkPrefix = data.get('link_prefix', '')
        para_data.LinkText = data.get('link_text', '')
        para_data.LinkLevel = data.get('link_level', '')
        para_data.id = _id
        para_data.parent_id = _id

        para_data.DocumentSequenceIndex = 0 if is_top_elm else prev_data.DocumentSequenceIndex+1
        doc_id = prev_data.doc_id
        update_link_index(session, IqvdocumentlinkDb.__tablename__,
                          doc_id, prev_data.DocumentSequenceIndex, CurdOp.CREATE)
        session.add(para_data)
        data['link_id'] = para_data.link_id
        return data

    @staticmethod
    def update(session, data):
        """
        """
        obj = session.query(IqvdocumentlinkDb).filter(
            IqvdocumentlinkDb.id == data['id']).first()
        if not obj:
            _id = data['id']
            raise Exception(f'{_id} is missing from paragraph ')
        update_existing_props(obj, data)
        obj.LinkPrefix = data.get('link_prefix', '')
        obj.LinkText = data.get('link_text', '')
        obj.LinkLevel = data.get('link_level', '')
        session.add(obj)

    @staticmethod
    def delete(session, data):
        obj = session.query(IqvdocumentlinkDb).filter(
            IqvdocumentlinkDb.id == data['id']).first()
        if not obj:
            _id = data['id']
            raise Exception(f'{_id} is missing from paragraph db')
        sequence_id = obj.DocumentSequenceIndex
        doc_id = obj.doc_id
        update_link_index(session, IqvdocumentlinkDb.__tablename__, doc_id,
                          sequence_id, CurdOp.DELETE)
        session.delete(obj)


Index('iqvdocumentlink_db_doc_id', IqvdocumentlinkDb.doc_id)
Index('iqvdocumentlink_db_doc_id_hierarchy',
      IqvdocumentlinkDb.doc_id, IqvdocumentlinkDb.hierarchy)
Index('iqvdocumentlink_db_iqv_standard_term',
      IqvdocumentlinkDb.iqv_standard_term)
Index('iqvdocumentlink_db_link_id', IqvdocumentlinkDb.link_id)
Index('iqvdocumentlink_db_link_id_level2', IqvdocumentlinkDb.link_id_level2)
Index('iqvdocumentlink_db_link_id_level3', IqvdocumentlinkDb.link_id_level3)
Index('iqvdocumentlink_db_link_id_level4', IqvdocumentlinkDb.link_id_level4)
Index('iqvdocumentlink_db_link_id_level5', IqvdocumentlinkDb.link_id_level5)
Index('iqvdocumentlink_db_link_id_level6', IqvdocumentlinkDb.link_id_level6)
Index('iqvdocumentlink_db_link_id_subsection1',
      IqvdocumentlinkDb.link_id_subsection1)
Index('iqvdocumentlink_db_link_id_subsection2',
      IqvdocumentlinkDb.link_id_subsection2)
Index('iqvdocumentlink_db_link_id_subsection3',
      IqvdocumentlinkDb.link_id_subsection3)
Index('iqvdocumentlink_db_parent_id',
      IqvdocumentlinkDb.parent_id, IqvdocumentlinkDb.group_type)
Index('iqvdocumentlink_db_parent_id_hierarchy', IqvdocumentlinkDb.parent_id,
      IqvdocumentlinkDb.hierarchy, IqvdocumentlinkDb.group_type)
