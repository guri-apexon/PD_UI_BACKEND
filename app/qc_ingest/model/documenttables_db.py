from sqlalchemy import Column, Index, and_
from .__base__ import SchemaBase, schema_to_dict, update_existing_props, update_roi_index, CurdOp, MissingParamException
from .iqvpage_roi_db import IqvpageroiDb
from .documentparagraphs_db import DocumentparagraphsDb
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN
import uuid
import json
from collections import defaultdict


class ParseTable():
   def __init__(self):
      pass

   def parse_row(self, props):
      row_idx = int(float(props['row_idx']))
      row_roi_id = props.get('row_roi_id', '')
      row = props['row_props']
      num_cols = len(row)
      col_vals = {}
      for col_idx, col_data in row.items():
         col_idx = int(float(col_idx))
         roi_data = col_data.get('roi_id', {})
         col_vals[col_idx] = {'val': col_data.get('content', ''), 'row_roi_id': row_roi_id,
                              'cell_roi': roi_data.get('datacell_roi_id', '')}
      return row_idx, col_vals

   def parse(self, table_data):
      num_rows = len(table_data)
      rows_data = {}
      for row in table_data:
         row_idx, row_data = self.parse_row(row)
         num_cols = len(row['row_props'])
         rows_data[row_idx] = row_data
      return num_rows, num_cols, rows_data

   def get_order_data(self, rows_data, order='row'):
      num_rows = len(rows_data)
      num_cols = len(rows_data[0])
      out_data = defaultdict(list)
      for row_idx, row_vals in rows_data.items():
         for col_idx, row_vals in row_vals.items():
            if order == 'col':
               out_data[col_idx].append(rows_data[row_idx][col_idx])
            else:
               out_data[row_idx].append(rows_data[row_idx][col_idx])
      return out_data


class TableOp:
   CREATE_TABLE = 'create_table'
   DELETE_TABLE = 'delete_table'
   UPDATE_TABLE = 'delete_table'
   INSERT_ROW = 'insert_row'
   INSERT_COLUMN = 'insert_column'
   DELETE_ROW = 'delete_row'
   DELETE_COLUMN = 'delete_column'
   UPDATE_COLUMN = 'update_column'


class DocumenttablesDb(SchemaBase):
   __tablename__ = "documenttables_db"
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
   # references = Column(TEXT)

   @staticmethod
   def create(session, data):
      """
      update document paragraph and childbox.
      data : prev data

      """
      doc_table_helper = DocTableHelper()
      if not data.get('op_type', None):
         raise MissingParamException('op_type')
      if not data.get('content', None):
        raise MissingParamException('content')
      content = data['content']
      if not content.get('TableProperties', None):
         raise MissingParamException('.TableProperties.')
      table_props = content['TableProperties']
      if isinstance(table_props, str):
         table_props = json.loads(table_props)

      if isinstance(table_props, str):
         table_props = json.loads(table_props)
      parse_table = ParseTable()
      num_rows, num_cols, table_data = parse_table.parse(table_props)
      if data['op_type'] == TableOp.CREATE_TABLE:
         table_id = doc_table_helper.create_table(
             session, data, num_rows, num_cols, table_data)
         print('table id is ', table_id)
      else:
         table_roi_id = data.get('line_id', None)
         if not table_roi_id:
            raise MissingParamException('line_id')
         if data['op_type'] == TableOp.INSERT_ROW:
            for row_idx, row_data in table_data.items():
               if not row_idx:
                  raise MissingParamException('row_idx ')
               doc_table_helper.insert_row(
                   session, table_roi_id, row_idx, row_data)

         elif data['op_type'] == TableOp.INSERT_COLUMN:
            doc_table_helper.insert_col(session, table_roi_id, table_data)
         else:
            raise MissingParamException(" or invalid operation type ")

      return data

   @staticmethod
   def update(session, data):
      """
      """
      doc_table_helper = DocTableHelper()
      if not data.get('content', None):
          raise MissingParamException('.content.')
      content = data['content']
      if not content.get('TableProperties', None):
         raise MissingParamException('.TableProperties.')
      table_props = content['TableProperties']
      if isinstance(table_props, str):
         table_props = json.loads(table_props)
      parse_table = ParseTable()
      _, _, table_data = parse_table.parse(table_props)
      doc_table_helper.update_table(session, table_data)

   @staticmethod
   def delete(session, data):
      doc_table_helper = DocTableHelper()
      table_id = data['id']
      if data['op_type'] == TableOp.DELETE_TABLE:
         doc_table_helper.delete_table(session, table_id)
      else:
         if not data.get('content', None):
             raise MissingParamException('.content.')
         content = data['content']
         if not content.get('TableProperties', None):
             raise MissingParamException('.TableProperties.')
         table_props = content['TableProperties']
         if isinstance(table_props, str):
            table_props = json.loads(table_props)
         parse_table = ParseTable()
         _, _, table_data = parse_table.parse(table_props)
         if data['op_type'] == TableOp.DELETE_ROW:
            doc_table_helper.delete_row(session, table_id, table_data)

         elif data['op_type'] == TableOp.DELETE_COLUMN:
            doc_table_helper.delete_column(session, table_data)
         else:
            raise MissingParamException(" or invalid operation type ")


