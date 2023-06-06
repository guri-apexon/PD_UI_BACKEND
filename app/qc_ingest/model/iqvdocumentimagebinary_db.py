from sqlalchemy import Column, DateTime
from .__base__ import SchemaBase, schema_to_dict, update_roi_index, CurdOp, update_existing_props,MissingParamException, get_utc_datetime
from . import DocumentparagraphsDb
from .iqvpage_roi_db import IqvpageroiDb
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER, BYTEA
import base64


class IqvdocumentimagebinaryDb(SchemaBase):
   __tablename__ = "iqvdocumentimagebinary_db"
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
   para_id = Column(TEXT)
   childbox_id = Column(TEXT)
   pathfilename = Column(TEXT)
   height = Column(INTEGER)
   width = Column(INTEGER)
   sequence_id = Column(INTEGER)
   img = Column(BYTEA)
   image_format = Column(TEXT)
   userId = Column(VARCHAR(100))
   last_updated = Column(DateTime(timezone=True), nullable=True)
   num_updates = Column(INTEGER, default=0)

   @staticmethod
   def create(session, data):
      """
      update document paragraph and childbox.
      data : prev data

      """
      cid, is_next_elm = None, False
      # if at top next element props are taken
      if data['prev_id']:
         cid = data['prev_id']
      else:
         cid = data['next_id']
         is_next_elm = True

      prev_data = session.query(IqvpageroiDb).filter(
          IqvpageroiDb.id == cid).first()
      if not prev_data:
         raise MissingParamException(f'{cid} is missing from paragraph db')
      prev_dict = schema_to_dict(prev_data)
      para_data = DocumentparagraphsDb(**prev_dict)
      _id = data['uuid'] if data.get('uuid', None) else str(uuid.uuid4())
      update_existing_props(para_data, data)
      para_data.hierarchy = 'paragraph'
      para_data.group_type = 'DocumentParagraphs'
      para_data.m_ROI_TYPEVal=100 #image
      para_data.Value = para_data.strText = ''
      para_data.id = _id
      para_data.DocumentSequenceIndex = prev_data.DocumentSequenceIndex-1 if is_next_elm else prev_data.DocumentSequenceIndex+1
      para_data.SequenceID = prev_data.SequenceID-1 if is_next_elm else prev_data.SequenceID+1
      doc_id = prev_data.doc_id
      para_data.parent_id = doc_id
      para_data.last_updated = get_utc_datetime()
      para_data.num_updates = 0
      update_roi_index(session, doc_id, para_data.link_id , para_data.SequenceID, CurdOp.CREATE)

      binary_obj = IqvdocumentimagebinaryDb()
      update_existing_props(binary_obj, prev_dict)
      binary_obj.id = str(uuid.uuid4())
      content=data['content']
      idx=content.find(',')
      org_content=content[idx+1:]
      img_format=content[content.find('/')+1:content.find(';')]
      pad = len(org_content)%4
      org_content +=("="*pad)
      binary_obj.img = base64.b64decode(org_content.strip())
      binary_obj.image_format=img_format
      binary_obj.para_id = para_data.id
      binary_obj.childbox_id = para_data.id
      binary_obj.userId = data.get('userId', None)
      binary_obj.last_updated = get_utc_datetime()
      binary_obj.num_updates = 0
      session.add(para_data)
      session.add(binary_obj)
      return data
#

   @staticmethod
   def update(session, data):
      """
      """
      para_obj = session.query(DocumentparagraphsDb).filter(
          DocumentparagraphsDb.id == data['id']).first()
      if not para_obj:
         _id = data['id']
         raise MissingParamException(f'{_id} is missing from paragraph db')
      para_obj.userId = data.get('userId', None)
      para_obj.last_updated = get_utc_datetime()
      para_obj.num_updates = para_obj.num_updates + 1

      obj = session.query(IqvdocumentimagebinaryDb).filter(
          IqvdocumentimagebinaryDb.para_id == data['id']).first()
      if not obj:
         _id = data['id']
         raise MissingParamException(f'{_id} is missing from imagebinary db')
      content=data['content']
      idx=content.find(',')
      org_content=content[idx+1:]
      img_format=content[content.find('/')+1:content.find(';')]
      obj.img = base64.b64decode(org_content)
      obj.image_format = img_format
      obj.userId = data.get('userId', None)
      obj.last_updated = get_utc_datetime()
      obj.num_updates = obj.num_updates + 1
      session.add(para_obj)
      session.add(obj)


   @staticmethod
   def delete(session, data):
      obj = session.query(DocumentparagraphsDb).filter(
          DocumentparagraphsDb.id == data['id']).first()
      if not obj:
         _id = data['id']
         raise MissingParamException(f'{_id} is missing from paragraph db')
      session.delete(obj)
      session.query(IqvdocumentimagebinaryDb).filter(
          IqvdocumentimagebinaryDb.para_id == data['id']).delete()
