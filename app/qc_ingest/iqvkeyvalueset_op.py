from sqlalchemy import and_
from .model.__base__ import schema_to_dict, MissingParamException, get_table_index
from .model.documenttables_db import DocumenttablesDb, DocTableHelper
from .model.iqvkeyvalueset_db import IqvkeyvaluesetDb
import uuid


class PropertiesMaker():

    def get_keyvalueset(self, key, val, prev_dict, parent_id, hierarchy):
        uid = str(uuid.uuid4())
        keyvalueset = IqvkeyvaluesetDb()
        keyvalueset.id = uid
        keyvalueset.doc_id = prev_dict['doc_id']
        keyvalueset.link_id = prev_dict['link_id']
        keyvalueset.link_id_level2 = prev_dict['link_id_level2']
        keyvalueset.link_id_level3 = prev_dict['link_id_level3']
        keyvalueset.link_id_level4 = prev_dict['link_id_level4']
        keyvalueset.link_id_level5 = prev_dict['link_id_level5']
        keyvalueset.link_id_level6 = prev_dict['link_id_level6']
        keyvalueset.link_id_subsection1 = prev_dict['link_id_subsection1']
        keyvalueset.link_id_subsection2 = prev_dict['link_id_subsection2']
        keyvalueset.link_id_subsection3 = prev_dict['link_id_subsection3']
        keyvalueset.parent_id = parent_id
        keyvalueset.group_type = 'Properties'
        keyvalueset.key = key
        keyvalueset.value = val
        keyvalueset.hierarchy = hierarchy
        keyvalueset.confidence = 0
        keyvalueset.rawScore = 0
        return keyvalueset

    def update_table_properties(self, row, table_index, table_name, prev_dict, session):
        """

        """
        table_properties_list = list()
        for col in row:
            table_properties_dict = {'TableIndex': table_index, 'RowIndex': int(table_index)*1000+col['row_idx']+1,
                                     'ColIndex': col['col_idx']+1, 'FootNoteLink': '', 'TableName': table_name, 'FullText': col['val']}
            col_id = col['datacell_roi_id']
            for key, val in table_properties_dict.items():
                obj = session.query(IqvkeyvaluesetDb).filter(and_(
                    IqvkeyvaluesetDb.parent_id == col_id, IqvkeyvaluesetDb.key == key)).first()
                if not obj:
                    keyvalueset = self.get_keyvalueset(
                        key, val, prev_dict, col_id, 'table')
                    table_properties_list.append(keyvalueset)
                else:
                    obj.value = val
                    session.add(obj)
        return table_properties_list

    def update_footnote_properties(self, footnote, table_index, prev_dict, session):
        """

        """
        footnote_properties_list = list()
        attachment_id = footnote['AttachmentId']
        footnote_properties_dict = {'TableIndex': table_index, 'AttachmentId': attachment_id,
                                    'IsFootnote': '', 'FootnoteText': footnote['Text']}
        for key, val in footnote_properties_dict.items():
            obj = session.query(IqvkeyvaluesetDb).filter(and_(
                IqvkeyvaluesetDb.parent_id == attachment_id, IqvkeyvaluesetDb.key == key)).first()
            if not obj:
                keyvalueset = self.get_keyvalueset(
                    key, val, prev_dict, attachment_id, 'paragraph')
                footnote_properties_list.append(keyvalueset)
            else:
                obj.value = val
                session.add(obj)
        return footnote_properties_list

    def update_keyvalueset_db(self, session, data, table_roi_id, table_index):
        """

        """
        doc_table_helper = DocTableHelper()
        table_name = data.get('TableName', "")
        if not table_index or not table_roi_id:
            raise MissingParamException('table_index or table_roi_id')
        table_roi_data = session.query(DocumenttablesDb).filter(
            DocumenttablesDb.id == table_roi_id).first()
        prev_dict = schema_to_dict(table_roi_data)
        table_data = doc_table_helper.get_table(session, table_roi_id)
        for row in table_data.values():
            table_properties_list = self.update_table_properties(
                row, table_index, table_name, prev_dict, session)
            for table_properties in table_properties_list:
                session.add(table_properties)
        if data['AttachmentListProperties'] != None:
            table_footnote_data = doc_table_helper.get_table_footnote_data(
                session, table_roi_id)
            for footnote in table_footnote_data:
                footnote_properties_list = self.update_footnote_properties(
                    footnote, table_index, prev_dict, session)
                for footnote_properties in footnote_properties_list:
                    session.add(footnote_properties)
        return table_index


class IqvkeyvaluesetOp():

    @staticmethod
    def create(session, data):
        """

        """
        session.commit()
        table_roi_id = data.get('uuid')
        doc_id = data.get('doc_id')
        properties_maker = PropertiesMaker()
        table_index = get_table_index(session, doc_id, table_roi_id)
        properties_maker.update_keyvalueset_db(
            session, data, table_roi_id, table_index)
        obj = session.query(IqvkeyvaluesetDb).filter(and_(
            IqvkeyvaluesetDb.doc_id == doc_id, IqvkeyvaluesetDb.key == 'TableIndex')).all()
        id_list = list()
        for row in obj:
            table_index_value = int(((row.value).split("."))[0])
            if table_index_value >= int(table_index):
                id_list.append([row.id, table_index_value + 1])
        for i in id_list:
            obj = session.query(IqvkeyvaluesetDb).filter(
                IqvkeyvaluesetDb.id == i[0]).update({IqvkeyvaluesetDb.value: i[1]})
        return data

    @staticmethod
    def update(session, data):
        """

        """
        op_type = data.get('op_type', None)
        if op_type in ['modify', 'insert_row', 'insert_column']:
            table_roi_id = data.get('id')
            table_index = data.get('TableIndex', None)
            properties_maker = PropertiesMaker()
            properties_maker.update_keyvalueset_db(
                session, data, table_roi_id, table_index)
            session.commit()

    @staticmethod
    def delete(session, data):
        """

        """
        table_index = data.get('TableIndex', None)
        table_roi_id = data.get('id', None)
        if not table_index or not table_roi_id:
            raise MissingParamException('table_index or table_roi_id')
        obj = session.query(IqvkeyvaluesetDb).filter(and_(IqvkeyvaluesetDb.doc_id == data.get(
            'doc_id'), IqvkeyvaluesetDb.key == 'TableIndex')).all()
        id_list = list()
        for row in obj:
            table_index_value = int(((row.value).split("."))[0])
            if table_index_value >= int(table_index):
                id_list.append([row.id, table_index_value - 1])
        for i in id_list:
            obj = session.query(IqvkeyvaluesetDb).filter(
                IqvkeyvaluesetDb.id == i[0]).update({IqvkeyvaluesetDb.value: i[1]})
