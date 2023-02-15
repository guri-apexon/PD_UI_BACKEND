from .model import *


class Document:

    id = ""
    doc_id = ""
    link_id = ""
    link_id_level2 = ""
    link_id_level3 = ""
    link_id_level4 = ""
    link_id_level5 = ""
    link_id_level6 = ""
    link_id_subsection1 = ""
    link_id_subsection2 = ""
    link_id_subsection3 = ""
    hierarchy = ""
    iqv_standard_term = ""
    parent_id = ""
    group_type = ""
    strText = ""
    strTextTranslated = ""
    DocumentSequenceIndex = 0
    hAlignmentVal = 0
    RotationCorrectionDegrees = 0
    m_WORD_LAYOUTVal = 0
    m_ROI_TYPEVal = 0
    BulletTypeVal = 0
    BulletIndentationLevel = 0
    m_PARENT_ROI_TYPEVal = 0
    HeaderSequence = 0
    FooterSequence = 0
    ImageIndex = 0
    DocumentRelId = ""
    PageSequenceIndex = 0
    PageID = ""
    UncorrectedImageFilename = ""
    ImageFormatVal = ""
    bOutputImageCreated = False
    OutputImageFilename = ""
    OutputImageFilename_RotationCorrection = ""
    OutputImageFilename_RotationCorrectionToDropBox = ""
    OutputImageFilename_FinalImageProcessingOutput = ""
    OutputImageFilename_FinalImageProcessingOutputToDropBox = ""
    OutputImageFilename_OriginalSegment = ""
    OutputImageFilename_Segments = ""
    OutputImageFilename_SegmentsToDropBox = ""
    OutputImageFilename_Cleaned = ""
    OutputImageFilenameT = ""
    OutputImageFilenameTDropBox = ""
    bIsImage = False
    Hue = 0
    Rotation_MajorAxis = 0
    htmlTagType = ""
    textTypeVal = 0
    contentTypeVal = 0
    bNoTranslate = False
    SegmentationType = 0
    TranslatedTextNoSegmentation = ""
    SegmentationMethodVal = 0
    TranslationMethod1 = ""
    TranslationMatch = 0
    imagePaddingPixels = 0
    imageScaling = 0
    IsTableCell = False
    tableCell_pageIndex = 0
    tableCell_rowIndex = 0
    bIsSharedString = False
    tableCell_SharedStringIndex = 0
    tableCell_SheetRowIndex = 0
    tableCell_SheetColIndex = 0
    tableCell_colIndex = 0
    tableCell_SheetName = ""
    tableCell_SheetCellReference = ""
    OriginalROIWidthInches = 0
    OriginalROIHeightInches = 0
    HorizontalResolution = 0
    VerticalResolution = 0
    rectangle_x = 0
    rectangle_y = 0
    rectangle_width = 0
    rectangle_height = 0
    parentrectangle_x = 0
    parentrectangle_y = 0
    parentrectangle_width = 0
    parentrectangle_height = 0
    rectangleGlobalLocationOnPage_x = 0
    rectangleGlobalLocationOnPage_y = 0
    rectangleGlobalLocationOnPage_width = 0
    rectangleGlobalLocationOnPage_height = 0
    IsCopyOfRoiId = ""
    bIsCheckbox = False
    bIsChecked = False
    CheckboxFill = 0
    bScannedOCR = False
    scannedOCRCode = ""
    SequenceID = 0
    SlideRelationshipId = ""
    SlideIndex = 0
    Value = ""
    Score = 0
    GT_TextMatch = ""
    GT_ScoreMatch = 0
    GT_ImageFilename = ""


class Fontinfo:

    id = ""
    doc_id = ""
    link_id = ""
    link_id_level2 = ""
    link_id_level3 = ""
    link_id_level4 = ""
    link_id_level5 = ""
    link_id_level6 = ""
    link_id_subsection1 = ""
    link_id_subsection2 = ""
    link_id_subsection3 = ""
    hierarchy = ""
    iqv_standard_term = ""
    parent_id = ""
    group_type = ""
    Bold = False
    Italics = False
    Caps = False
    ColorRGB = 0
    DStrike = False
    Emboss = False
    Imprint = False
    Outline = False
    rStyle = ""
    Shadow = False
    SmallCaps = False
    Strike = False
    Highlight = ""
    Size = 0
    Underline = ""
    Vanish = False
    rFonts = ""
    VertAlign = ""


class Subtext:

    id = ""
    doc_id = ""
    link_id = ""
    link_id_level2 = ""
    link_id_level3 = ""
    link_id_level4 = ""
    link_id_level5 = ""
    link_id_level6 = ""
    link_id_subsection1 = ""
    link_id_subsection2 = ""
    link_id_subsection3 = ""
    hierarchy = ""
    iqv_standard_term = ""
    parent_id = ""
    group_type = ""
    bNoTranslate = False
    reservedTypeVal = 0
    parent2LocalName = ""
    Value = ""
    OuterXml = ""
    strText = ""
    strTranslatedText = ""
    runElementName = ""
    DocumentSequenceIndex = 0
    sequence = 0
    startCharIndex = 0


class DocumentLink:

    id = ""
    doc_id = ""
    link_id = ""
    link_id_level2 = ""
    link_id_level3 = ""
    link_id_level4 = ""
    link_id_level5 = ""
    link_id_level6 = ""
    link_id_subsection1 = ""
    link_id_subsection2 = ""
    link_id_subsection3 = ""
    hierarchy = ""
    iqv_standard_term = ""
    parent_id = ""
    group_type = ""
    LinkType = ""
    DocumentSequenceIndex = 0
    LinkPage = 0
    LinkLevel = 0
    LinkText = ""
    LinkPrefix = ""


class TableType:

    table_dict = {'text': DocumentparagraphsDb, 'table': DocumenttablesDb, 'font_info': FontinfoDb, 'image': DocumentimagesDb,
                  'header': DocumentparagraphsDb, 'link_db': IqvdocumentlinkDb, 'subtext': IqvsubtextDb}


class Linklevel:

    link_level_dict = {"1": "link_id",
                       "2": "link_id_level2",
                       "3": "link_id_level3",
                       "4": "link_id_level4",
                       "5": "link_id_level5",
                       "6": "link_id_level6",
                       "7": "link_id_subsection1",
                       "8": "link_id_subsection2",
                       "9": "link_id_subsection3"}
