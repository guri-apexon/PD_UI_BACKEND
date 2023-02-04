from .model import *
import uuid
from .document import *
from .db_utils import *

table_dict = TableType.table_dict

link_level_dict = Linklevel.link_level_dict

def get_add_content_info(data: dict):
    """getting add info dict for image"""
    try:
        prev_line_id = data['prev_line_detail']['line_id']
        chunks = [prev_line_id[i:i+36] for i in range(0, len(prev_line_id), 36)]
        prev_para_id = chunks[0]
        prev_line_details = get_prev_line_detail(prev_para_id, data.get('type'))
        new_para_line = Document()
        new_childbox_line = Document()
        if prev_line_details is not None:
            for key, val in prev_line_details.items():
                if hasattr(new_para_line, key):
                    setattr(new_para_line, key, val)
            _id = uuid.uuid4()
            _id = str(_id)
            new_para_line.id = _id
            new_para_line.DocumentSequenceIndex = new_para_line.DocumentSequenceIndex + 1
            new_para_line.SequenceID = new_para_line.SequenceID + 1

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
        return new_para_line, new_childbox_line
    except Exception as exc:
        logger.exception(
            f"Exception received in get_add_content_info: {exc}")
    
def get_action_dict(payload: str):
    """getting action dict for image"""
    try:
        action_dict = {'modify': [], 'delete': [], 'add': []}
        for data in payload:
            action = data.get('qc_change_type')
            if action == 'add':
                new_para_line_dict, new_childbox_line_dict = get_add_content_info(
                    data)
                (action_dict[action]).append(
                        {data.get('type'): [new_para_line_dict, new_childbox_line_dict]})
            elif action == 'modify' or action == 'delete':
                (action_dict[action]).append(
                        {data.get('type'): data})

        return action_dict
    except Exception as exc:
        logger.exception(
            f"Exception received in get_action_dict: {exc}")

def process(payload: dict):
    """processing payload for image data"""
    try:
        action_dict = get_action_dict(payload)
        for key, val in action_dict.items():
            if key == 'modify' and len(val)>0:
                db_update_image(val)
            if key == 'delete' and len(val) > 0:
                db_delete_image(val)
            if key == 'add' and len(val) > 0:
                db_add_image(val)
    except Exception as exc:
        logger.exception(
            f"Exception received in processing image data: {exc}")
