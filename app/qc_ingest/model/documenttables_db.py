from sqlalchemy import Column, and_, DateTime
from .__base__ import SchemaBase, schema_to_dict, update_existing_props, update_roi_index, update_attachment_footnote_index, CurdOp, MissingParamException, get_utc_datetime
from .iqvpage_roi_db import IqvpageroiDb
from .iqvkeyvalueset_db import IqvkeyvaluesetDb
from .documentparagraphs_db import DocumentparagraphsDb
from .pd_meta_entity_mapping_lookup import insert_meta_entity
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN,FLOAT
import uuid
from app.config import SOURCE
from copy import deepcopy
from collections import defaultdict
from datetime import datetime, timezone


class ParseTable():

    def parse_row(self, props):
        """
        parse rows of tables
        """
        row_idx = int(float(props['row_idx']))
        row_roi_id = props.get('row_roi_id', '')
        row = props['row_props']
        col_vals = {}
        for col_idx, col_data in row.items():
            col_idx = int(float(col_idx))
            roi_data = col_data.get('roi_id', {})
            col_vals[col_idx] = {'val': col_data.get('content', ''), 'row_roi_id': row_roi_id,
                                 'cell_roi': roi_data.get('datacell_roi_id', '')}
        return row_idx, col_vals

    def parse(self, table_data):
        """
        parse table data
        """
        num_rows = len(table_data)
        rows_data = {}
        num_cols = 0
        for row in table_data:
            row_idx, row_data = self.parse_row(row)
            if len(row['row_props']) > num_cols:
                num_cols = len(row['row_props'])
            rows_data[row_idx] = row_data
        return num_rows, num_cols, rows_data

    def get_order_data(self, rows_data, order='row'):
        """
        get order data
        """
        out_data = defaultdict(list)
        for row_idx, row_vals in rows_data.items():
            for col_idx, row_vals in row_vals.items():
                if order == 'col':
                    out_data[col_idx].append(rows_data[row_idx][col_idx])
                else:
                    out_data[row_idx].append(rows_data[row_idx][col_idx])
        return out_data

    def get_op_params(self, op_type, op_params, table_data):
        """
        get op_params
        """
        for table_prop in op_params:
            if op_type == TableOp.UPDATE_TABLE:
                row_idx = table_prop["row_idx"]
                rdata = table_data[int(row_idx)]
                table_prop['row_roi_id'] = rdata[0]['row_roi_id']
                row_props = table_prop['row_props']
                for cell_idx, cell_data in row_props.items():
                    cell_data['roi_id']['datacell_roi_id'] = rdata[int(
                        cell_idx)]['datacell_roi_id']

            elif op_type == TableOp.INSERT_COLUMN:
                row_idx = table_prop["row_idx"]
                rdata = table_data[int(row_idx)]
                table_prop['row_roi_id'] = rdata[0]['row_roi_id']

            elif op_type == TableOp.DELETE_ROW:
                row_idx = table_prop["row_idx"]
                rdata = table_data[int(row_idx)]
                table_prop['row_roi_id'] = rdata[0]['row_roi_id']
                prop = {"content": "",
                        "roi_id": {
                            "row_roi_id": "",
                            "datacell_roi_id": ""
                        }}
                row_props = table_prop['row_props']
                for cell_data in rdata:
                    col_idx = cell_data['col_idx']
                    row_props[col_idx] = deepcopy(prop)
                    row_props[col_idx]['roi_id']['datacell_roi_id'] = cell_data['datacell_roi_id']

            elif op_type == TableOp.DELETE_COLUMN:
                row_idx = table_prop["row_idx"]
                rdata = table_data[int(row_idx)]
                table_prop['row_roi_id'] = rdata[0]['row_roi_id']
                row_props = table_prop['row_props']
                for col_idx, cell_data in row_props.items():
                    col_cell_data = rdata[int(col_idx)]
                    cell_data['roi_id']['datacell_roi_id'] = col_cell_data['datacell_roi_id']

        return op_params


