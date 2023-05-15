from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from datetime import datetime, timezone

SchemaBase = declarative_base()


class MissingParamException(Exception):
    def __init__(self, param, *args):
        self.param = param
        super().__init__(args)

    def __str__(self):
        return f"Missing {self.param}  in request "


class CurdOp:
    CREATE = "create"
    UPDATE = "update"
    READ = "read"
    DELETE = 'delete'

def get_utc_datetime():
    return datetime.now(timezone.utc)


def schema_to_dict(row):
    data = {}
    for column in row.__table__.columns:
        data[column.name] = (getattr(row, column.name))
    return data

def update_link_update_details(session, link_id, user_id, last_updated):
    
    table_name = 'iqvdocumentlink_db'
    sql = f'UPDATE {table_name} SET "userId" = \'{user_id}\', "last_updated" = \'{last_updated}\', "num_updates" = "num_updates" + 1 WHERE "id" = \'{link_id}\''
    session.execute(sql)


def update_table_index(session,table_index, doc_id, op_code):
    """

    """
    table_name = 'iqvfootnoterecord_db'
    sql = f'UPDATE {table_name} SET "table_sequence_index" = "table_sequence_index" {op_code} 1 WHERE "doc_id" = \'{doc_id}\' AND \
                "table_sequence_index" >= {int(table_index)}'
    session.execute(sql)

def update_attachment_footnote_index(session, table_roi_id, sequnce_index, op_code):
    """

    """
    group_type = 'Attachments'
    table_name = 'documenttables_db'
    sql = f'UPDATE {table_name} SET "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "parent_id" = \'{table_roi_id}\' AND "group_type" = \'{group_type}\' AND \
                "DocumentSequenceIndex" >= {sequnce_index}'
    session.execute(sql)


def update_footnote_index(session, table_roi_id, sequnce_index, op_code):
    """

    """
    table_name = 'iqvfootnoterecord_db'
    sql = f'UPDATE {table_name} SET "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "table_roi_id" = \'{table_roi_id}\' AND \
                "DocumentSequenceIndex" >= {sequnce_index}'
    session.execute(sql)


def update_roi_index(session, doc_id, sequence_id, op):
    """

    """
    for table_name, group_type in [("documentparagraphs_db", "DocumentParagraphs"), ("documenttables_db", "DocumentTables")]:
        op_code = '+' if op == CurdOp.CREATE else '-'
        sql = f'UPDATE {table_name} SET "SequenceID" = "SequenceID" {op_code} 1 ,\
            "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "doc_id" = \'{doc_id}\' AND \
                "SequenceID" >= {sequence_id}  AND "group_type" = \'{group_type}\' '
        session.execute(sql)


def update_link_index(session, table_name, doc_id, sequence_idx, op):
    """

    """
    op_code = '+' if op == CurdOp.CREATE else '-'
    sql = f'UPDATE {table_name} SET "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 \
         WHERE "DocumentSequenceIndex" >= {sequence_idx} \
         AND "doc_id" = \'{doc_id}\' AND "group_type" = \'DocumentLinks\' AND "LinkType" = \'toc\' '
    session.execute(sql)


def update_partlist_index(session, table_name, doc_id, sequence_id, op):
    """

    """
    op_code = '+' if op == CurdOp.CREATE else '-'
    sql = f'UPDATE {table_name} SET "sequence_id" = "sequence_id" {op_code} 1 \
        WHERE "sequence_id" >= {sequence_id} AND "doc_id" = \'{doc_id}\' AND "group_type" = \'DocumentPartsList\' '
    session.execute(sql)


def update_existing_props(obj, data):
    for key, val in data.items():
        if hasattr(obj, key):
            setattr(obj, key, val)
