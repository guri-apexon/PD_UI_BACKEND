from .model import *
import uuid
from .document import *
from .db_utils import *
import logging
from app.utilities.config import settings


logger = logging.getLogger(settings.LOGGER_NAME)

table_dict = TableType.table_dict

link_level_dict = Linklevel.link_level_dict


def get_font_info_dict(font_info: dict, header_info_dict):
    """building fontinfo dict"""
    try:
        font_info_db = Fontinfo()
        if len(font_info) > 0:
            for key, val in font_info.items():
                if hasattr(font_info_db, key):
                    setattr(font_info_db, key, val)
            if header_info_dict:
                font_info_db.link_id = header_info_dict['link_id']
                font_info_db.link_id_level2 = header_info_dict['link_id_level2']
                font_info_db.link_id_level3 = header_info_dict['link_id_level3']
                font_info_db.link_id_level4 = header_info_dict['link_id_level4']
                font_info_db.link_id_level5 = header_info_dict['link_id_level5']
                font_info_db.link_id_level6 = header_info_dict['link_id_level6']
                font_info_db.link_id_subsection1 = header_info_dict['link_id_subsection1']
                font_info_db.link_id_subsection2 = header_info_dict['link_id_subsection2']
                font_info_db.link_id_subsection3 = header_info_dict['link_id_subsection3']

    except Exception as exc:
        logger.exception(
            f"Exception received in get_font_info_dict: {exc}")

    return font_info_db.__dict__


def get_info_dict(data: dict, id: str, parent_id: str):
    """building info dict for paragraph, subtext and header for modify and delete"""
    try:
        new_info_dict = dict()
        new_info_dict['id'] = id
        new_info_dict['parent_id'] = parent_id
        content = data.get('content')
        if data.get('type') == 'header':
            new_info_dict['LinkText'] = content
            if content[0].isdigit():
                content_list = content.split(' ')
                new_info_dict['LinkPrefix'] = content_list[0]
        else:
            new_info_dict['strText'] = content
        new_info_dict['doc_id'] = data.get('aidocid')
        new_info_dict['link_id'] = data['font_info']['link_id']
        new_info_dict['link_id_level2'] = data['font_info']['link_id_level2']
        new_info_dict['link_id_level3'] = data['font_info']['link_id_level3']
        new_info_dict['link_id_level4'] = data['font_info']['link_id_level4']
        new_info_dict['link_id_level5'] = data['font_info']['link_id_level5']
        new_info_dict['link_id_level6'] = data['font_info']['link_id_level6']
        new_info_dict['link_id_subsection1'] = data['font_info']['link_id_subsection1']
        new_info_dict['link_id_subsection2'] = data['font_info']['link_id_subsection2']
        new_info_dict['link_id_subsection3'] = data['font_info']['link_id_subsection3']
        return new_info_dict
    except Exception as exc:
        logger.exception(
            f"Exception received in get_info_dict: {exc}")


def get_content_info(data: dict):
    """getting complete info for modify or delete"""
    try:
        content_info_dict = None
        font_info_dict = None
        subtext_info_dict = None
        header_info_dict = None
        font_info = data.get('font_info')
        line_id = data.get('line_id')
        chunks = [line_id[i:i+36] for i in range(0, len(line_id), 36)]
        if data.get('type') == 'text':
            content_info_dict = get_info_dict(data, chunks[1], chunks[0])
            subtext_info_dict = get_info_dict(data, chunks[2], chunks[1])
            font_info_dict = get_font_info_dict(font_info, header_info_dict)
        if data.get('type') == 'header':
            link_level = link_level_dict[data['file_section_level']]
            id = data['font_info'][link_level]
            header_info_dict = get_info_dict(data, id, data['aidocid'])
        return content_info_dict, font_info_dict, subtext_info_dict, header_info_dict
    except Exception as exc:
        logger.exception(
            f"Exception received in get_content_info: {exc}")


