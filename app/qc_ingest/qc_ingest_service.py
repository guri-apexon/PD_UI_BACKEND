
import logging
from app.utilities.config import settings
from ..db.session import SessionLocal
from .model.documentparagraphs_db import DocumentparagraphsDb
from .model.iqvdocumentimagebinary_db import IqvdocumentimagebinaryDb
from .model.documentpartlist_db import DocumentpartslistDb
from .model.iqvdocument_link_db import IqvdocumentlinkDb
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


def get_content_info(data: dict, action_type):
    """
    use prev_line id for add ,delete update curr line id used
    """
    try:
        line_id, prev_link_id, prev_line_id = None, None, None
        if action_type == 'add':
            prev_details = data['prev_detail']
            prev_line_id = prev_details.get('line_id', '')[0:36]
            prev_link_id = prev_details.get('link_record_uid', '')
        data['prev_id'] = prev_line_id
        data['prev_link_record_uid'] = prev_link_id
        data['id'] = data.get('line_id', '')
        data['link_record_uid'] = data.get('link_record_uid', '')
        return data
    except Exception as e:
        raise Exception("Invalid input parameters : "+str(e))


def process_data(session, mapper, data: dict):
    action_name = data['qc_change_type']
    action_data = get_content_info(data, action_name)
    if action_name == 'add' and action_data:
        mapper.create(session, action_data)
    elif action_name == 'modify' and action_data:
        mapper.update(session, action_data)
    elif action_name == 'delete' and action_data:
        mapper.delete(session, action_data)


def process(payload: list):
    """
    commit for every part in payload 
    """

    if not payload:
        return True
    mapper = RelationalMapper()
    with SessionLocal() as session:
        for data in payload:   
            process_data(session, mapper, data)
        session.commit()
    return True