class TableOp:
    CREATE_TABLE = 'create_table'
    DELETE_TABLE = 'delete_table'
    UPDATE_TABLE = 'modify'
    INSERT_ROW = 'insert_row'
    INSERT_COLUMN = 'insert_column'
    DELETE_ROW = 'delete_row'
    DELETE_COLUMN = 'delete_column'
    ADD = 'add'
    MODIFY = 'modify'
    DELETE = 'delete'


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
        doc_table_helper = DocTableHelper()
        table_props = data.get('op_params')
        if table_props != None:
            parse_table = ParseTable()
            num_rows, num_cols, table_data = parse_table.parse(table_props)
            if data['op_type'] == TableOp.CREATE_TABLE:
                table_id = doc_table_helper.create_table(
                    session, data, num_rows, num_cols, table_data)
            else:
                raise MissingParamException(" or invalid operation type ")
        doc_table_helper.create_footnote(session, data)
        session.commit()
        return data

    @staticmethod
    def update(session, data):
        """
        """
        doc_table_helper = DocTableHelper()
        table_roi_id = data.get('table_roi_id')
        if not table_roi_id:
            raise MissingParamException('line_id')
        op_parameter = data.get('op_params')
        if op_parameter != None and len(op_parameter)>0:
            table_datail = doc_table_helper.get_table(session, table_roi_id)
            userid = data.get('userId')
            op_type = data.get('op_type', None)
            parse_table = ParseTable()
            count = 1
            for op_param in op_parameter:
                op_params = parse_table.get_op_params(op_type, op_param, table_datail)
                _, _, table_data = parse_table.parse(op_params)
                if op_type == TableOp.UPDATE_TABLE:
                    doc_table_helper.update_table(session, table_data, userid)
                elif op_type == TableOp.INSERT_ROW:
                    for row_idx, row_data in table_data.items():
                        doc_table_helper.insert_row(
                            session, table_roi_id, row_idx, row_data, userid)

                elif op_type == TableOp.INSERT_COLUMN:
                    doc_table_helper.insert_col(
                        session, table_roi_id, table_data, userid)

                elif op_type == TableOp.DELETE_ROW:
                    doc_table_helper.delete_row(session, table_data)
                    if len(op_parameter) == count:
                        doc_table_helper._update_table_row_index(session, DocumenttablesDb.__tablename__, table_roi_id, 0, CurdOp.DELETE)
                    count +=1

                elif op_type == TableOp.DELETE_COLUMN:
                    doc_table_helper.delete_column(session, table_data)
                    if len(op_parameter) == count:
                        doc_table_helper._update_table_col_index(session, DocumenttablesDb.__tablename__, table_roi_id, 0, CurdOp.DELETE)
                    count +=1
                else:
                    raise MissingParamException(" or invalid operation type")

        doc_table_helper.update_footnote(session, data)
        
        iqv_standard_term  = data.get('iqv_standard_term','')
        obj = session.query(DocumenttablesDb).filter(DocumenttablesDb.id == table_roi_id).first()
        if not obj:
            raise MissingParamException("{table_roi_id} in Documenttables DB")
        if iqv_standard_term and iqv_standard_term != obj.iqv_standard_term:
            source_system = '' if obj.predicted_term_source_system == None else obj.predicted_term_source_system
            if source_system.startswith('NLP') or source_system == '':
                insert_meta_entity(session, 'table', data.get('TableName'), iqv_standard_term)
            obj.predicted_term_source_system = SOURCE
            obj.iqv_standard_term = iqv_standard_term
            session.add(obj)
        session.commit()

    @staticmethod
    def delete(session, data):
        doc_table_helper = DocTableHelper()
        table_id = data.get('table_roi_id')
        if data['op_type'] == TableOp.DELETE_TABLE:
            doc_table_helper.delete_table(session, table_id)
            doc_table_helper.delete_footnote(session, data)
        else:
            raise MissingParamException("or invalid operation type")
        


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
        para_data.iqv_standard_term = iqv_standard_term = data.get('iqv_standard_term','')
        source_system = ""
        if iqv_standard_term != "":
            source_system = SOURCE
        para_data.predicted_term_source_system = source_system
        para_data.DocumentSequenceIndex = prev_data.DocumentSequenceIndex - \
            1 if is_top_elm else prev_data.DocumentSequenceIndex+1
        para_data.SequenceID = prev_data.SequenceID - \
            1 if is_top_elm else prev_data.SequenceID+1
        doc_id = prev_data.doc_id
        para_data.parent_id = data['doc_id'] = doc_id
        para_data.last_updated = get_utc_datetime()
        para_data.num_updates = 0
        update_roi_index(session, doc_id, para_data.link_id, para_data.DocumentSequenceIndex, CurdOp.CREATE)
        session.add(para_data)
        return para_data
    
    def create_footnote(self, session, data):
        
        if data.get('AttachmentListProperties'):
            cid = None
            # if at top next element props are taken
            if data['prev_id']:
                cid = data['prev_id']
            else:
                cid = data['next_id']
            prev_data = session.query(IqvpageroiDb).filter(
                and_(IqvpageroiDb.id == cid, IqvpageroiDb.group_type != 'ChildBoxes')).first()
            if not prev_data:
                raise MissingParamException(cid)
            prev_dict = schema_to_dict(prev_data)
            para_data = DocumenttablesDb(**prev_dict)
            for index, footnote in enumerate(data['AttachmentListProperties']):
                uid = str(uuid.uuid4())
                para_data.id = footnote['AttachmentId'] = uid
                para_data.parent_id = data.get('uuid')
                para_data.hierarchy = 'table'
                para_data.group_type = 'Attachments'
                para_data.DocumentSequenceIndex = index
                para_data.Value = footnote.get('Text', '')
                para_data.last_updated = get_utc_datetime()
                para_data.num_updates = 1
                session.add(deepcopy(para_data))
        return data
    
    def update_footnote(self, session, data):
        if data.get('AttachmentListProperties'):
            for footnote in data['AttachmentListProperties']:
                sequnce_index = None
                attachment_id = footnote.get("AttachmentId", None)
                text_value = footnote.get('Text', '')
                qc_change_type_footnote = footnote.get(
                    "qc_change_type_footnote", '')
                table_roi_id = data['table_roi_id']
                previous_sequnce_index = footnote.get("PrevousAttachmentIndex")
                if qc_change_type_footnote == TableOp.ADD:
                    uid = str(uuid.uuid4())
                    if previous_sequnce_index == None:
                        sequnce_index = previous_sequnce_index = 0
                    else:
                        sequnce_index = previous_sequnce_index + 1
                    previous_obj = session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id ==
                                                                        table_roi_id, DocumenttablesDb.group_type == 'Attachments', DocumenttablesDb.DocumentSequenceIndex == previous_sequnce_index)).first()
                    if not previous_obj:
                        if sequnce_index == 0:
                            previous_obj = session.query(IqvpageroiDb).filter(
                                            and_(IqvpageroiDb.id == table_roi_id, IqvpageroiDb.group_type != 'ChildBoxes')).first()
                            prev_dict=schema_to_dict(previous_obj)
                            obj = DocumenttablesDb(**prev_dict)
                            obj.hierarchy = 'table'
                            obj.group_type = 'Attachments'
                            obj.parent_id = table_roi_id
                        else:   
                            raise MissingParamException("{0} previous footnote in Iqvfootnoterecord DB".format(table_roi_id))
                    else:
                        prev_dict=schema_to_dict(previous_obj)
                        obj = DocumenttablesDb(**prev_dict)
                    obj.id = footnote['AttachmentId'] = uid
                    obj.DocumentSequenceIndex = sequnce_index
                    obj.Value = text_value
                    session.add(obj)
                    update_attachment_footnote_index(
                        session, table_roi_id, sequnce_index, '+')
                if qc_change_type_footnote == TableOp.MODIFY:
                    obj = session.query(DocumenttablesDb).filter(
                        DocumenttablesDb.id == attachment_id).first()
                    if not obj:
                        raise MissingParamException("{0} in DocumenttablesDb DB".format(attachment_id))
                    obj.Value = text_value
                    session.add(obj)
                if qc_change_type_footnote == TableOp.DELETE:
                    obj = session.query(DocumenttablesDb).filter(
                        DocumenttablesDb.id == attachment_id).first()
                    if not obj:
                        raise MissingParamException("{0} in DocumenttablesDb DB".format(attachment_id))
                    sequnce_index = obj.DocumentSequenceIndex
                    session.delete(obj)
                    update_attachment_footnote_index(
                        session, table_roi_id, sequnce_index, '-')
                    session.query(IqvkeyvaluesetDb).filter(
                        IqvkeyvaluesetDb.parent_id == attachment_id).delete()
                session.commit()

    
    def delete_footnote(self, session, data):
        try:
            table_roi_id = data.get('table_roi_id')
            attachment_ids = session.query(DocumenttablesDb.id).filter(and_(
                DocumenttablesDb.parent_id == table_roi_id, DocumenttablesDb.group_type == 'Attachments')).all()
            for attachment_id in attachment_ids:
                session.query(IqvkeyvaluesetDb).filter(
                    IqvkeyvaluesetDb.parent_id == attachment_id[0]).delete()
            session.query(DocumenttablesDb).filter(and_(
                DocumenttablesDb.parent_id == table_roi_id, DocumenttablesDb.group_type == 'Attachments')).delete()
        except Exception as ex:
            raise MissingParamException("{0}{1} in DocumenttablesDb DB".format(table_roi_id, ex))

    def _update_table_row_index(self, session, table_name, parent_id, row_sequence_id, op):
        """
        parent_id is table_id
        row_sequence_id: update existing row index as well ,here we considering exact row idx
        """
        row_ids = self._get_all_rows_ids(session, parent_id, row_sequence_id)
        if op == CurdOp.CREATE:
            op_code = '+'
            row_id_str = ''
            for row_id in row_ids:
                row_id_str += f"'{row_id[0]}',"
            if len(row_ids) > 0:
                row_id_str = row_id_str[0:-1]
                sql_query = f'UPDATE {table_name} SET "tableCell_rowIndex" = "tableCell_rowIndex" {op_code} 1 WHERE "parent_id" IN ({row_id_str}) AND "group_type"= \'ChildBoxes\' '
                session.execute(sql_query)
                sql_query1 = f'UPDATE {table_name} SET "tableCell_rowIndex" = "tableCell_rowIndex" {op_code} 1 ,\
                    "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "DocumentSequenceIndex" >= \'{row_sequence_id}\' \
                        AND "parent_id" = \'{parent_id}\' AND "group_type"= \'ChildBoxes\' '
                session.execute(sql_query1)
        else:
            for index, row_id in enumerate(row_ids):
                sql_query = f'UPDATE {table_name} SET "tableCell_rowIndex" = {index} ,\
                    "DocumentSequenceIndex" = {index} WHERE "id" = \'{row_id[0]}\' AND "group_type"= \'ChildBoxes\''
                session.execute(sql_query)
                sql_query1 = f'UPDATE {table_name} SET "tableCell_rowIndex" = {index} WHERE "parent_id" = \'{row_id[0]}\' AND "group_type"= \'ChildBoxes\''
                session.execute(sql_query1)

    def _update_table_col_index(self, session, table_name, parent_id, col_sequence_id, op):
        """
        parent_id = row_id
        row_sequence_id: update existing row index as well ,here we considering exact row idx
        """
        if op == CurdOp.CREATE:
            op_code = '+'
            sql_query = f'UPDATE {table_name} SET "tableCell_colIndex" = "tableCell_colIndex" {op_code} 1 ,\
            "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "tableCell_colIndex" >= \'{col_sequence_id}\' \
                AND "parent_id" = \'{parent_id}\' AND "group_type"= \'ChildBoxes\' '
            session.execute(sql_query)
        else:
            row_ids = self._get_all_rows_ids(session, parent_id, 0)
            for index, row_id in enumerate(row_ids):
                col_ids = self._get_all_cols_ids(session, row_id[0])
                for index, col_id in enumerate(col_ids):
                    sql_query = f'UPDATE {table_name} SET "tableCell_colIndex" = {index} ,\
                        "DocumentSequenceIndex" = {index} WHERE "id" = \'{col_id[0]}\' AND "group_type"= \'ChildBoxes\''
                    session.execute(sql_query)

    def insert_col(self, session, table_id, data, userid):
        """
        table_id is parent id for all rows 
        first all rows ids must be fetched then crossponding col can be updated.
        """
        rows_info = self._get_all_rows_ids(session, table_id, 0)
        row_obj = self._get_table_obj(session, table_id)
        sequence_index = row_obj.DocumentSequenceIndex
        sequence_id = row_obj.SequenceID
        for row_id, row_idx in rows_info:
            row_dict = schema_to_dict(row_obj)
            row_dict['tableCell_rowIndex'] = row_idx
            row_dict['id'] = row_id
            row_dict['userId'] = userid
            r_data = data.get(row_dict['tableCell_rowIndex'], None)
            if not r_data:
                raise MissingParamException(
                    f'{row_dict["tableCell_rowIndex"]} row index  ')
            for col_idx, col_data in r_data.items():
                col_sequence_index = sequence_index + (len(r_data)*(row_idx+1))-(len(r_data)-(col_idx+1))
                col_sequence_id = sequence_id + (len(r_data)*(row_idx+1))-(len(r_data)-(col_idx+1))
                # first update indexes then update..
                self._update_table_col_index(
                    session, DocumenttablesDb.__tablename__, row_id, col_idx, CurdOp.CREATE)
                update_roi_index(session, row_obj.doc_id, row_obj.link_id, col_sequence_index, CurdOp.CREATE)
                self.add_col(session, row_dict, col_idx, col_data['val'], col_sequence_index, col_sequence_id)

    def delete_column(self, session, table_data):
        child_cell_id_list = list()
        for row_idx, row_data in table_data.items():
            for col_idx, col_data in row_data.items():
                row_id, cell_id = col_data['row_roi_id'], col_data['cell_roi']
                child_obj = session.query(DocumenttablesDb).filter(
                    DocumenttablesDb.parent_id == cell_id).first()
                child_cell_id_list.append(child_obj.id)
                session.query(DocumentparagraphsDb).filter(
                    DocumentparagraphsDb.id == child_obj.id).delete()
                session.query(DocumenttablesDb).filter(
                    DocumenttablesDb.id == cell_id).delete()
                session.query(DocumenttablesDb).filter(
                    DocumenttablesDb.parent_id == cell_id).delete()
        session.query(IqvkeyvaluesetDb).filter(
                    IqvkeyvaluesetDb.parent_id.in_(child_cell_id_list)).delete()

    def _get_all_rows(self, session, table_id):
        rows = session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id == table_id,
                                                           DocumenttablesDb.group_type == 'ChildBoxes')).all()
        return rows

    def _get_all_rows_ids(self, session, table_id, row_sequence_id):
        row_obj = session.query(DocumenttablesDb.id, DocumenttablesDb.tableCell_rowIndex).filter(and_(DocumenttablesDb.parent_id == table_id,
                                                                                                      DocumenttablesDb.group_type == 'ChildBoxes', DocumenttablesDb.DocumentSequenceIndex>=int(row_sequence_id))).order_by(DocumenttablesDb.DocumentSequenceIndex).all()
        return row_obj

    def _get_all_cols_ids(self, session, row_id):
        col_obj = session.query(DocumenttablesDb.id, DocumenttablesDb.tableCell_colIndex).filter(and_(DocumenttablesDb.parent_id == row_id,
                                                                                                      DocumenttablesDb.group_type == 'ChildBoxes')).order_by(DocumenttablesDb.DocumentSequenceIndex).all()
        return col_obj

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
        row_data.last_updated = get_utc_datetime()
        row_data.num_updates = 0
        session.add(row_data)
        return row_data

    def add_col(self, session, row_data: dict, col_idx: int, content: str, sequence_index: int, sequence_id: int):
        """
        row_data: for copying default values. 
        """
        parent_id = row_data['id']
        for i in range(2):
            _id = str(uuid.uuid4())
            col_data = DocumenttablesDb(**row_data)
            row_idx = row_data['tableCell_rowIndex']
            col_data.id = _id
            col_data.hierarchy = 'table'
            col_data.group_type = 'ChildBoxes'
            col_data.parent_id = parent_id
            col_data.tableCell_rowIndex = int(row_idx)
            col_data.tableCell_colIndex = int(col_idx)
            col_data.DocumentSequenceIndex = int(col_idx)
            col_data.last_updated = get_utc_datetime()
            col_data.num_updates = 0
            col_data.Value = col_data.strText = content
            parent_id = _id
            session.add(col_data)
        
        para_data = DocumentparagraphsDb(**row_data)
        para_data.hierarchy = 'paragraph'
        para_data.group_type = 'DocumentParagraphs'     
        para_data.id = parent_id
        para_data.parent_id = para_data.doc_id
        para_data.DocumentSequenceIndex = int(sequence_index)
        para_data.SequenceID = int(sequence_id)
        para_data.tableCell_rowIndex = int(row_idx)
        para_data.tableCell_colIndex = int(col_idx)
        para_data.Value = para_data.strText = content
        para_data.last_updated = get_utc_datetime()
        para_data.num_updates = 0
        session.add(para_data)
                    

    def insert_row(self, session, table_roi_id, row_idx, data, userid):
        """
        table_id: is parent id for row
        """
        self._update_table_row_index(session, DocumenttablesDb.__tablename__, table_roi_id,
                                        row_idx, CurdOp.CREATE)

        table_obj = self._get_table_obj(session, table_roi_id)
        sequence_index = table_obj.DocumentSequenceIndex
        sequence_id = table_obj.SequenceID
        table_dict = schema_to_dict(table_obj)
        table_dict['id'] = table_roi_id
        table_dict['userId'] = userid
        row_data = self.add_row(session, table_dict, row_idx)
        row_data = schema_to_dict(row_data)
        for col_idx, col_data in data.items():
            col_sequence_index = sequence_index + (len(data)*(row_idx+1))-(len(data)-(col_idx+1))
            col_sequence_id = sequence_id + (len(data)*(row_idx+1))-(len(data)-(col_idx+1))
            update_roi_index(session, table_obj.doc_id, table_obj.link_id, col_sequence_index, CurdOp.CREATE)
            self.add_col(session, row_data, col_idx, col_data['val'], col_sequence_index, col_sequence_id)

    def update_cell_info(self, session, content, col_uid, child_cell_id, userid):
        
        obj_list = session.query(IqvpageroiDb).filter(IqvpageroiDb.id.in_((col_uid,child_cell_id))).all()
        if not obj_list and len(obj_list)==0:
            raise MissingParamException(f'{col_uid}, {child_cell_id} in {IqvpageroiDb.__tablename__}')
        for obj in obj_list:
            obj.Value = obj.strText = content
            obj.userId = userid
            obj.last_updated = get_utc_datetime()
            obj.num_updates = obj.num_updates + 1
            session.add(obj)


    def create_table(self, session, data, num_rows, num_cols, rows_data):
        """
        data_list:dict of row indexes and col data..
        """
        table_entry = self._create_table_entry(session, data)
        sequence_index = table_entry.DocumentSequenceIndex
        sequence_id = table_entry.SequenceID
        table_entry_dict = schema_to_dict(table_entry)
        for row_idx, row_data in rows_data.items():
            row_entry = self.add_row(session, table_entry_dict, row_idx)
            row_dict = schema_to_dict(row_entry)
            for col_idx, col_val in row_data.items():
                sequence_index += 1
                sequence_id += 1
                update_roi_index(session, table_entry.doc_id, table_entry.link_id, sequence_index, CurdOp.CREATE)
                self.add_col(session, row_dict, col_idx, col_val['val'], sequence_index, sequence_id)
        return table_entry.id

    def delete_table(self, session, table_id):
        """
        get all rows and delete ,get all cols and delete at last delete all entries.
        """
        row_ids = session.query(DocumenttablesDb).filter(and_(
            DocumenttablesDb.parent_id == table_id, DocumenttablesDb.group_type == 'ChildBoxes')).all()
        for row_id in row_ids:
            col_ids = session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id == row_id.id).all()
            for col_id in col_ids:
                child_col_ids = session.query(DocumenttablesDb.id).filter(
                    DocumenttablesDb.parent_id == col_id.id).all()
                for child_col_id in child_col_ids:
                    session.query(DocumentparagraphsDb).filter(
                        DocumentparagraphsDb.id == child_col_id[0]).delete()
                    session.query(IqvkeyvaluesetDb).filter(
                    IqvkeyvaluesetDb.parent_id == child_col_id[0]).delete()
                session.query(DocumenttablesDb).filter(
                    DocumenttablesDb.parent_id == col_id.id).delete()
            session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id == row_id.id).delete()
        # delete rows
        session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id ==
                                                    table_id, DocumenttablesDb.group_type == 'ChildBoxes')).delete()
        # delete table
        session.query(IqvkeyvaluesetDb).filter(
            IqvkeyvaluesetDb.parent_id == table_id).delete()
        session.query(DocumenttablesDb).filter(
            DocumenttablesDb.id == table_id).delete()

    def delete_row(self, session, table_data):

        for row_idx, row_data in table_data.items():
            row_id = row_data[0]['row_roi_id']
            obj = session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id == row_id).all()
            cell_id_list = list()
            child_cell_id_list = list() 
            for cell_data in obj:
                child_obj = session.query(DocumenttablesDb.id).filter(
                    DocumenttablesDb.parent_id == cell_data.id).first()
                child_cell_id_list.append(child_obj[0])
                cell_id_list.append(cell_data.id)
                session.query(DocumentparagraphsDb).filter(
                    DocumentparagraphsDb.id == child_obj[0]).delete()
            session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id.in_(cell_id_list)).delete()
            session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id == row_id).delete()
            session.query(DocumenttablesDb).filter(
                DocumenttablesDb.id == row_id).delete()
            session.query(IqvkeyvaluesetDb).filter(
                IqvkeyvaluesetDb.parent_id.in_(child_cell_id_list)).delete()

    def get_table(self, session, table_id):
        row_ids = session.query(DocumenttablesDb.id).filter(and_(
            DocumenttablesDb.parent_id == table_id, DocumenttablesDb.group_type == 'ChildBoxes')).all()
        table_data = {}
        for row_id in row_ids:
            cols_data = session.query(DocumenttablesDb).filter(
                DocumenttablesDb.parent_id == row_id[0]).all()
            row_data = ['']*len(cols_data)
            row_idx = ''
            for col in cols_data:
                row_idx = col.tableCell_rowIndex
                row_data[col.tableCell_colIndex] = {
                    'col_idx': col.tableCell_colIndex, 'row_roi_id': row_id[0],
                    'row_idx': row_idx, 'datacell_roi_id': col.id, 'val': col.Value
                }
            table_data[row_idx] = row_data
        return table_data

    def get_table_index(self, session, doc_id, table_roi_id):
        group_type = 'DocumentTables'
        obj = session.query(DocumenttablesDb.id).filter(and_(DocumenttablesDb.doc_id == doc_id, DocumenttablesDb.group_type == group_type)).order_by(DocumenttablesDb.DocumentSequenceIndex).all()
        table_index = None
        for i in range(len(obj)):
            if table_roi_id == obj[i][0]:
                table_index = i + 1
                break
        return table_index

    def get_table_footnote_data(self, session, table_id):
        data = list()
        obj = session.query(DocumenttablesDb).filter(and_(DocumenttablesDb.parent_id == table_id, DocumenttablesDb.group_type == 'Attachments')).order_by(DocumenttablesDb.DocumentSequenceIndex).all()
        if not obj:
            data = list()
        for row in obj:
            data.append({"AttachmentId": row.id,
                    "Text": row.Value}) 
        return data


    def _get_cell_roi_id(self, session, row_idx, col_idx):
        cell_id = session.query(DocumenttablesDb.id).filter(
            and_(DocumenttablesDb.tableCell_rowIndex == row_idx, DocumenttablesDb.tableCell_colIndex != col_idx, DocumenttablesDb.group_type == 'ChildBoxes')).first()
        return cell_id[0]

    def _get_child_cell_roi_id(self, session, col_uid):
        child_cell_id = session.query(DocumenttablesDb.id).filter(
            and_(DocumenttablesDb.parent_id == col_uid, DocumenttablesDb.group_type == 'ChildBoxes')).first()
        if not child_cell_id:
            raise MissingParamException('child_cell_id in Documenttables DB')
        return child_cell_id[0]

    def update_table(self, session, table_data, userid):
        """
        """
        for row_idx, row_data in table_data.items():
            for col_idx, col_data in row_data.items():
                if not col_data.get('cell_roi', None):
                    col_data['cell_roi'] = self._get_cell_roi_id(
                        session, row_idx, col_idx)
                child_cell_id = self._get_child_cell_roi_id(session, col_data['cell_roi'])
                self.update_cell_info(
                    session, col_data['val'], col_data['cell_roi'], child_cell_id, userid)