def build_info_dict(data: dict, prev_para_id: str, header_info_dict, info_dict: dict, line_id: str, subtext_id: str, prev_line_data_type: str):
    """building info dict for add"""
    try:
        prev_line_details = get_prev_line_detail(
            prev_para_id, prev_line_data_type)
        new_para_line = Document()
        new_childbox_line = Document()
        new_subtext_line = Subtext()
        if prev_line_details is None:
            if info_dict.get(line_id):
                prev_line_details = info_dict[line_id]['new_para_line_dict']
        if prev_line_details is not None:
            for key, val in prev_line_details.items():
                if hasattr(new_para_line, key):
                    setattr(new_para_line, key, val)
            _id = uuid.uuid4()
            _id = str(_id)
            new_para_line.id = _id
            new_para_line.hierarchy = 'paragraph'
            new_para_line.group_type = 'DocumentParagraphs'
            new_para_line.DocumentSequenceIndex = new_para_line.DocumentSequenceIndex + 1
            new_para_line.SequenceID = new_para_line.SequenceID + 1
            if data.get('type') == 'header':
                new_para_line.link_id = header_info_dict['link_id']
                new_para_line.link_id_level2 = header_info_dict['link_id_level2']
                new_para_line.link_id_level3 = header_info_dict['link_id_level3']
                new_para_line.link_id_level4 = header_info_dict['link_id_level4']
                new_para_line.link_id_level5 = header_info_dict['link_id_level5']
                new_para_line.link_id_level6 = header_info_dict['link_id_level6']
                new_para_line.link_id_subsection1 = header_info_dict['link_id_subsection1']
                new_para_line.link_id_subsection2 = header_info_dict['link_id_subsection2']
                new_para_line.link_id_subsection3 = header_info_dict['link_id_subsection3']

            new_para_line = new_para_line.__dict__
            for key, val in new_para_line.items():
                if hasattr(new_childbox_line, key):
                    setattr(new_childbox_line, key, val)
                _id = uuid.uuid4()
                _id = str(_id)
                new_childbox_line.id = _id
                new_childbox_line.parent_id = new_para_line['id']
                new_childbox_line.group_type = 'ChildBoxes'
                new_childbox_line.strText = data['content']
                new_childbox_line.DocumentSequenceIndex = 0
                new_childbox_line.SequenceID = 0
                new_childbox_line.bIsCheckbox = True

            new_childbox_line = new_childbox_line.__dict__
            prev_subtext_line_details = None
            if subtext_id is not None:
                prev_subtext_line_details = get_prev_line_detail(
                    prev_para_id, 'subtext')

            if prev_subtext_line_details is not None:
                for key, val in prev_subtext_line_details.items():
                    if hasattr(new_subtext_line, key):
                        setattr(new_subtext_line, key, val)
            _id = uuid.uuid4()
            _id = str(_id)
            new_subtext_line.id = _id
            new_subtext_line.doc_id = new_childbox_line['doc_id']
            new_subtext_line.link_id = new_childbox_line['link_id']
            new_subtext_line.link_id_level2 = new_childbox_line['link_id_level2']
            new_subtext_line.link_id_level3 = new_childbox_line['link_id_level3']
            new_subtext_line.link_id_level4 = new_childbox_line['link_id_level4']
            new_subtext_line.link_id_level5 = new_childbox_line['link_id_level5']
            new_subtext_line.link_id_level6 = new_childbox_line['link_id_level6']
            new_subtext_line.link_id_subsection1 = new_childbox_line['link_id_subsection1']
            new_subtext_line.link_id_subsection2 = new_childbox_line['link_id_subsection2']
            new_subtext_line.link_id_subsection3 = new_childbox_line['link_id_subsection3']
            new_subtext_line.strText = new_childbox_line['strText']
            new_subtext_line.parent_id = new_childbox_line['id']
            if subtext_id is None:
                new_subtext_line.group_type = 'IQVSubTextList'
                new_subtext_line.hierarchy = "paragraph"
                new_subtext_line.iqv_standard_term = ""
                new_subtext_line.bNoTranslate = False
                new_subtext_line.reservedTypeVal = 0
                new_subtext_line.parent2LocalName = ""
                new_subtext_line.Value = ""
                new_subtext_line.OuterXml = ""
                new_subtext_line.strTranslatedText = ""
                new_subtext_line.runElementName = "t"
                new_subtext_line.DocumentSequenceIndex = 0
                new_subtext_line.sequence = -1
                new_subtext_line.startCharIndex = 0

            new_subtext_line = new_subtext_line.__dict__
        return prev_line_details, new_para_line, new_childbox_line, new_subtext_line
    except Exception as exc:
        logger.exception(
            f"Exception received in build_info_dict: {exc}")


