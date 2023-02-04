from document import Document, Fontinfo, DocumentLink, Subtext, TableType, Linklevel
from model import *
import logging as logger
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from config import settings
URL = settings.LOCAL_DB_URL
engine = create_engine(URL, echo=True)
Session = sessionmaker(bind=engine)
table_dict = TableType.table_dict

link_level_dict = Linklevel.link_level_dict


def db_update(val_list: list):
    """updating paragraph data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        table_name = table_dict.get(content_type)
                        obj = session.query(table_name).filter(
                            table_name.id == data.get('id'))
                        for row in obj:
                            for key, val in data.items():
                                if hasattr(row, key):
                                    setattr(row, key, val)
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in updating paragraph data in DB: {exc}")


def db_delete(val_list: list):
    """deleting paragraph data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        table_name = table_dict.get(content_type)
                        if table_name == IqvdocumentlinkDb:
                            obj = session.query(table_name).filter(
                                table_name.id == data.get('id'))
                            for row in obj:
                                document_sequence_index = row.DocumentSequenceIndex
                            del_obj = session.query(table_name).filter(
                                table_name.id == data.get('id')).delete()
                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == data.get(
                                'doc_id'), table_name.DocumentSequenceIndex > document_sequence_index))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex - 1

                        elif table_name != FontinfoDb:
                            obj = session.query(table_name).filter(
                                table_name.id == data.get('id'))
                            for row in obj:
                                document_sequence_index = row.DocumentSequenceIndex
                            del_obj = session.query(table_name).filter(
                                table_name.id == data.get('id')).delete()
                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == data.get('doc_id'), table_name.link_id == data.get('link_id'),
                                                                         table_name.link_id_level2 == data.get(
                                'link_id_level2'), table_name.link_id_level3 == data.get('link_id_level3'),
                                table_name.link_id_level4 == data.get(
                                'link_id_level4'), table_name.link_id_level5 == data.get('link_id_level5'),
                                table_name.link_id_level6 == data.get(
                                'link_id_level6'), table_name.link_id_subsection1 == data.get('link_id_subsection1'),
                                table_name.link_id_subsection2 == data.get(
                                'link_id_subsection2'), table_name.link_id_subsection3 == data.get('link_id_subsection3'),
                                table_name.parent_id == data.get('parent_id'), table_name.DocumentSequenceIndex > document_sequence_index))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex - 1
                                    if table_name != IqvsubtextDb:
                                        row.SequenceID = row.SequenceID - 1
                        else:
                            del_obj = session.query(table_name).filter(
                                table_name.id == data.get('id')).delete()
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in deleting paragraph data in DB: {exc}")


def db_add(val_list: list):
    """adding paragraph data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        table_name = table_dict.get(content_type)
                        if table_name == IqvdocumentlinkDb:
                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == data.get(
                                'doc_id'), table_name.DocumentSequenceIndex > data.get('DocumentSequenceIndex')))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
                            data = table_name(**data)
                            add_obj = session.add(data)

                        elif table_name == DocumentparagraphsDb:
                            if content_type == 'header':
                                para_data = data[0]
                                obj1 = session.query(table_name).filter(and_(table_name.doc_id == para_data.get('doc_id'), table_name.link_id == para_data.get('link_id'),
                                                                             table_name.link_id_level2 == para_data.get(
                                    'link_id_level2'), table_name.link_id_level3 == para_data.get('link_id_level3'),
                                    table_name.link_id_level4 == para_data.get(
                                    'link_id_level4'), table_name.link_id_level5 == para_data.get('link_id_level5'),
                                    table_name.link_id_level6 == para_data.get(
                                    'link_id_level6'), table_name.link_id_subsection1 == para_data.get('link_id_subsection1'),
                                    table_name.link_id_subsection2 == para_data.get(
                                    'link_id_subsection2'), table_name.link_id_subsection3 == para_data.get('link_id_subsection3'),
                                    table_name.parent_id == para_data.get('parent_id'), table_name.DocumentSequenceIndex > para_data.get('DocumentSequenceIndex')))
                                for row in obj1:
                                    if row is not None:
                                        row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
                                        row.SequenceID = row.SequenceID + 1

                            for para_data in data[1:]:
                                obj1 = session.query(table_name).filter(and_(table_name.doc_id == para_data.get('doc_id'), table_name.link_id == para_data.get('link_id'),
                                                                             table_name.link_id_level2 == para_data.get(
                                    'link_id_level2'), table_name.link_id_level3 == para_data.get('link_id_level3'),
                                    table_name.link_id_level4 == para_data.get(
                                    'link_id_level4'), table_name.link_id_level5 == para_data.get('link_id_level5'),
                                    table_name.link_id_level6 == para_data.get(
                                    'link_id_level6'), table_name.link_id_subsection1 == para_data.get('link_id_subsection1'),
                                    table_name.link_id_subsection2 == para_data.get(
                                    'link_id_subsection2'), table_name.link_id_subsection3 == para_data.get('link_id_subsection3'),
                                    table_name.parent_id == para_data.get('parent_id'), table_name.DocumentSequenceIndex > para_data.get('DocumentSequenceIndex')))
                                for row in obj1:
                                    if row is not None:
                                        row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
                                        row.SequenceID = row.SequenceID + 1
                                para_data = table_name(**para_data)
                                add_obj = session.add(para_data)
                        elif table_name == IqvsubtextDb:
                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == data.get('doc_id'), table_name.link_id == data.get('link_id'),
                                                                         table_name.link_id_level2 == data.get(
                                'link_id_level2'), table_name.link_id_level3 == data.get('link_id_level3'),
                                table_name.link_id_level4 == data.get(
                                'link_id_level4'), table_name.link_id_level5 == data.get('link_id_level5'),
                                table_name.link_id_level6 == data.get(
                                'link_id_level6'), table_name.link_id_subsection1 == data.get('link_id_subsection1'),
                                table_name.link_id_subsection2 == data.get(
                                'link_id_subsection2'), table_name.link_id_subsection3 == data.get('link_id_subsection3'),
                                table_name.parent_id == data.get('parent_id'), table_name.DocumentSequenceIndex > data.get('DocumentSequenceIndex')))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
                            data = table_name(**data)
                            add_obj = session.add(data)

                        else:
                            data = table_name(**data)
                            add_obj = session.add(data)
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in adding paragraph data in DB: {exc}")


def db_add_image(val_list: list):
    """adding Image data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        table_name = table_dict.get(content_type)

                        for para_data in data:
                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == para_data.get('doc_id'), table_name.link_id == para_data.get('link_id'),
                                                                         table_name.link_id_level2 == para_data.get(
                                'link_id_level2'), table_name.link_id_level3 == para_data.get('link_id_level3'),
                                table_name.link_id_level4 == para_data.get(
                                'link_id_level4'), table_name.link_id_level5 == para_data.get('link_id_level5'),
                                table_name.link_id_level6 == para_data.get(
                                'link_id_level6'), table_name.link_id_subsection1 == para_data.get('link_id_subsection1'),
                                table_name.link_id_subsection2 == para_data.get(
                                'link_id_subsection2'), table_name.link_id_subsection3 == para_data.get('link_id_subsection3'),
                                table_name.parent_id == para_data.get('parent_id'), table_name.DocumentSequenceIndex > para_data.get('DocumentSequenceIndex')))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
                                    row.SequenceID = row.SequenceID + 1
                            para_data = table_name(**para_data)
                            add_obj = session.add(para_data)
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in adding Image data in DB: {exc}")


