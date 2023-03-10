from sqlalchemy import Column
from .__base__ import SchemaBase, schema_to_dict, update_roi_index, CurdOp, update_existing_props
from . import DocumentparagraphsDb
import uuid
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

   @staticmethod
   def create(session, data):
      """
      update document paragraph and childbox.
      data : prev data

      """
      cid, is_top_elm = None, False
      # if at top next element props are taken
      if data['prev_id']:
         cid = data['prev_id']
      else:
         cid = data['id']
         is_top_elm = True

      prev_data = session.query(DocumentparagraphsDb).filter(
          DocumentparagraphsDb.id == cid).first()
      if not prev_data:
         _id = data['prev_id']
         raise Exception(f'{_id} is missing from paragraph db')
      prev_dict = schema_to_dict(prev_data)
      para_data = DocumentparagraphsDb(**prev_dict)
      _id = data['uuid'] if data.get('uuid', None) else str(uuid.uuid4())
      update_existing_props(para_data, data)
      para_data.hierarchy = 'paragraph'
      para_data.group_type = 'DocumentParagraphs'
      para_data.m_ROI_TYPEVal=100 #image
      para_data.id = _id
      para_data.DocumentSequenceIndex = 0 if is_top_elm else prev_data.DocumentSequenceIndex+1
      para_data.SequenceID = 0 if is_top_elm else prev_data.SequenceID+1
      doc_id = prev_data.doc_id
      para_data.parent_id = doc_id
      update_roi_index(session, doc_id, prev_data.SequenceID, CurdOp.CREATE)

      binary_obj = IqvdocumentimagebinaryDb()
      update_existing_props(binary_obj, prev_dict)
      binary_obj.id = str(uuid.uuid4())
      binary_obj.img = base64.b64decode(data['content'])
      binary_obj.para_id = para_data.id
      binary_obj.childbox_id = para_data.id
      session.add(para_data)
      session.add(binary_obj)
      return data
#

   @staticmethod
   def update(session, data):
      """
      """
      obj = session.query(IqvdocumentimagebinaryDb).filter(
          IqvdocumentimagebinaryDb.para_id == data['id']).first()
      if not obj:
         _id = data['id']
         raise Exception(f'{_id} is missing from paragraph and imagebinary db')
      obj.img = base64.b64decode(data['content'])
      session.add(obj)

   @staticmethod
   def get(id, hierachy):
      pass

   @staticmethod
   def delete(session, data):
      obj = session.query(DocumentparagraphsDb).filter(
          DocumentparagraphsDb.id == data['id']).first()
      if not obj:
         _id = data['id']
         raise Exception(f'{_id} is missing from paragraph db')
      sequence_id = obj.SequenceID
      doc_id = obj.doc_id
      session.delete(obj)
      update_roi_index(session, doc_id, sequence_id, CurdOp.DELETE)
      session.query(IqvdocumentimagebinaryDb).filter(
          IqvdocumentimagebinaryDb.para_id == data['id']).delete()
