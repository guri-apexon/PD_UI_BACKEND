from model import *
import json
import pandas as pd
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.orm import sessionmaker
from config import DbConfig, LocalDbConfig
URL = LocalDbConfig.url
engine = create_engine(URL, echo=True)
Session = sessionmaker(bind=engine)


session = Session()
df = pd.read_csv('link_db_data-fa386108-6df3-4188-b897-4f078d2b23f0.csv')
data = df.to_dict('records')

df1 = pd.read_csv('para_db_data-fa386108-6df3-4188-b897-4f078d2b23f0.csv')
data1 = df1.to_dict('records')

df2 = pd.read_csv('fontinfo_db_data-fa386108-6df3-4188-b897-4f078d2b23f0.csv')
data2 = df2.to_dict('records')

df3 = pd.read_csv('subtext_db_data-fa386108-6df3-4188-b897-4f078d2b23f0.csv')
data3 = df3.to_dict('records')

# session.bulk_insert_mappings(IqvdocumentlinkDb,data)
session.bulk_insert_mappings(DocumentparagraphsDb,data1)
# session.bulk_insert_mappings(FontinfoDb,data2)
# session.bulk_insert_mappings(IqvsubtextDb,data3)
session.commit()
session.close_all()


# re = session.query(FontinfoDb).filter(FontinfoDb.id == '1d51e9ad-4c81-498f-a73a-56be911e5c49')
# session.close_all()
# for i in re:
#     L_URL = LocalDbConfig.url
#     l_engine = create_engine(L_URL, echo=True)
#     LSession = sessionmaker(bind=l_engine)
#     lsession = LSession()
#     data = i.__dict__
#     print(data)
#     #c = DocumentparagraphsDb(HeaderSequence= 0, OutputImageFilename_Segments= '', IsCopyOfRoiId= '', FooterSequence= 0, OutputImageFilename_SegmentsToDropBox= '', bIsCheckbox= False, ImageIndex= 0, OutputImageFilename_Cleaned= '', bIsChecked= False, DocumentRelId= '', OutputImageFilenameT= '', CheckboxFill= 0.0, PageSequenceIndex= -1, OutputImageFilenameTDropBox= '', bScannedOCR= True, PageID= '', bIsImage= False, scannedOCRCode= 'eng', UncorrectedImageFilename= '', Hue= 0, SequenceID= 0, ImageFormatVal= '', Rotation_MajorAxis= 0, SlideRelationshipId= '', bOutputImageCreated= False, htmlTagType= '', SlideIndex= -1, OutputImageFilename= '', textTypeVal= -1, Value= '', OutputImageFilename_RotationCorrection= '', contentTypeVal= 0, Score= 0.0, OutputImageFilename_RotationCorrectionToDropBox= '', bNoTranslate= False, GT_TextMatch= '', OutputImageFilename_FinalImageProcessingOutput= '', SegmentationType= 1, GT_ScoreMatch= 0.0, OutputImageFilename_FinalImageProcessingOutputToDropBox= '', TranslatedTextNoSegmentation= '', GT_ImageFilename= '', OutputImageFilename_OriginalSegment= '', SegmentationMethodVal= -1, link_id_subsection3= '', TranslationMethod1= '', OriginalROIHeightInches= 0.0, hierarchy= 'paragraph', TranslationMatch= 0.0, HorizontalResolution= 96.0, iqv_standard_term= '', imagePaddingPixels= 0.0, VerticalResolution= 96.0, parent_id= 'f66fe0aa-0290-4253-9357-e42e10af970f', imageScaling= 0.0, rectangle_x= 0, group_type= 'ChildBoxes', IsTableCell= False, rectangle_y= 0, id= '52dc5287-45b4-4599-b7f1-7213b8b1660e', strText= 'Capivasertib (AZD5363), a novel pyrrolopyrimidine-derived compound, is a potent, selective inhibitor of the kinase activity of all 3 isoforms of AKT (Davies et al 2012).' , tableCell_pageIndex= -1, rectangle_width= 0, rectangle_height= 0, doc_id= 'fa386108-6df3-4188-b897-4f078d2b23f0', strTextTranslated= '', tableCell_rowIndex= -1, link_id= 'e066c0c8-8cf9-11ed-b3d7-005056ab6469', DocumentSequenceIndex= 0, bIsSharedString= False, parentrectangle_x= 0, link_id_level2= '', hAlignmentVal= -1, tableCell_SharedStringIndex= 0, parentrectangle_y= 0, link_id_level3= '', RotationCorrectionDegrees= 0.0, tableCell_SheetRowIndex= 0, parentrectangle_width= 0, link_id_level4= '', m_WORD_LAYOUTVal= 0, tableCell_SheetColIndex= 0, parentrectangle_height= 0, link_id_level5= '', m_ROI_TYPEVal= -1, tableCell_colIndex= -1, rectangleGlobalLocationOnPage_x= 0, link_id_level6= '', BulletTypeVal= -1, tableCell_SheetName= '', rectangleGlobalLocationOnPage_y= 0, link_id_subsection1= '', BulletIndentationLevel= -1, tableCell_SheetCellReference= '', rectangleGlobalLocationOnPage_width= 0, link_id_subsection2= '', m_PARENT_ROI_TYPEVal= -1, OriginalROIWidthInches= 0.0, rectangleGlobalLocationOnPage_height= 0)
#     lsession.add(c)
#     lsession.commit()
#     lsession.close_all()