class DocTableHelper():
   def _create_table_entry(self, session, data):
      """
      prev_line_id after which table should be added ..
      """
      cid, is_top_elm = None, False
      # if at top next element props are taken
      if data['prev_id']:
         cid = data['prev_id']
      else:
         cid = data['next_id']
         is_top_elm = True
      prev_data = session.query(IqvpageroiDb).filter(
          and_(IqvpageroiDb.id == cid, IqvpageroiDb.group_type != 'ChildBoxes')).first()
      if not prev_data:
         raise MissingParamException(cid)
      prev_dict = schema_to_dict(prev_data)
      para_data = DocumenttablesDb(**prev_dict)
      _id = data['uuid'] if data.get('uuid', None) else str(uuid.uuid4())
      update_existing_props(para_data, data)
      para_data.hierarchy = 'table'
      para_data.group_type = 'DocumentTables'
      para_data.id = _id
      para_data.Value = ''
      para_data.DocumentSequenceIndex = prev_data.DocumentSequenceIndex-1 if is_top_elm else prev_data.DocumentSequenceIndex+1
      para_data.SequenceID = prev_data.SequenceID-1 if is_top_elm else prev_data.SequenceID+1
      doc_id = prev_data.doc_id
      para_data.parent_id = doc_id
      update_roi_index(session, doc_id, para_data.SequenceID, CurdOp.CREATE)
      session.add(para_data)
      return para_data

   def _update_table_row_index(self, session, table_name, row_id_list, op):
      """
      parent_id is table_id
      row_sequence_id: update existing row index as well ,here we considering exact row idx
      """
      op_code = '+' if op == CurdOp.CREATE else '-' 
      row_id_str=''
      for row_id in row_id_list:    
         row_id_str+=f"'{row_id}',"
      row_id_str=row_id_str[0:-1]
      sql_query = f'UPDATE {table_name} SET "tableCell_rowIndex" = "tableCell_rowIndex" {op_code} 1 ,\
         "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE \
         "parent_id" IN ({row_id_str}) OR "id" IN ({row_id_str})'
      session.execute(sql_query)

   def _update_table_col_index(self, session, table_name, parent_id, col_sequence_id, op):
      """
      parent_id = row_id
      row_sequence_id: update existing row index as well ,here we considering exact row idx
      """
      op_code = '+' if op == CurdOp.CREATE else '-'
      sql_query = f'UPDATE {table_name} SET "tableCell_colIndex" = "tableCell_colIndex" {op_code} 1 ,\
         "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "tableCell_colIndex" >= \'{col_sequence_id}\' \
            AND "parent_id" = \'{parent_id}\' AND "group_type"= \'ChildBoxes\' '
      session.execute(sql_query)

   def insert_col(self, session, table_id, data):
      """
      table_id is parent id for all rows 
      first all rows ids must be fetched then crossponding col can be updated.
      """
      rows_info=self._get_all_rows_ids(session,table_id)
      row_obj = self._get_table_obj(session, table_id)
      for row_id,row_idx in rows_info:       
         row_dict = schema_to_dict(row_obj)
         row_dict['tableCell_rowIndex']=row_idx
         row_dict['id']=row_id
         r_data = data.get(row_dict['tableCell_rowIndex'], None)
         if not r_data:
            raise MissingParamException(
                f'{row_dict["tableCell_rowIndex"]} row index  ')
         for col_idx, col_data in r_data.items():
            #first update indexes then update..
            self._update_table_col_index(
                session, DocumenttablesDb.__tablename__,row_id, col_idx, CurdOp.CREATE)
            self.add_col(session, row_dict, col_idx, col_data['val'])

   def delete_column(self, session, table_data):
      for _, row_data in table_data.items():
         for col_idx, col_data in row_data.items():
            row_id, cell_id = col_data['row_roi_id'], col_data['cell_roi']
            session.query(DocumenttablesDb).filter(
                DocumenttablesDb.id == cell_id).delete()
            self._update_table_col_index(
                session, DocumenttablesDb.__tablename__, row_id, col_idx, CurdOp.DELETE)

   def _get_all_rows(self, session, table_id):
      rows = session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id == table_id,
                                                         DocumenttablesDb.group_type == 'ChildBoxes')).all()
      return rows

   def _get_all_rows_ids(self, session, table_id):
      row_obj = session.query(DocumenttablesDb.id,DocumenttablesDb.tableCell_rowIndex).filter(and_(DocumenttablesDb.parent_id == table_id,
                                                            DocumenttablesDb.group_type == 'ChildBoxes')).all()
      return row_obj
   
   def _get_table_obj(self, session, table_id):
      obj = session.query(DocumenttablesDb).filter(DocumenttablesDb.id == table_id,
                                                         DocumenttablesDb.hierarchy == 'table').first()
      return obj

   def add_row(self, session, table_data, row_idx):
      _id = str(uuid.uuid4())
      row_data = DocumenttablesDb(**table_data)
      row_data.id = _id
      row_data.hierarchy = 'table'
      row_data.group_type = 'ChildBoxes'
      row_data.parent_id = table_data['id']
      row_data.tableCell_rowIndex = int(row_idx)
      row_data.tableCell_colIndex = -1
      row_data.DocumentSequenceIndex = int(row_idx)
      row_data.Value = ''
      session.add(row_data)
      return row_data

   def add_col(self, session, row_data: dict, col_idx: int, content: str):
      """
      row_data: for copying default values. 
      """
      _id = str(uuid.uuid4())
      col_data = DocumenttablesDb(**row_data)
      row_idx = row_data['tableCell_rowIndex']
      col_data.id = _id
      col_data.hierarchy = 'table'
      col_data.group_type = 'ChildBoxes'
      col_data.parent_id = row_data['id']
      col_data.tableCell_rowIndex = int(row_idx)
      col_data.tableCell_colIndex = int(col_idx)
      col_data.DocumentSequenceIndex = int(col_idx)
      col_data.Value = content
      session.add(col_data)
      return col_data

   def insert_row(self, session, table_roi_id, row_idx, data):
      """
      table_id: is parent id for row
      """
      rows_info=self._get_all_rows_ids(session,table_roi_id)
      all_row_ids=[]
      for row_id,r_idx in rows_info:
         if r_idx>=row_idx:
            all_row_ids.append(row_id)
      self._update_table_row_index(session, DocumenttablesDb.__tablename__,
                                   all_row_ids, CurdOp.CREATE)
      
      table_obj = self._get_table_obj(session, table_roi_id)
      table_dict = schema_to_dict(table_obj)   
      table_dict['id']=table_roi_id
      row_data = self.add_row(session, table_dict, row_idx)
      row_data = schema_to_dict(row_data)
      for col_idx, col_data in data.items():
         self.add_col(session, row_data, col_idx, col_data['val'])


   def update_cell_info(self, session, content, col_uid):
      if not col_uid:
         raise MissingParamException('col_uid')
      table_name = DocumenttablesDb.__tablename__
      sql_query = f'UPDATE {table_name} SET "Value" = \'{content}\' WHERE "id" = \'{col_uid}\''
      session.execute(sql_query)

   def create_table(self, session, data, num_rows, num_cols, rows_data):
      """
      data_list:dict of row indexes and col data..
      """
      table_entry = self._create_table_entry(session, data)
      table_entry_dict = schema_to_dict(table_entry)
      for row_idx, row_data in rows_data.items():
         row_entry = self.add_row(session, table_entry_dict, row_idx)
         row_dict = schema_to_dict(row_entry)
         for col_idx, col_val in row_data.items():
            self.add_col(session, row_dict, col_idx, col_val['val'])
      return table_entry.id

   def delete_table(self, session, table_id):
      """
      get all rows and delete ,get all cols and delete at last delete all entries.
      """
      row_ids = session.query(DocumenttablesDb.id).filter(and_(
          DocumenttablesDb.parent_id == table_id, DocumenttablesDb.group_type == 'ChildBoxes')).all()
      for row_id in row_ids:
         session.query(DocumenttablesDb).filter(
             DocumenttablesDb.parent_id == row_id[0]).delete()
      # delete rows
      session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id ==
                                                  table_id, DocumenttablesDb.group_type == 'ChildBoxes')).delete()
      # delete table
      obj = session.query(DocumenttablesDb).filter(
          DocumenttablesDb.id == table_id).first()
      doc_id = obj.doc_id
      sequence_id = obj.SequenceID
      session.delete(obj)
      # update roi index
      update_roi_index(session, doc_id, sequence_id, CurdOp.DELETE)

   def delete_row(self, session, table_id, table_data):

      rows_info=self._get_all_rows_ids(session,table_id)
      for row_idx, row_data in table_data.items():
         row_id = row_data[0]['row_roi_id']
         session.query(DocumenttablesDb).filter(
               DocumenttablesDb.parent_id == row_id).delete()
         session.query(DocumenttablesDb).filter(
               DocumenttablesDb.id == row_id).delete()
         all_row_ids=[]
         for row_id,r_idx in rows_info:
            if r_idx>row_idx:
               all_row_ids.append(row_id)  
         self._update_table_row_index(
               session, DocumenttablesDb.__tablename__, all_row_ids, CurdOp.DELETE)

   def get_table(self, session, table_id):
      row_ids = session.query(DocumenttablesDb.id).filter(and_(
          DocumenttablesDb.parent_id == table_id, DocumenttablesDb.group_type == 'ChildBoxes')).all()
      table_data = {}
      for row_id in row_ids:
         cols_data = session.query(DocumenttablesDb).filter(
             DocumenttablesDb.parent_id == row_id[0]).all()
         row_data = ['']*len(cols_data)
         row_idx=''
         for col in cols_data:
             row_idx=col.tableCell_rowIndex
             row_data[col.tableCell_colIndex] = {
                 'col_idx': col.tableCell_colIndex, 'row_roi_id': row_id[0],
                 'row_idx': row_idx, 'datacell_roi_id': col.id, 'val': col.Value
             }
         table_data[row_idx]=row_data
      return table_data

   def update_table(self, session, table_data):
      """
      """
      for row_idx, row_data in table_data.items():
         for col_idx, col_data in row_data.items():
            self.update_cell_info(
                session, col_data['val'], col_data['cell_roi'])
