import psycopg2
import pandas as pd
from model import *
import json
import uuid
from document import Document, Fontinfo, DocumentLink, Subtext
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from config import settings
URL = settings.LOCAL_DB_URL
engine = create_engine(URL, echo=True)
Session = sessionmaker(bind=engine)

with open('QC_add_pyload.txt', 'r') as f:
    data = f.read()
    payload = json.loads(data)

table_dict = {'text': DocumentparagraphsDb, 'image': DocumentimagesDb, 'table': DocumenttablesDb, 'item': DocumentitemsDb,
              'header': DocumentheadersDb, 'footer': DocumentfootersDb, 'font_info': FontinfoDb, 'link_db': IqvdocumentlinkDb, 'subtext': IqvsubtextDb}

link_level_dict = {"1": "link_id",
                   "2": "link_id_level2",
                   "3": "link_id_level3",
                   "4": "link_id_level4",
                   "5": "link_id_level5",
                   "6": "link_id_level6",
                   "7": "link_id_subsection1",
                   "8": "link_id_subsection2",
                   "9": "link_id_subsection3", }


def db_update(val_list):
    with Session() as session:
        for data_dict in val_list:
            for content_type, data in data_dict.items():
                table_name = table_dict.get(content_type)
                obj = session.query(table_name).filter(
                    table_name.id == data.get('id'))
                for row in obj:
                    for key, val in data.items():
                        if hasattr(row, key):
                            setattr(row, key, val)
        session.commit()


def db_delete(val_list):
    with Session() as session:
        for data_dict in val_list:
            for content_type, data in data_dict.items():
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
                        row.DocumentSequenceIndex = row.DocumentSequenceIndex - 1

                elif table_name != FontinfoDb:
                    obj = session.query(table_name).filter(
                        table_name.id == data.get('id'))
                    for row in obj:
                        document_sequence_index = row.DocumentSequenceIndex
                    del_obj = session.query(table_name).filter(
                        table_name.id == data.get('id')).delete()
                    obj1 = session.query(table_name).filter(and_(table_name.doc_id == data.get(
                        'doc_id'), table_name.link_id == data.get('link_id'), table_name.parent_id == data.get('parent_id'), table_name.DocumentSequenceIndex > document_sequence_index))
                    for row in obj1:
                        row.DocumentSequenceIndex = row.DocumentSequenceIndex - 1
                else:
                    del_obj = session.query(table_name).filter(
                        table_name.id == data.get('id')).delete()
        session.commit()


def db_add():
    pass


def get_font_info_dict(font_info):
    font_info_dict = dict()
    font_info_db = FontinfoDb.__dict__
    for key in font_info_db.keys():
        font_info_dict[key] = font_info.get(key)
    return font_info_dict


def get_subtext_info_dict(data, roi_id):
    subtext_info_dict = dict()
    subtext_info_dict['id'] = roi_id['subtext']
    subtext_info_dict['parent_id'] = roi_id['childbox']
    subtext_info_dict['strText'] = data.get('content')
    subtext_info_dict['doc_id'] = data.get('aidocid')
    subtext_info_dict['link_id'] = data['font_info']['link_id']
    return subtext_info_dict


def get_content_info_dict(data, roi_id):
    content_info_dict = dict()
    content_info_dict['id'] = roi_id['childbox']
    content_info_dict['parent_id'] = roi_id['para']
    content_info_dict['strText'] = data.get('content')
    content_info_dict['doc_id'] = data.get('aidocid')
    content_info_dict['link_id'] = data['font_info']['link_id']
    return content_info_dict


def get_header_info_dict(data):
    header_info_dict = dict()
    link_level = link_level_dict[data['file_section_level']]
    header_info_dict['id'] = data['font_info'][link_level]
    header_info_dict['strText'] = data.get('content')
    header_info_dict['doc_id'] = data.get('aidocid')
    header_info_dict['link_id'] = data['font_info']['link_id']
    return header_info_dict


def get_content_info(data):
    content_info_dict = None
    font_info_dict = None
    subtext_info_dict = None
    header_info_dict = None
    font_info = data.get('font_info')
    if data.get('type') == 'text':
        content_info_dict = get_content_info_dict(
            data, font_info['roi_id'])
        font_info_dict = get_font_info_dict(font_info)
        subtext_info_dict = get_subtext_info_dict(data, font_info['roi_id'])
    if data.get('type') == 'header':
        header_info_dict = get_header_info_dict(data)
    return content_info_dict, font_info_dict, subtext_info_dict, header_info_dict

def get_prev_line_detail(id,content_type):
    with Session() as session:
        table_name = table_dict.get(content_type)
        obj = session.query(table_name).filter(
            table_name.id == id)
        for row in obj:
            document_sequence_index = row.DocumentSequenceIndex
            sequence_id = row.SequenceID
    return document_sequence_index, sequence_id

def get_update_next_line_detail(id,content_type):
    with Session() as session:
        table_name = table_dict.get(content_type)
        obj = session.query(table_name).filter(
            table_name.id == id)
        for row in obj:
            row.DocumentSequenceIndex = row.DocumentSequenceIndex + 1
            row.SequenceID = row.SequenceID + 1

