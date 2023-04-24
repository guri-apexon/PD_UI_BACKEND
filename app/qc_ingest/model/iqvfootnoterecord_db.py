from sqlalchemy import Column, and_
from .__base__ import SchemaBase, schema_to_dict, MissingParamException, update_footnote_index, update_table_index, get_table_index
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER
import uuid


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
        if data.get('AttachmentListProperties'):
            table_roi_id = data.get('uuid')
            doc_id = data.get('doc_id', None)
            if not doc_id or not table_roi_id:
                raise MissingParamException('doc_id or table_roi_id')
            table_index = get_table_index(session, doc_id, table_roi_id)
            if not table_index:
                raise MissingParamException('table_index')
            for index, footnote in enumerate(data['AttachmentListProperties']):
                uid = str(uuid.uuid4())
                footnoterecord = IqvfootnoterecordDb()
                footnoterecord.id = uid
                footnoterecord.doc_id = data.get('doc_id')
                footnoterecord.roi_id = footnote.get('AttachmentId', None)
                footnoterecord.table_roi_id = table_roi_id
                footnoterecord.table_link_text = data.get('TableName', '')
                footnoterecord.table_sequence_index = table_index
                footnoterecord.DocumentSequenceIndex = index
                text_value = footnote.get('Text', '')
                footnoterecord.footnote_text = text_value
                footnote_indicator = None
                splited_text = text_value.split(": ")
                if text_value != splited_text[0] and len(splited_text)>0:
                    footnote_indicator = splited_text[0]
                else:
                    splited_text = text_value.split('. ')
                    if text_value != splited_text[0] and len(splited_text)>0:
                        footnote_indicator = splited_text[0]
                footnoterecord.footnote_indicator = footnote_indicator
                session.add(footnoterecord)
            update_table_index(session, table_index, doc_id, '+')
        return data


    @staticmethod
    def update(session, data):
        """
        
        """
        if data.get('AttachmentListProperties'):
            for footnote in data['AttachmentListProperties']:
                sequnce_index = None
                attachment_id = footnote.get("AttachmentId", None)
                text_value = footnote.get('Text', '')
                footnote_indicator = None
                splited_text = text_value.split(": ")
                if text_value != splited_text[0] and len(splited_text)>0:
                    footnote_indicator = splited_text[0]
                else:
                    splited_text = text_value.split('. ')
                    if text_value != splited_text[0] and len(splited_text)>0:
                        footnote_indicator = splited_text[0]
                qc_change_type_footnote = footnote.get(
                    "qc_change_type_footnote", '')
                table_roi_id = data['table_roi_id']
                previous_sequnce_index = footnote.get("PrevousAttachmentIndex")
                if qc_change_type_footnote == 'add':
                    uid = str(uuid.uuid4())
                    if previous_sequnce_index == None:
                        sequnce_index = previous_sequnce_index = 0
                    else:
                        sequnce_index = previous_sequnce_index + 1
                    previous_obj = session.query(IqvfootnoterecordDb).filter(and_(IqvfootnoterecordDb.table_roi_id ==
                                                                        table_roi_id, IqvfootnoterecordDb.DocumentSequenceIndex == previous_sequnce_index)).first()
                    if not previous_obj:
                        if sequnce_index == 0:
                            doc_id = data.get('doc_id')
                            table_index = get_table_index(session, doc_id, table_roi_id)
                            if not table_index:
                                raise MissingParamException('table_index')
                            obj = IqvfootnoterecordDb()
                            obj.doc_id = doc_id
                            obj.table_roi_id = table_roi_id
                            obj.table_sequence_index = table_index
                        else:   
                            raise MissingParamException("{0} previous footnote in Iqvfootnoterecord DB".format(table_roi_id))
                    else:
                        prev_dict=schema_to_dict(previous_obj)
                        obj = IqvfootnoterecordDb(**prev_dict)
                    obj.id = uid
                    obj.roi_id = attachment_id
                    obj.DocumentSequenceIndex = sequnce_index
                    obj.footnote_text = text_value
                    obj.footnote_indicator = footnote_indicator
                    session.add(obj)
                    update_footnote_index(
                        session, table_roi_id, sequnce_index, '+')
                if qc_change_type_footnote == 'modify':
                    obj = session.query(IqvfootnoterecordDb).filter(
                        IqvfootnoterecordDb.roi_id == attachment_id).first()
                    if not obj:
                        raise MissingParamException("{0} in Iqvfootnoterecord DB".format(attachment_id))
                    obj.footnote_text = text_value
                    obj.footnote_indicator = footnote_indicator
                    session.add(obj)
                if qc_change_type_footnote == 'delete':
                    obj = session.query(IqvfootnoterecordDb).filter(
                        IqvfootnoterecordDb.roi_id == attachment_id).first()
                    if not obj:
                        raise MissingParamException("{0} in Iqvfootnoterecord DB".format(attachment_id))
                    sequnce_index = obj.DocumentSequenceIndex
                    session.delete(obj)
                    update_footnote_index(
                        session, table_roi_id, sequnce_index, '-')
                session.commit()


    @staticmethod
    def delete(session, data):
        """
        
        """
        table_index = data.get('TableIndex', None)
        table_roi_id = data.get('table_roi_id', None)
        if not table_index or not table_roi_id:
            raise MissingParamException('table_index or table_roi_id')
        session.query(IqvfootnoterecordDb).filter(
            IqvfootnoterecordDb.table_roi_id == table_roi_id).delete()
        update_table_index(session, table_index, data.get('doc_id'), '-')
