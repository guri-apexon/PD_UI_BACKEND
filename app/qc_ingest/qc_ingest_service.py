
import logging
import json
from copy import deepcopy
from app.utilities.config import settings
from .model.documentparagraphs_db import DocumentparagraphsDb
from .model.iqvdocumentimagebinary_db import IqvdocumentimagebinaryDb
from .model.documentpartlist_db import DocumentpartslistDb
from .model.iqvdocument_link_db import IqvdocumentlinkDb
from .model.documenttables_db import DocumenttablesDb, TableOp
from .model.iqvfootnoterecord_db import IqvfootnoterecordDb
from .model.iqvpage_roi_db import IqvpageroiDb
from .iqvkeyvalueset_op import IqvkeyvaluesetOp
from .model.__base__ import MissingParamException, update_link_update_details, get_utc_datetime
from .table_payload_wrapper import get_table_props
from app.db.session import SessionLocal

logger = logging.getLogger(settings.LOGGER_NAME)

# documentPartListDb and DocumentParagraph has same id for all lines .PartListDb and then paragraph updated with sameinfo
# imagebinary db internally updates paragraph db,there also partlist should be updated
# linkdb generated link will be updated to partlistdb and paragraph db.


class RelationalMapper():

    RelationMap = {
        "header": {
            "name": IqvdocumentlinkDb,
            "children": [DocumentpartslistDb, DocumentparagraphsDb]
        },
        "text": {
            "name": DocumentpartslistDb,
            "children": [DocumentparagraphsDb]
        },
        "image": {
            "name": DocumentpartslistDb,
            "children": [IqvdocumentimagebinaryDb]
        },
        "table":{
            "name": DocumenttablesDb,
            "children":[IqvfootnoterecordDb, IqvkeyvaluesetOp]

        }

    }

    def create(self, session, data):
        relation_name = data['type']
        rel_map = RelationalMapper.RelationMap[relation_name]
        table = rel_map['name']
        data = table.create(session, data)
        for child_table in rel_map['children']:
            child_table.create(session, data)

    def update(self, session, data):
        relation_name = data['type']
        rel_map = RelationalMapper.RelationMap.get(relation_name,None)
        if not rel_map:
            raise Exception(f'unknown relation type in request -- {relation_name} -- ')
        table = rel_map['name']
        table.update(session, data)
        for child_table in rel_map['children']:
            child_table.update(session, data)

    def delete(self, session, data):
        relation_name = data['type']
        rel_map = RelationalMapper.RelationMap[relation_name]
        table = rel_map['name']
        table.delete(session, data)
        for child_table in rel_map['children']:
            child_table.delete(session, data)


def get_table_roi_id(session, line_id):
    col_id = session.query(DocumenttablesDb.parent_id).filter(DocumenttablesDb.id == line_id).first()
    if not col_id:
        raise MissingParamException('record for line_id in Documenttables DB')
    row_id = session.query(DocumenttablesDb.parent_id).filter(DocumenttablesDb.id == col_id[0]).first()
    if not row_id:
        raise MissingParamException('row_id for line_id in Documenttables DB')
    table_id = session.query(DocumenttablesDb.parent_id).filter(DocumenttablesDb.id == row_id[0]).first()
    if not table_id:
        raise MissingParamException('table_id for line_id in Documenttables DB')
    return table_id[0]

    
def get_content_info(data: dict, session):
    """
    use prev_line id for add ,delete update curr line id used
    """
    try:
        action_type = data['qc_change_type']
        action_list = list()
        prev_line_id,next_line_id, table_props, footnote_list = None, None, None, None
        if data.get('type') == 'table':
            if action_type != TableOp.ADD:
                line_id = data.get('line_id', '')[0:36]
                if not line_id:
                    raise MissingParamException('line_id')
                data['table_roi_id'] = get_table_roi_id(session, line_id)
            table_props, footnote_list = get_table_props(action_type, data)
        if action_type == TableOp.ADD:
            prev_details = data.get('prev_detail',{})
            prev_line_id = prev_details.get('line_id', '')[0:36]
            next_details=data.get('next_detail',{})
            next_line_id=next_details.get('line_id','')[0:36]
        data['prev_id'] = prev_line_id
        data['next_id']=next_line_id
        data['id'] = data.get('line_id', '')[0:36]
        audit = data.get('audit', {})
        data['userId'] = audit.get('last_updated_user', None)

        if table_props == None or len(table_props) == 0:
            if footnote_list != None and len(footnote_list) > 0:
                data['AttachmentListProperties'] = footnote_list
            action_list.append(data)
        else:
            for index, table_props_data in enumerate(table_props):
                if not table_props_data.get('op_type', None):
                    raise MissingParamException('op_type')
                if not table_props_data.get('op_params', None) and table_props_data['op_type'] != 'delete_table':
                    raise MissingParamException('op_params')
                data['op_type'] = table_props_data['op_type']
                data['op_params'] = table_props_data['op_params']
                if index == len(table_props)-1:
                    data['AttachmentListProperties'] = footnote_list
                else:
                    data['AttachmentListProperties'] = None
                action_data = deepcopy(data)
                action_list.append(action_data)
        return action_type, action_list
    except Exception as e:
        raise Exception("Invalid input parameters : "+str(e))


def process_data(session, mapper, data: dict):
    action_name, action_list = get_content_info(data, session)
    for action_data in action_list:
        if action_name == TableOp.ADD and action_data:
            mapper.create(session, action_data)
        elif action_name == TableOp.MODIFY and action_data:
            mapper.update(session, action_data)
        elif action_name == TableOp.DELETE and action_data:
            mapper.delete(session, action_data)
        session.commit()
    return data


def process(payload: list):
    """
    commit for every part in payload 
    """

    if not payload:
        return []
    mapper = RelationalMapper()
    uid_list=[]
    link_id, user_id, is_section_header = None, None, False
    with SessionLocal() as session:
        for data in payload:  
            data = process_data(session, mapper, data)
            uid_list.append({'uuid':data.get('uuid',''),
                             'op_type':data.get('op_type',''),
                             'qc_change_type':data.get('qc_change_type','')})

            if data.get('type') == 'header' and data.get('link_level') in ['1',1]:
                link_id = None
                is_section_header = True
            
            if is_section_header == False:
                if link_id == None and data.get('link_id') in ['', None]:
                    _id = data.get('line_id', '')[0:36] if data.get("line_id") not in ['', None] else data.get('uuid')
                    obj = session.query(IqvpageroiDb).filter(IqvpageroiDb.id == _id).first()
                    if obj:
                        link_id = obj.link_id
                elif link_id == None and data.get('link_id') not in ['', None]:
                    link_id = data.get('link_id')
                user_id = data.get('userId')
        if link_id not in ['', None] and user_id != None:
            update_link_update_details(session, link_id, user_id, get_utc_datetime())
            session.commit()
    return uid_list
