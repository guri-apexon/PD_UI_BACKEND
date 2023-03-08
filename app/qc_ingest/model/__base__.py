from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_

SchemaBase = declarative_base()

class CurdOp:
    CREATE="create"
    UPDATE="update"
    READ="read"
    DELETE='delete'

def schema_to_dict(row):
    data = {}
    for column in row.__table__.columns:
        data[column.name] = (getattr(row, column.name))
    return data

def update_roi_index(session, table_name,doc_id,sequence_id, op):
    """
    
    """
    op_code = '+' if op == CurdOp.CREATE else '-'
    sql = f'UPDATE {table_name} SET "SequenceID" = "SequenceID" {op_code} 1 ,\
        "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 WHERE "SequenceID" > {sequence_id} \
         AND "doc_id" = \'{doc_id}\' AND "group_type" = \'DocumentParagraphs\' '
    session.execute(sql)

def update_link_index(session, table_name,doc_id,sequence_idx, op):
    """
    
    """
    op_code = '+' if op == CurdOp.CREATE else '-'
    sql = f'UPDATE {table_name} SET "DocumentSequenceIndex" = "DocumentSequenceIndex" {op_code} 1 \
         WHERE "DocumentSequenceIndex" > {sequence_idx} \
         AND "doc_id" = \'{doc_id}\' AND "group_type" = \'DocumentLinks\' AND "LinkType" = \'toc\' '
    session.execute(sql)

def update_partlist_index(session, table_name,doc_id,sequence_id, op):
    """
    
    """
    op_code = '+' if op == CurdOp.CREATE else '-'
    sql = f'UPDATE {table_name} SET "sequence_id" = "sequence_id" {op_code} 1 \
        WHERE "sequence_id" > {sequence_id} AND "doc_id" = \'{doc_id}\' AND "group_type" = \'DocumentPartsList\' '
    session.execute(sql)

def update_existing_props(obj,data):
    for key, val in data.items():
        if hasattr(obj, key):
            setattr(obj, key, val)