from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class DocumentitemsDb(SchemaBase):
   __tablename__ = "documentitems_db"
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
   hierarchy = Column(VARCHAR(128),primary_key=True,nullable=False)
   iqv_standard_term = Column(TEXT)
   parent_id = Column(TEXT)
   group_type = Column(TEXT)
   strText = Column(TEXT)
   strTextTranslated = Column(TEXT)
   DocumentSequenceIndex = Column(INTEGER,nullable=False)
   hAlignmentVal = Column(INTEGER,nullable=False)
   RotationCorrectionDegrees = Column(DOUBLE_PRECISION,nullable=False)
   m_WORD_LAYOUTVal = Column(INTEGER,nullable=False)
   m_ROI_TYPEVal = Column(INTEGER,nullable=False)
   BulletTypeVal = Column(INTEGER,nullable=False)
   BulletIndentationLevel = Column(INTEGER,nullable=False)
   m_PARENT_ROI_TYPEVal = Column(INTEGER,nullable=False)
   HeaderSequence = Column(INTEGER,nullable=False)
   FooterSequence = Column(INTEGER,nullable=False)
   ImageIndex = Column(INTEGER,nullable=False)
   DocumentRelId = Column(TEXT)
   PageSequenceIndex = Column(INTEGER,nullable=False)
   PageID = Column(TEXT)
   UncorrectedImageFilename = Column(TEXT)
   ImageFormatVal = Column(TEXT)
   bOutputImageCreated = Column(BOOLEAN,nullable=False)
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
   bIsImage = Column(BOOLEAN,nullable=False)
   Hue = Column(INTEGER,nullable=False)
   Rotation_MajorAxis = Column(INTEGER,nullable=False)
   htmlTagType = Column(TEXT)
   textTypeVal = Column(INTEGER,nullable=False)
   contentTypeVal = Column(INTEGER,nullable=False)
   bNoTranslate = Column(BOOLEAN,nullable=False)
   SegmentationType = Column(INTEGER,nullable=False)
   TranslatedTextNoSegmentation = Column(TEXT)
   SegmentationMethodVal = Column(INTEGER,nullable=False)
   TranslationMethod1 = Column(TEXT)
   TranslationMatch = Column(DOUBLE_PRECISION,nullable=False)
   imagePaddingPixels = Column(DOUBLE_PRECISION,nullable=False)
   imageScaling = Column(DOUBLE_PRECISION,nullable=False)
   IsTableCell = Column(BOOLEAN,nullable=False)
   tableCell_pageIndex = Column(INTEGER,nullable=False)
   tableCell_rowIndex = Column(INTEGER,nullable=False)
   bIsSharedString = Column(BOOLEAN,nullable=False)
   tableCell_SharedStringIndex = Column(INTEGER,nullable=False)
   tableCell_SheetRowIndex = Column(INTEGER,nullable=False)
   tableCell_SheetColIndex = Column(INTEGER,nullable=False)
   tableCell_colIndex = Column(INTEGER,nullable=False)
   tableCell_SheetName = Column(TEXT)
   tableCell_SheetCellReference = Column(TEXT)
   OriginalROIWidthInches = Column(DOUBLE_PRECISION,nullable=False)
   OriginalROIHeightInches = Column(DOUBLE_PRECISION,nullable=False)
   HorizontalResolution = Column(DOUBLE_PRECISION,nullable=False)
   VerticalResolution = Column(DOUBLE_PRECISION,nullable=False)
   rectangle_x = Column(INTEGER,nullable=False)
   rectangle_y = Column(INTEGER,nullable=False)
   rectangle_width = Column(INTEGER,nullable=False)
   rectangle_height = Column(INTEGER,nullable=False)
   parentrectangle_x = Column(INTEGER,nullable=False)
   parentrectangle_y = Column(INTEGER,nullable=False)
   parentrectangle_width = Column(INTEGER,nullable=False)
   parentrectangle_height = Column(INTEGER,nullable=False)
   rectangleGlobalLocationOnPage_x = Column(INTEGER,nullable=False)
   rectangleGlobalLocationOnPage_y = Column(INTEGER,nullable=False)
   rectangleGlobalLocationOnPage_width = Column(INTEGER,nullable=False)
   rectangleGlobalLocationOnPage_height = Column(INTEGER,nullable=False)
   IsCopyOfRoiId = Column(TEXT)
   bIsCheckbox = Column(BOOLEAN,nullable=False)
   bIsChecked = Column(BOOLEAN,nullable=False)
   CheckboxFill = Column(DOUBLE_PRECISION,nullable=False)
   bScannedOCR = Column(BOOLEAN,nullable=False)
   scannedOCRCode = Column(TEXT)
   SequenceID = Column(INTEGER,nullable=False)
   SlideRelationshipId = Column(TEXT)
   SlideIndex = Column(INTEGER,nullable=False)
   Value = Column(TEXT)
   Score = Column(DOUBLE_PRECISION,nullable=False)
   GT_TextMatch = Column(TEXT)
   GT_ScoreMatch = Column(DOUBLE_PRECISION,nullable=False)
   GT_ImageFilename = Column(TEXT)

# Index('documentitems_db_doc_id',DocumentitemsDb.doc_id)
# Index('documentitems_db_doc_id_hierarchy',DocumentitemsDb.doc_id,DocumentitemsDb.hierarchy)
# Index('documentitems_db_iqv_standard_term',DocumentitemsDb.iqv_standard_term)
# Index('documentitems_db_link_id',DocumentitemsDb.link_id)
# Index('documentitems_db_link_id_level2',DocumentitemsDb.link_id_level2)
# Index('documentitems_db_link_id_level3',DocumentitemsDb.link_id_level3)
# Index('documentitems_db_link_id_level4',DocumentitemsDb.link_id_level4)
# Index('documentitems_db_link_id_level5',DocumentitemsDb.link_id_level5)
# Index('documentitems_db_link_id_level6',DocumentitemsDb.link_id_level6)
# Index('documentitems_db_link_id_subsection1',DocumentitemsDb.link_id_subsection1)
# Index('documentitems_db_link_id_subsection2',DocumentitemsDb.link_id_subsection2)
# Index('documentitems_db_link_id_subsection3',DocumentitemsDb.link_id_subsection3)
# Index('documentitems_db_parent_id',DocumentitemsDb.parent_id,DocumentitemsDb.group_type)
# Index('documentitems_db_parent_id_hierarchy',DocumentitemsDb.parent_id,DocumentitemsDb.hierarchy,DocumentitemsDb.group_type)
