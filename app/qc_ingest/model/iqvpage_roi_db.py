
from sqlalchemy import Column, DateTime
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,FLOAT
from datetime import datetime

class IqvpageroiDb(SchemaBase):
   __tablename__ = "iqvpageroi_db"
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
   userId = Column(VARCHAR(100))
   last_updated = Column(DateTime(timezone=True),
                          default=datetime.utcnow, nullable=False)
   num_updates = Column(INTEGER, default=1)
   references=Column(TEXT)
   predicted_term = Column(TEXT,default='')
   predicted_term_confidence = Column(FLOAT,default=0.0)
   predicted_term_source_system = Column(TEXT,default='')
   predicted_term_system_version = Column(TEXT,default='')