# document_sequence_index, sequence_id = get_prev_next_line_detail('e1aec867-bd34-4013-a6d7-e72d3ee1a3a8','text')
# print(document_sequence_index)

def build_content_info_dict(data):
    prev_para_id = data['prev_line_detail']['roi_id']['para']
    document_sequence_index, sequence_id = get_prev_line_detail(prev_para_id,data.get('type'))
    new_para_line = Document()
    _id = uuid.uuid4()
    _id = str(_id)
    new_para_line.id = _id
    new_para_line.doc_id = data['aidocid']
    new_para_line.parent_id = data['aidocid']
    new_para_line.hierarchy = 'paragraph'
    new_para_line.group_type = 'DocumentParagraphs'
    new_para_line.link_id = data['prev_line_detail']['link_id']
    new_para_line.link_id_level2 = data['prev_line_detail']['link_id_level2']
    new_para_line.link_id_level3 = data['prev_line_detail']['link_id_level3']
    new_para_line.link_id_level4 = data['prev_line_detail']['link_id_level4']
    new_para_line.link_id_level5 = data['prev_line_detail']['link_id_level5']
    new_para_line.link_id_level6 = data['prev_line_detail']['link_id_level6']
    new_para_line.link_id_subsection1 = data['prev_line_detail']['link_id_subsection1']
    new_para_line.link_id_subsection2 = data['prev_line_detail']['link_id_subsection2']
    new_para_line.link_id_subsection3 = data['prev_line_detail']['link_id_subsection3']
    new_para_line.DocumentSequenceIndex = document_sequence_index + 1
    new_para_line.SequenceID = sequence_id + 1
    new_para_line.bIsCheckbox = False

    childbox_list = list()
    childbox_list.append(new_para_line)
    for index in range(len(data['content'])):
        if data['content'][index]['type'] == 'text':
            new_childbox_line = Document()
            _id = uuid.uuid4()
            _id = str(_id)
            new_childbox_line.id = _id
            new_childbox_line.doc_id = data['aidocid']
            new_childbox_line.parent_id = new_para_line.doc_id
            new_childbox_line.hierarchy = 'paragraph'
            new_childbox_line.group_type = 'ChildBoxes'
            new_childbox_line.strText = data['content'][index]['content']
            new_childbox_line.link_id = data['prev_line_detail']['link_id']
            new_childbox_line.link_id_level2 = data['prev_line_detail']['link_id_level2']
            new_childbox_line.link_id_level3 = data['prev_line_detail']['link_id_level3']
            new_childbox_line.link_id_level4 = data['prev_line_detail']['link_id_level4']
            new_childbox_line.link_id_level5 = data['prev_line_detail']['link_id_level5']
            new_childbox_line.link_id_level6 = data['prev_line_detail']['link_id_level6']
            new_childbox_line.link_id_subsection1 = data['prev_line_detail']['link_id_subsection1']
            new_childbox_line.link_id_subsection2 = data['prev_line_detail']['link_id_subsection2']
            new_childbox_line.link_id_subsection3 = data['prev_line_detail']['link_id_subsection3']
            new_childbox_line.DocumentSequenceIndex = index
            new_childbox_line.SequenceID = index
            new_childbox_line.bIsCheckbox = True
            childbox_list.append(new_childbox_line)
    next_para_id = data['next_line_detail']['roi_id']['para']
    document_sequence_index, sequence_id = get_update_next_line_detail(next_para_id,data.get('type'))
    return childbox_list

def build_font_info_dict(data):
    pass

def build_subtext_info_dict(data):
    pass

def build_header_info_dict(data):
    pass

def get_add_content_info(data):
    content_info_dict = None
    font_info_dict = None
    subtext_info_dict = None
    header_info_dict = None
    content_info_dict = build_content_info_dict(data)
    font_info_dict = build_font_info_dict(data)
    subtext_info_dict = build_subtext_info_dict(data)
    header_info_dict = build_header_info_dict(data)
    return content_info_dict, font_info_dict, subtext_info_dict, header_info_dict




def get_action_dict(payload):
    action_dict = {'modify': [], 'delete': [], 'add': []}
    for data in payload:
        action = data.get('qc_change_type')
        if action == 'add':
            content_info_dict, font_info_dict, subtext_info_dict, header_info_dict = get_add_content_info(
                data)
        else:
            content_info_dict, font_info_dict, subtext_info_dict, header_info_dict = get_content_info(
                data)
            if content_info_dict != None and font_info_dict != None and subtext_info_dict != None:
                (action_dict[action]).append(
                    {'font_info': font_info_dict, data.get('type'): content_info_dict, 'subtext': subtext_info_dict})
            elif header_info_dict != None:
                (action_dict[action]).append(
                    {'link_db': header_info_dict})

    return action_dict


def process(payload):
    action_dict = get_action_dict(payload)
    for key, val in action_dict.items():
        # if key == 'modify' and len(val)>0:
        #     db_update(val)
        if key == 'delete' and len(val) > 0:
            db_delete(val)

process(payload)
