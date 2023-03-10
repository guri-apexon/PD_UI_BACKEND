

from sqlalchemy import Column, Index
from .__base__ import SchemaBase, schema_to_dict, update_link_index, CurdOp, update_existing_props
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER,BOOLEAN,TIMESTAMP
from datetime import datetime
import uuid


LINKS_INFO = ["link_id",
              "link_id_level2",
              "link_id_level3",
              "link_id_level4",
              "link_id_level5",
              "link_id_level6",
              "link_id_subsection1",
              "link_id_subsection2",
              "link_id_subsection3"]

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
    def get_link_id(session,data):
        link_query='SELECT * FROM iqvdocumentlink_db'+' WHERE '
        link_list,link_level=[],0
        for link_key in LINKS_INFO:
            if data.get(link_key,None):
                lk_str=f' "{link_key}" = \'{data[link_key]}\' '
                if 'subsection' not in link_key:
                    link_level+=1
                link_list.append(lk_str) 
        link_str=" AND ".join(link_list)
        link_query+=link_str + ' AND '+f'"LinkLevel" = \'{link_level}\''
        link_obj_list= session.execute(link_query)
        link_obj,count=None,0
        for obj in link_obj_list:
            link_obj=obj
            count+=1
        if count!=1:
            raise Exception("Cant find unique link record with requested payload ")
        return IqvdocumentlinkDb(**link_obj)
    
    @staticmethod
    def is_top_link(data):
        top_elm=True
        for link_key in LINKS_INFO:
            if data.get(link_key,None):
                top_elm=False
                break
        return top_elm
    
    @staticmethod
    def create(session, data):
        """
        update document paragraph and childbox.
        data : prev data

        """
        cid, is_top_elm = None, False
        is_top_elm=IqvdocumentlinkDb.is_top_link(data['prev_detail']) if data.get('prev_detail',None) else True
        if not is_top_elm:
            prev_data = IqvdocumentlinkDb.get_link_id(session,data['prev_detail'])
            if not prev_data:
                raise Exception(f'cant find related link object ')
        else:
            prev_data=IqvdocumentlinkDb(id='',hierarchy='document',group_type='DocumentLinks',DocumentSequenceIndex=-1)
        prev_dict = schema_to_dict(prev_data)
        para_data = IqvdocumentlinkDb(**prev_dict)
        _id = data['uuid'] if data['uuid'] else str(uuid.uuid4())
        data['uuid'] = _id
        link_str=LINKS_INFO[para_data.LinkLevel-1]
        setattr(para_data,link_str,_id)
        update_existing_props(para_data, data)
        para_data.hierarchy = 'document'
        para_data.group_type = 'DocumentLinks'
        para_data.LinkType = 'toc'
        para_data.LinkPrefix = data.get('link_prefix', '')
        para_data.LinkText = data.get('link_text', '')
        para_data.LinkLevel = data.get('link_level', prev_data.LinkLevel)
        para_data.id = _id
        para_data.DocumentSequenceIndex = 0 if is_top_elm else prev_data.DocumentSequenceIndex+1
        doc_id = prev_data.doc_id
        para_data.parent_id=doc_id
        update_link_index(session, IqvdocumentlinkDb.__tablename__,
                          doc_id, prev_data.DocumentSequenceIndex, CurdOp.CREATE)
        session.add(para_data)
        data['is_link']=True
        if not data['content']:
            data['content']=para_data.LinkPrefix+' '+para_data.LinkText
        return data

    @staticmethod
    def update(session, data):
        """
        """
        obj=IqvdocumentlinkDb.get_link_id(session,data)
        if not obj:
            raise Exception(f'unable to find link object ')

        link_text= data['link_text'] if data.get('link_text',None) else obj.LinkText
        link_prefix= data['link_prefix'] if data.get('link_prefix',None) else obj.LinkPrefix
        
        sql = f'UPDATE {IqvdocumentlinkDb.__tablename__} SET "LinkText" = \'{link_text}\' , \
                    "LinkPrefix" = \'{link_prefix}\'  \
                      WHERE  "id" = \'{obj.id}\' '
        session.execute(sql)

    @staticmethod
    def delete(session, data):
        obj=IqvdocumentlinkDb.get_link_id(session,data)
        if not obj:
            raise Exception(f'unable to find link object ')
        sequence_id = obj.DocumentSequenceIndex
        doc_id = obj.doc_id
        update_link_index(session, IqvdocumentlinkDb.__tablename__, doc_id,
                          sequence_id, CurdOp.DELETE)
        sql_query = f'DELETE FROM {IqvdocumentlinkDb.__tablename__} WHERE "id"=\'{obj.id}\''
        session.execute(sql_query)

