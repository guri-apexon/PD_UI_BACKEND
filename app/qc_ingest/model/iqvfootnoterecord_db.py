from sqlalchemy import Column, Index, and_
from .__base__ import SchemaBase, schema_to_dict, MissingParamException, update_footnote_index
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR, INTEGER, BOOLEAN, BIGINT, JSONB, BYTEA
import uuid
from datetime import datetime


class IqvfootnoterecordDb(SchemaBase):

    __tablename__ = "iqvfootnoterecord_db"
    id = Column(VARCHAR(128), primary_key=True, nullable=False)
    doc_id = Column(TEXT)
    DocumentSequenceIndex = Column(INTEGER, nullable=False)
    dts = Column(TEXT)
    footnote_indicator = Column(TEXT)
    footnote_text = Column(TEXT)
    pname = Column(TEXT)
    procedure = Column(TEXT)
    procedure_text = Column(TEXT)
    ProcessMachineName = Column(TEXT)
    ProcessVersion = Column(TEXT)
    roi_id = Column(TEXT)
    run_id = Column(TEXT)
    section = Column(TEXT)
    table_link_text = Column(TEXT)
    table_roi_id = Column(TEXT)
    table_sequence_index = Column(INTEGER)
    study_cohort = Column(TEXT)


    @staticmethod
    def create(session, data):
        """
        
        """
        if data['AttachmentListProperties'] != None:
            for index, footnote in enumerate(data['AttachmentListProperties']):
                uid = str(uuid.uuid4())
                footnoterecord = IqvfootnoterecordDb()
                footnoterecord.id = uid
                footnoterecord.doc_id = data.get('doc_id')
                footnoterecord.table_roi_id = data.get('uuid')
                footnoterecord.table_link_text = data.get('TableName', '')
                footnoterecord.table_sequence_index = data.get('TableIndex', '')
                footnoterecord.DocumentSequenceIndex = index
                footnoterecord.footnote_text = footnote.get('footnote_text', '')
                footnoterecord.footnote_indicator = footnote.get(
                    'footnote_indicator', '')
                session.add(footnoterecord)
        return data


    @staticmethod
    def update(session, data):
        """
        
        """
        if data['AttachmentListProperties'] != None:
            for footnote in data['AttachmentListProperties']:
                sequnce_index = None
                footnote_line_id = footnote.get("footnote_line_id", None)
                qc_change_type_footnote = footnote.get(
                    "qc_change_type_footnote", '')
                table_roi_id = data['id']
                previous_sequnce_index = footnote.get("previous_sequnce_index")
                if qc_change_type_footnote == 'add':
                    uid = str(uuid.uuid4())
                    if previous_sequnce_index == None:
                        sequnce_index = 0
                    else:
                        sequnce_index = previous_sequnce_index + 1
                    previous_obj = session.query(IqvfootnoterecordDb).filter(and_(IqvfootnoterecordDb.table_roi_id ==
                                                                        table_roi_id, IqvfootnoterecordDb.DocumentSequenceIndex == sequnce_index)).first()
                    if not previous_obj:
                        raise MissingParamException("{0} previous footnote in Iqvfootnoterecord DB".format(table_roi_id))
                    prev_dict=schema_to_dict(previous_obj)
                    obj = IqvfootnoterecordDb(**prev_dict)
                    obj.id = uid
                    obj.DocumentSequenceIndex = sequnce_index
                    obj.footnote_text = footnote.get('footnote_text', '')
                    obj.footnote_indicator = footnote.get('footnote_indicator', '')
                    session.add(obj)
                    update_footnote_index(
                        session, table_roi_id, sequnce_index, '+')
                if qc_change_type_footnote == 'modify':
                    obj = session.query(IqvfootnoterecordDb).filter(
                        IqvfootnoterecordDb.id == footnote_line_id).first()
                    if not obj:
                        raise MissingParamException("{0} in Iqvfootnoterecord DB".format(footnote_line_id))
                    obj.footnote_text = footnote.get('footnote_text', '')
                    obj.footnote_indicator = footnote.get('footnote_indicator', '')
                    session.add(obj)
                if qc_change_type_footnote == 'delete':
                    obj = session.query(IqvfootnoterecordDb).filter(
                        IqvfootnoterecordDb.id == footnote_line_id).first()
                    if not obj:
                        raise MissingParamException("{0} in Iqvfootnoterecord DB".format(footnote_line_id))
                    sequnce_index = obj.DocumentSequenceIndex
                    session.delete(obj)
                    update_footnote_index(
                        session, table_roi_id, sequnce_index, '-')
                session.commit()


    @staticmethod
    def delete(session, data):
        """
        
        """
        try:
            session.query(IqvfootnoterecordDb).filter(
                IqvfootnoterecordDb.table_roi_id == data['id']).delete()
        except Exception as ex:
            raise MissingParamException("{0}{1} in Iqvfootnoterecord DB".format(data['id'], ex))