def build_header_info_dict(data: dict, prev_para_id: str):
    """building header info dict for add"""
    try:
        prev_line_details = get_prev_line_detail(
            prev_para_id, 'link_db')
        new_line = DocumentLink()
        if prev_line_details is not None:
            for key, val in prev_line_details.items():
                if hasattr(new_line, key):
                    setattr(new_line, key, val)
            _id = uuid.uuid4()
            _id = str(_id)
            new_line.id = _id
            content = data.get('content')
            new_line.LinkText = content
            if content[0].isdigit():
                content_list = content.split(' ')
                new_line.LinkPrefix = content_list[0]
                new_line.iqv_standard_term = "cpt_" + \
                    ' '.join(content_list[1:])
            else:
                new_line.LinkPrefix = ""
                new_line.iqv_standard_term = ' '.join(content_list)
            new_line.DocumentSequenceIndex = new_line.DocumentSequenceIndex + 1
            new_line.LinkLevel = new_line.LinkLevel + 1
            link_level = link_level_dict[str(new_line.LinkLevel)]
            new_link_id = uuid.uuid4()
            new_link_id = str(_id)
            new_line = new_line.__dict__
            new_line[link_level] = new_link_id

        return new_line
    except Exception as exc:
        logger.exception(
            f"Exception received in build_header_info_dict: {exc}")


def get_add_content_info(data: dict, info_dict: dict):
    """getting add info dict for text"""
    try:
        new_para_line_dict = None
        new_childbox_line_dict = None
        font_info_dict = None
        subtext_info_dict = None
        header_info_dict = None
        prev_line_details = None
        link_level = None
        if data.get('type') == 'header':
            link_level = link_level_dict[data['prev_line_detail']['file_section_level']]
            if link_level != "":
                prev_para_id = data['prev_line_detail'][link_level]
                header_info_dict = build_header_info_dict(data, prev_para_id)
        if link_level != "":
            prev_line_id = data['prev_line_detail']['line_id']
            prev_line_data_type = data['prev_line_detail']['type']
            chunks = [prev_line_id[i:i+36]
                    for i in range(0, len(prev_line_id), 36)]
            prev_para_id = chunks[0]
            subtext_id = None
            if len(chunks) == 3:
                subtext_id = chunks[2]
            line_id = data.get('line_id')
            prev_line_details, new_para_line_dict, new_childbox_line_dict, subtext_info_dict = build_info_dict(
                data, prev_para_id, header_info_dict, info_dict, prev_line_id, subtext_id, prev_line_data_type)
            font_info_dict = get_font_info_dict(
                data['font_info'], header_info_dict)
            info_dict[line_id] = {'new_para_line_dict': new_para_line_dict,
                                'new_childbox_line_dict': new_childbox_line_dict,
                                'subtext_info_dict': subtext_info_dict,
                                'header_info_dict': header_info_dict,
                                'font_info_dict': font_info_dict}
            return prev_line_details, new_para_line_dict, new_childbox_line_dict, font_info_dict, subtext_info_dict, header_info_dict
    except Exception as exc:
        logger.exception(
            f"Exception received in get_add_content_info: {exc}")


def get_action_dict(payload: str):
    """getting action dict for text"""
    try:
        action_dict = {'modify': [], 'delete': [], 'add': []}
        info_dict = dict()
        for data in payload:
            action = data.get('qc_change_type')
            if action == 'add':
                prev_line_details, new_para_line_dict, new_childbox_line_dict, font_info_dict, subtext_info_dict, header_info_dict = get_add_content_info(
                    data, info_dict)
                (action_dict[action]).append(
                    {'font_info': font_info_dict, data.get('type'): [prev_line_details, new_para_line_dict, new_childbox_line_dict], 'subtext': subtext_info_dict, 'link_db': header_info_dict})
            elif action == 'modify' or action == 'delete':
                content_info_dict, font_info_dict, subtext_info_dict, header_info_dict = get_content_info(
                    data)
                if content_info_dict != None and font_info_dict != None and subtext_info_dict != None:
                    (action_dict[action]).append(
                        {'font_info': font_info_dict, data.get('type'): content_info_dict, 'subtext': subtext_info_dict})
                elif header_info_dict != None:
                    (action_dict[action]).append(
                        {'link_db': header_info_dict})

        return action_dict
    except Exception as exc:
        logger.exception(
            f"Exception received in get_action_dict: {exc}")


def process(payload: list):
    """processing payload for text data"""
    try:
        action_dict = get_action_dict(payload)
        for key, val in action_dict.items():
            if key == 'modify' and len(val) > 0:
                db_update(val)
            if key == 'delete' and len(val) > 0:
                db_delete(val)
            if key == 'add' and len(val) > 0:
                db_add(val)
        return True
    except Exception as exc:
        logger.exception(
            f"Exception received in processing text data: {exc}")
