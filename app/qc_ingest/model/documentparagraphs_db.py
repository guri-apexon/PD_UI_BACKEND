from sqlalchemy import Column, Index, DateTime
from .__base__ import SchemaBase, schema_to_dict, update_roi_index, CurdOp, update_existing_props, MissingParamException, get_utc_datetime
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN, BIGINT, JSONB, BYTEA,FLOAT
import uuid
from datetime import datetime, timezone
from .iqvpage_roi_db import IqvpageroiDb


class DocumentparagraphsDb(SchemaBase):
    __tablename__ = "documentparagraphs_db"
    id = Column(VARCHAR(128), primary_key=True, nullable=False)
    doc_id = Column(TEXT)
    link_id = Column(TEXT)
    link_id_level2 = Column(TEXT, default='')
    link_id_level3 = Column(TEXT, default='')
    link_id_level4 = Column(TEXT, default='')
    link_id_level5 = Column(TEXT, default='')
    link_id_level6 = Column(TEXT, default='')
    link_id_subsection1 = Column(TEXT, default='')
    link_id_subsection2 = Column(TEXT, default='')
    link_id_subsection3 = Column(TEXT, default='')
    hierarchy = Column(VARCHAR(128), primary_key=True, nullable=False)
    iqv_standard_term = Column(TEXT, default='')
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    strText = Column(TEXT, default='')
    strTextTranslated = Column(TEXT, default='')
    DocumentSequenceIndex = Column(INTEGER, nullable=False)
    hAlignmentVal = Column(INTEGER, nullable=False, default=-1)
    RotationCorrectionDegrees = Column(DOUBLE_PRECISION, nullable=False, default=0)
    m_WORD_LAYOUTVal = Column(INTEGER, nullable=False, default=0)
    m_ROI_TYPEVal = Column(INTEGER, nullable=False, default=404)
    BulletTypeVal = Column(INTEGER, nullable=False, default=-1)
    BulletIndentationLevel = Column(INTEGER, nullable=False, default=-1)
    m_PARENT_ROI_TYPEVal = Column(INTEGER, nullable=False, default=-1)
    HeaderSequence = Column(INTEGER, nullable=False, default=0)
    FooterSequence = Column(INTEGER, nullable=False, default=0)
    ImageIndex = Column(INTEGER, nullable=False, default=0)
    DocumentRelId = Column(TEXT, default='')
    PageSequenceIndex = Column(INTEGER, nullable=False, default=-1)
    PageID = Column(TEXT, default='')
    UncorrectedImageFilename = Column(TEXT, default='')
    ImageFormatVal = Column(TEXT, default='')
    bOutputImageCreated = Column(BOOLEAN, nullable=False, default=False)
    OutputImageFilename = Column(TEXT, default='')
    OutputImageFilename_RotationCorrection = Column(TEXT, default='')
    OutputImageFilename_RotationCorrectionToDropBox = Column(TEXT, default='')
    OutputImageFilename_FinalImageProcessingOutput = Column(TEXT, default='')
    OutputImageFilename_FinalImageProcessingOutputToDropBox = Column(TEXT, default='')
    OutputImageFilename_OriginalSegment = Column(TEXT, default='')
    OutputImageFilename_Segments = Column(TEXT, default='')
    OutputImageFilename_SegmentsToDropBox = Column(TEXT, default='')
    OutputImageFilename_Cleaned = Column(TEXT, default='')
    OutputImageFilenameT = Column(TEXT, default='')
    OutputImageFilenameTDropBox = Column(TEXT, default='')
    bIsImage = Column(BOOLEAN, nullable=False, default=False)
    Hue = Column(INTEGER, nullable=False, default=0)
    Rotation_MajorAxis = Column(INTEGER, nullable=False, default=0)
    htmlTagType = Column(TEXT, default='')
    textTypeVal = Column(INTEGER, nullable=False, default=-1)
    contentTypeVal = Column(INTEGER, nullable=False, default=0)
    bNoTranslate = Column(BOOLEAN, nullable=False, default=False)
    SegmentationType = Column(INTEGER, nullable=False, default=1)
    TranslatedTextNoSegmentation = Column(TEXT, default='')
    SegmentationMethodVal = Column(INTEGER, nullable=False, default=-1)
    TranslationMethod1 = Column(TEXT, default='')
    TranslationMatch = Column(DOUBLE_PRECISION, nullable=False, default=-0)
    imagePaddingPixels = Column(DOUBLE_PRECISION, nullable=False, default=0)
    imageScaling = Column(DOUBLE_PRECISION, nullable=False, default=0)
    IsTableCell = Column(BOOLEAN, nullable=False, default=False)
    tableCell_pageIndex = Column(INTEGER, nullable=False, default=-1)
    tableCell_rowIndex = Column(INTEGER, nullable=False, default=-1)
    bIsSharedString = Column(BOOLEAN, nullable=False, default=False)
    tableCell_SharedStringIndex = Column(INTEGER, nullable=False, default=0)
    tableCell_SheetRowIndex = Column(INTEGER, nullable=False, default=0)
    tableCell_SheetColIndex = Column(INTEGER, nullable=False, default=0)
    tableCell_colIndex = Column(INTEGER, nullable=False, default=-1)
    tableCell_SheetName = Column(TEXT, default='')
    tableCell_SheetCellReference = Column(TEXT, default='')
    OriginalROIWidthInches = Column(DOUBLE_PRECISION, nullable=False, default=0)
    OriginalROIHeightInches = Column(DOUBLE_PRECISION, nullable=False, default=0)
    HorizontalResolution = Column(DOUBLE_PRECISION, nullable=False, default=96)
    VerticalResolution = Column(DOUBLE_PRECISION, nullable=False, default=96)
    rectangle_x = Column(INTEGER, nullable=False, default=0)
    rectangle_y = Column(INTEGER, nullable=False, default=0)
    rectangle_width = Column(INTEGER, nullable=False, default=0)
    rectangle_height = Column(INTEGER, nullable=False, default=0)
    parentrectangle_x = Column(INTEGER, nullable=False, default=0)
    parentrectangle_y = Column(INTEGER, nullable=False, default=0)
    parentrectangle_width = Column(INTEGER, nullable=False, default=0)
    parentrectangle_height = Column(INTEGER, nullable=False, default=0)
    rectangleGlobalLocationOnPage_x = Column(INTEGER, nullable=False, default=0)
    rectangleGlobalLocationOnPage_y = Column(INTEGER, nullable=False, default=0)
    rectangleGlobalLocationOnPage_width = Column(INTEGER, nullable=False, default=0)
    rectangleGlobalLocationOnPage_height = Column(INTEGER, nullable=False, default=0)
    IsCopyOfRoiId = Column(TEXT, default='')
    bIsCheckbox = Column(BOOLEAN, nullable=False, default=False)
    bIsChecked = Column(BOOLEAN, nullable=False, default=False)
    CheckboxFill = Column(DOUBLE_PRECISION, nullable=False, default=0)
    bScannedOCR = Column(BOOLEAN, nullable=False, default=True)
    scannedOCRCode = Column(TEXT, default='eng')
    SequenceID = Column(INTEGER, nullable=False, default=0)
    SlideRelationshipId = Column(TEXT, default='')
    SlideIndex = Column(INTEGER, nullable=False, default=-1)
    Value = Column(TEXT)
    Score = Column(DOUBLE_PRECISION, nullable=False, default=0)
    GT_TextMatch = Column(TEXT, default='')
    GT_ScoreMatch = Column(DOUBLE_PRECISION, nullable=False, default=0)
    GT_ImageFilename = Column(TEXT, default='')
    userId = Column(VARCHAR(100))
    last_updated = Column(DateTime(timezone=True), nullable=True)
    num_updates = Column(INTEGER, default=0)
    predicted_term = Column(TEXT,default='')
    predicted_term_confidence = Column(FLOAT,default=0.0)
    predicted_term_source_system = Column(TEXT,default='')
    predicted_term_system_version = Column(TEXT,default='')
    references = Column(TEXT)

    @staticmethod
    def create(session, data):
        """
        update document paragraph and childbox.
        data : prev data

        """
        if data.get('is_section_completely_new') == True:
            para_data = DocumentparagraphsDb()
            _id = data['uuid'] if data.get('uuid',None) else str(uuid.uuid4())
            data['uuid'] = para_data.id = para_data.link_id = _id 
            para_data.SequenceID = 0   
            para_data.DocumentSequenceIndex = 0
            para_data.doc_id = para_data.parent_id = data.get('doc_id')
            para_data.userId = data.get('userId')
        else:
            cid, is_top_elm = None, False
            if data['prev_id']:
                cid = data['prev_id']
            else:
                cid = data.get('next_id', None)
                is_top_elm = True
            if not cid and data['is_link']:
                return data
            if not data['content'] and data['is_link']:
                data['content'] = data['link_text']

            prev_data = session.query(IqvpageroiDb).filter(
                IqvpageroiDb.id == cid).first()
            if not prev_data:
                raise MissingParamException(cid)
            prev_dict = schema_to_dict(prev_data)
            para_data = DocumentparagraphsDb(**prev_dict)
            _id = data['uuid'] if data.get('uuid', None) else str(uuid.uuid4())
            update_existing_props(para_data, data)
            para_data.id = _id
            para_data.DocumentSequenceIndex = prev_data.DocumentSequenceIndex - \
                1 if is_top_elm else prev_data.DocumentSequenceIndex+1
            para_data.SequenceID = prev_data.SequenceID - \
                1 if is_top_elm else prev_data.SequenceID+1
            doc_id = prev_data.doc_id
            para_data.parent_id = doc_id
            update_roi_index(session, doc_id, para_data.SequenceID, CurdOp.CREATE)
        
        para_data.hierarchy = 'paragraph'
        para_data.group_type = 'DocumentParagraphs'
        if data.get('content', None):
            para_data.Value = para_data.strText = data['content']
        para_data.last_updated = get_utc_datetime()
        para_data.num_updates = 1
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
            raise MissingParamException(f'{_id} in document paragraph db ')
        update_existing_props(obj, data)
        obj.last_updated = get_utc_datetime()
        obj.num_updates = obj.num_updates + 1
        if data.get('content', None):
            obj.Value = data['content']
        session.add(obj)

    @staticmethod
    def delete(session, data):
        obj = session.query(DocumentparagraphsDb).filter(
            DocumentparagraphsDb.id == data['id']).first()
        if not obj:
            _id = data['id']
            raise MissingParamException(f'{_id} in document paragraph db ')
        sequence_id = obj.SequenceID
        doc_id = obj.doc_id
        session.delete(obj)
        update_roi_index(session, doc_id, sequence_id, CurdOp.DELETE)
