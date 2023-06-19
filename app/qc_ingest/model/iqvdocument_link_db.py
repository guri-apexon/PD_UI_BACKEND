from sqlalchemy import Column,and_, DateTime
from .__base__ import SchemaBase, schema_to_dict, update_link_index, CurdOp, update_existing_props,MissingParamException, get_utc_datetime
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER,BOOLEAN,TIMESTAMP,FLOAT
import uuid
from .iqvpage_roi_db import IqvpageroiDb
from .pd_meta_entity_mapping_lookup import insert_meta_entity
from .documentparagraphs_db import DocumentparagraphsDb
from app.config import SOURCE
import logging

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
    link_id_level2 = Column(TEXT, default='')
    link_id_level3 = Column(TEXT, default='')
    link_id_level4 = Column(TEXT, default='')
    link_id_level5 = Column(TEXT, default='')
    link_id_level6 = Column(TEXT, default='')
    link_id_subsection1 = Column(TEXT)
    link_id_subsection2 = Column(TEXT)
    link_id_subsection3 = Column(TEXT)
    hierarchy = Column(VARCHAR(128), nullable=False)
    iqv_standard_term = Column(TEXT)
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    LinkType = Column(TEXT)
    DocumentSequenceIndex = Column(INTEGER, nullable=False)
    LinkPage = Column(INTEGER, nullable=False, default=1)
    LinkLevel = Column(INTEGER, nullable=False)
    LinkText = Column(TEXT)
    LinkPrefix = Column(TEXT)
    userId = Column(VARCHAR(100))
    last_updated = Column(DateTime(timezone=True), nullable=True)
    num_updates = Column(INTEGER, default=0)
    predicted_term = Column(TEXT,default='')
    predicted_term_confidence = Column(FLOAT,default=0.0)
    predicted_term_source_system = Column(TEXT,default='')
    predicted_term_system_version = Column(TEXT,default='')
    para_id = Column(TEXT,default='')


    @staticmethod
    def get_link_id(session,data):
        link_query='SELECT * FROM iqvdocumentlink_db'+' WHERE '
        if not data.get('link_level',None):
            raise MissingParamException(" link_level ")
        link_list,link_level=[],data['link_level']
        for link_key in LINKS_INFO:
            if data.get(link_key,None):
                lk_str=f' "{link_key}" = \'{data[link_key]}\' '
                link_list.append(lk_str) 
        link_str=" AND ".join(link_list)
        link_query+=link_str + ' AND '+f'"LinkLevel" = \'{link_level}\''
        link_obj_list= session.execute(link_query)
        link_obj,count=None,0
        for obj in link_obj_list:
            link_obj=obj
            count+=1
        if count!=1:
            logging.error("Cant find unique link record with requested payload ")
        return IqvdocumentlinkDb(**link_obj)
    
    @staticmethod
    def get_line_id_for_top_link(session,link_id):
        """
        
        """
        obj_list=session.query(IqvpageroiDb.id,IqvpageroiDb.DocumentSequenceIndex).filter(and_(IqvpageroiDb.link_id == link_id,
                                                        IqvpageroiDb.link_id_level2 == '',
                                                        IqvpageroiDb.link_id_level3 == '',
                                                        IqvpageroiDb.link_id_level4 == '',
                                                        IqvpageroiDb.link_id_level5 == '',
                                                        IqvpageroiDb.link_id_level6 == '',
                                                        IqvpageroiDb.group_type.in_(('DocumentParagraphs','DocumentTables')),
                                                        IqvpageroiDb.hierarchy.in_(('paragraph','table'))
                                                        )
                                                   ).all()
        min_seq_id,best_match_id=1e10,None
        for obj_id,obj_sequence_id in obj_list:
            if obj_sequence_id<min_seq_id:
                min_seq_id=obj_sequence_id
                best_match_id=obj_id            
        return best_match_id
    
    @staticmethod
    def get_curr_segment_info(session,data):
        """
        get segment information either from current or next segment
        """
        curr_dict={}
        if data.get('prev_detail') and data['prev_detail']['link_id']:
            prev_data = IqvdocumentlinkDb.get_link_id(session,data['prev_detail'])
            curr_dict = schema_to_dict(prev_data)
            curr_dict['DocumentSequenceIndex']=curr_dict['DocumentSequenceIndex']+1
            if not data.get('prev_id',None):
                data['prev_id']=IqvdocumentlinkDb.get_line_id_for_top_link(session, data['prev_detail']['link_id'])
            
        else:
            next_data = IqvdocumentlinkDb.get_link_id(session,data['next_detail'])
            curr_dict = schema_to_dict(next_data)
            if not data.get('next_id',None):
                data['next_id']=IqvdocumentlinkDb.get_line_id_for_top_link(session, data['next_detail']['link_id'])
        return curr_dict
        
    @staticmethod
    def create(session, data):
        """
        update document paragraph and childbox.
        data : prev data

        """
        if data.get('is_section_completely_new') == True:
            para_data = IqvdocumentlinkDb()
            _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
            data['uuid'] = para_data.id = para_data.link_id = _id
            para_data.DocumentSequenceIndex = 0
            para_data.LinkLevel = 1
            para_data.doc_id = para_data.parent_id = data.get('doc_id')
            para_data.userId = data.get('userId')
        else:
            curr_dict=IqvdocumentlinkDb.get_curr_segment_info(session,data)
            para_data = IqvdocumentlinkDb(**curr_dict)
            _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
            data['uuid'] = _id
            #if link level not mentioned add at same level of 
            link_level= data['link_level'] if data.get("link_level",None) else para_data.LinkLevel
            link_str=LINKS_INFO[int(link_level)-1]
            setattr(para_data,link_str,_id)
            data[link_str]=_id
            update_existing_props(para_data, data)
            para_data.LinkLevel = data.get('link_level', para_data.LinkLevel)
            para_data.id = _id
            doc_id = para_data.doc_id
            para_data.parent_id=doc_id
            update_link_index(session, IqvdocumentlinkDb.__tablename__,
                            doc_id, para_data.DocumentSequenceIndex, CurdOp.CREATE)
        para_data.hierarchy = 'document'
        para_data.group_type = 'DocumentLinks'
        para_data.LinkType = 'toc'
        para_data.LinkPrefix = data.get('link_prefix', '')
        para_data.LinkText = data.get('link_text', '')
        para_data.iqv_standard_term = iqv_standard_term = data.get('iqv_standard_term','')
        source_system = ""
        if iqv_standard_term != "":
            source_system = SOURCE
        para_data.predicted_term_source_system = source_system
        para_data.last_updated = get_utc_datetime()
        para_data.num_updates = 0
        session.add(para_data)
        data['is_link']=True
        if not data['content']:
            data['content']=para_data.LinkPrefix+para_data.LinkText
        return data

    @staticmethod
    def update(session, data):
        """
        """
        obj=IqvdocumentlinkDb.get_link_id(session,data)
        if not obj:
            raise Exception(f'unable to find link object ')
        if not data.get('id',None):
            data['id']=IqvdocumentlinkDb.get_line_id_for_top_link(session,data['link_id'])
        link_text= data.get('link_text','')
        link_prefix= data.get('link_prefix','')
        iqv_standard_term = data.get('iqv_standard_term','')
        user_id = data.get('userId','')
        last_updated = get_utc_datetime()
        source_system = '' if obj.predicted_term_source_system == None else obj.predicted_term_source_system
        if iqv_standard_term != obj.iqv_standard_term:
            if source_system.startswith('NLP') or source_system in '':
                category = 'header'
                if int(data.get('link_level')) >1:
                    if iqv_standard_term.startswith('cpt_assessments'):
                        category = 'assessments'
                    else:
                        category = 'subheader'
                insert_meta_entity(session, category, link_text, iqv_standard_term)
            source_system = SOURCE
        if data.get('content',None):
            data['content'] = link_text
        link_obj = session.query(IqvdocumentlinkDb).filter(IqvdocumentlinkDb.id == obj.id).first()
        link_obj.LinkText = link_text
        link_obj.LinkPrefix = link_prefix
        link_obj.iqv_standard_term = iqv_standard_term
        link_obj.userId = user_id
        link_obj.predicted_term_source_system = source_system
        link_obj.last_updated = last_updated
        link_obj.num_updates = link_obj.num_updates + 1
        session.add(link_obj)

    @staticmethod
    def delete(session, data):
        if data.get('is_section_header') == False or data.get('delete_section_header') == True:
            obj=IqvdocumentlinkDb.get_link_id(session,data)
            if not obj:
                raise Exception(f'unable to find link object ')
            sequence_id = obj.DocumentSequenceIndex
            doc_id = obj.doc_id
            if not data.get('id',None):
                data['id']=IqvdocumentlinkDb.get_line_id_for_top_link(session,data['link_id'])
            update_link_index(session, IqvdocumentlinkDb.__tablename__, doc_id,
                            sequence_id, CurdOp.DELETE)
            sql_query = f'DELETE FROM {IqvdocumentlinkDb.__tablename__} WHERE "id"=\'{obj.id}\''
            session.execute(sql_query)