def db_update_image(val_list: list):
    """updating Image data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        line_id = data['line_id']
                        chunks = [line_id[i:i+36]
                                  for i in range(0, len(line_id), 36)]
                        id = chunks[0]
                        table_name = table_dict.get(content_type)
                        obj = session.query(table_name).filter(
                            table_name.id == id)
                        for row in obj:
                            row.strText = data.get('content')
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in updating Image data in DB: {exc}")


def db_delete_image(val_list: list):
    """deleting Image data in DB"""
    try:
        with Session() as session:
            for data_dict in val_list:
                for content_type, data in data_dict.items():
                    if data is not None and len(data) > 0:
                        line_detail = None
                        line_id = data['line_id']
                        chunks = [line_id[i:i+36]
                                  for i in range(0, len(line_id), 36)]
                        for id in chunks:
                            obj = session.query(table_name).filter(
                                table_name.id == id)
                            for row in obj:
                                line_detail = row.__dict__
                            table_name = table_dict.get(content_type)
                            del_obj = session.query(table_name).filter(
                                table_name.id == id).delete()

                            obj1 = session.query(table_name).filter(and_(table_name.doc_id == line_detail.get('doc_id'), table_name.link_id == line_detail.get('link_id'),
                                                                         table_name.link_id_level2 == line_detail.get(
                                'link_id_level2'), table_name.link_id_level3 == line_detail.get('link_id_level3'),
                                table_name.link_id_level4 == line_detail.get(
                                'link_id_level4'), table_name.link_id_level5 == line_detail.get('link_id_level5'),
                                table_name.link_id_level6 == line_detail.get(
                                'link_id_level6'), table_name.link_id_subsection1 == line_detail.get('link_id_subsection1'),
                                table_name.link_id_subsection2 == line_detail.get(
                                'link_id_subsection2'), table_name.link_id_subsection3 == line_detail.get('link_id_subsection3'),
                                table_name.parent_id == line_detail.get('parent_id'), table_name.DocumentSequenceIndex > line_detail.get('DocumentSequenceIndex')))
                            for row in obj1:
                                if row is not None:
                                    row.DocumentSequenceIndex = row.DocumentSequenceIndex - 1
                                    row.SequenceID = row.SequenceID - 1
            session.commit()
    except Exception as exc:
        logger.exception(
            f"Exception received in deleting Image data in DB: {exc}")


def get_prev_line_detail(id: str, content_type: str):
    """getting previous line detail from DB"""
    try:
        prev_line_details = None
        with Session() as session:
            table_name = table_dict.get(content_type)
            obj = session.query(table_name).filter(
                table_name.id == id)
            for row in obj:
                prev_line_details = row.__dict__
        return prev_line_details
    except Exception as exc:
        logger.exception(
            f"Exception received in getting previous line detail from DB: {exc}")
