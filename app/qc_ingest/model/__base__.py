from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_

SchemaBase = declarative_base()

class MissingParamException(Exception):
    def __init__(self,param,*args):
        self.param=param
        super().__init__(args)
    def __str__(self):
        return f"Missing {self.param}  in request "

class CurdOp:
    CREATE = "create"
    UPDATE = "update"
    READ = "read"
    DELETE = 'delete'


def schema_to_dict(row):
    data = {}
    for column in row.__table__.columns:
        data[column.name] = (getattr(row, column.name))
    return data


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
