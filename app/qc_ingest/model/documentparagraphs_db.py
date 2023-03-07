from sqlalchemy import Column, Index
from .__base__ import SchemaBase, schema_to_dict, update_roi_index, CurdOp, update_existing_props
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN, BIGINT, JSONB, BYTEA
import uuid


class DocumentparagraphsDb(SchemaBase):
   __tablename__ = "documentparagraphs_db"
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
   hierarchy = Column(VARCHAR(128), primary_key=True, nullable=False)
   iqv_standard_term = Column(TEXT)
   parent_id = Column(TEXT)
   group_type = Column(TEXT)
   strText = Column(TEXT)
   strTextTranslated = Column(TEXT)
   DocumentSequenceIndex = Column(INTEGER, nullable=False)
   hAlignmentVal = Column(INTEGER, nullable=False)
   RotationCorrectionDegrees = Column(DOUBLE_PRECISION, nullable=False)
   m_WORD_LAYOUTVal = Column(INTEGER, nullable=False)
   m_ROI_TYPEVal = Column(INTEGER, nullable=False)
   BulletTypeVal = Column(INTEGER, nullable=False)
   BulletIndentationLevel = Column(INTEGER, nullable=False)
   m_PARENT_ROI_TYPEVal = Column(INTEGER, nullable=False)
   HeaderSequence = Column(INTEGER, nullable=False)
   FooterSequence = Column(INTEGER, nullable=False)
   ImageIndex = Column(INTEGER, nullable=False)
   DocumentRelId = Column(TEXT)
   PageSequenceIndex = Column(INTEGER, nullable=False)
   PageID = Column(TEXT)
   UncorrectedImageFilename = Column(TEXT)
   ImageFormatVal = Column(TEXT)
   bOutputImageCreated = Column(BOOLEAN, nullable=False)
   OutputImageFilename = Column(TEXT)
   OutputImageFilename_RotationCorrection = Column(TEXT)
   OutputImageFilename_RotationCorrectionToDropBox = Column(TEXT)
   OutputImageFilename_FinalImageProcessingOutput = Column(TEXT)
   OutputImageFilename_FinalImageProcessingOutputToDropBox = Column(TEXT)
   OutputImageFilename_OriginalSegment = Column(TEXT)
   OutputImageFilename_Segments = Column(TEXT)
   OutputImageFilename_SegmentsToDropBox = Column(TEXT)
   OutputImageFilename_Cleaned = Column(TEXT)
   OutputImageFilenameT = Column(TEXT)
   OutputImageFilenameTDropBox = Column(TEXT)
   bIsImage = Column(BOOLEAN, nullable=False)
   Hue = Column(INTEGER, nullable=False)
   Rotation_MajorAxis = Column(INTEGER, nullable=False)
   htmlTagType = Column(TEXT)
   textTypeVal = Column(INTEGER, nullable=False)
   contentTypeVal = Column(INTEGER, nullable=False)
   bNoTranslate = Column(BOOLEAN, nullable=False)
   SegmentationType = Column(INTEGER, nullable=False)
   TranslatedTextNoSegmentation = Column(TEXT)
   SegmentationMethodVal = Column(INTEGER, nullable=False)
   TranslationMethod1 = Column(TEXT)
   TranslationMatch = Column(DOUBLE_PRECISION, nullable=False)
   imagePaddingPixels = Column(DOUBLE_PRECISION, nullable=False)
   imageScaling = Column(DOUBLE_PRECISION, nullable=False)
   IsTableCell = Column(BOOLEAN, nullable=False)
   tableCell_pageIndex = Column(INTEGER, nullable=False)
   tableCell_rowIndex = Column(INTEGER, nullable=False)
   bIsSharedString = Column(BOOLEAN, nullable=False)
   tableCell_SharedStringIndex = Column(INTEGER, nullable=False)
   tableCell_SheetRowIndex = Column(INTEGER, nullable=False)
   tableCell_SheetColIndex = Column(INTEGER, nullable=False)
   tableCell_colIndex = Column(INTEGER, nullable=False)
   tableCell_SheetName = Column(TEXT)
   tableCell_SheetCellReference = Column(TEXT)
   OriginalROIWidthInches = Column(DOUBLE_PRECISION, nullable=False)
   OriginalROIHeightInches = Column(DOUBLE_PRECISION, nullable=False)
   HorizontalResolution = Column(DOUBLE_PRECISION, nullable=False)
   VerticalResolution = Column(DOUBLE_PRECISION, nullable=False)
   rectangle_x = Column(INTEGER, nullable=False)
   rectangle_y = Column(INTEGER, nullable=False)
   rectangle_width = Column(INTEGER, nullable=False)
   rectangle_height = Column(INTEGER, nullable=False)
   parentrectangle_x = Column(INTEGER, nullable=False)
   parentrectangle_y = Column(INTEGER, nullable=False)
   parentrectangle_width = Column(INTEGER, nullable=False)
   parentrectangle_height = Column(INTEGER, nullable=False)
   rectangleGlobalLocationOnPage_x = Column(INTEGER, nullable=False)
   rectangleGlobalLocationOnPage_y = Column(INTEGER, nullable=False)
   rectangleGlobalLocationOnPage_width = Column(INTEGER, nullable=False)
   rectangleGlobalLocationOnPage_height = Column(INTEGER, nullable=False)
   IsCopyOfRoiId = Column(TEXT)
   bIsCheckbox = Column(BOOLEAN, nullable=False)
   bIsChecked = Column(BOOLEAN, nullable=False)
   CheckboxFill = Column(DOUBLE_PRECISION, nullable=False)
   bScannedOCR = Column(BOOLEAN, nullable=False)
   scannedOCRCode = Column(TEXT)
   SequenceID = Column(INTEGER, nullable=False)
   SlideRelationshipId = Column(TEXT)
   SlideIndex = Column(INTEGER, nullable=False)
   Value = Column(TEXT)
   Score = Column(DOUBLE_PRECISION, nullable=False)
   GT_TextMatch = Column(TEXT)
   GT_ScoreMatch = Column(DOUBLE_PRECISION, nullable=False)
   GT_ImageFilename = Column(TEXT)

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
      para_data.id = _id
      para_data.parent_id = _id
      para_data.DocumentSequenceIndex = 0 if is_top_elm else prev_data.DocumentSequenceIndex+1
      para_data.SequenceID = 0 if is_top_elm else prev_data.SequenceID+1
      if data.get('content',None):
         para_data.Value=data['content']
      doc_id = prev_data.doc_id
      update_roi_index(session, DocumentparagraphsDb.__tablename__,
                       doc_id, prev_data.SequenceID, CurdOp.CREATE)
      session.add(para_data)
      return data
#

   @staticmethod
   def update(session, data):
      """
      """
      obj = session.query(DocumentparagraphsDb).filter(
          DocumentparagraphsDb.id == data['id']).first()
      if not obj:
         _id = data['id']
         raise Exception(f'{_id} is missing from paragraph ')
      update_existing_props(obj, data)
      if data.get('content',None):
         obj.Value=data['content']
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
      update_roi_index(session, DocumentparagraphsDb.__tablename__, doc_id,
                       sequence_id, CurdOp.DELETE)
