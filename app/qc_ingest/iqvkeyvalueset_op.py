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

    def update_table_cell_properties(self, row, table_index, table_name, prev_dict, session, link_roi, link_level):
        """

        """
        table_cell_properties_list = list()
        for col in row:
            header = 0.0
            if col['row_idx'] == 0:
                header = 1.0
            table_cell_properties_dict = {'TableIndex': table_index, 'RowIndex': float(int(table_index)*1000+col['row_idx']+1), 'IsHeaderCell': header,
                                          'ColIndex': [col['col_idx']+1], 'FootNoteLink': '', 'TableName': table_name, 'FullText': col['val'], 'LinkROI': link_roi, 'LinkLevel': link_level}
            para_properties_dict = {
                'TableIndex': table_index, 'LinkText': table_name, 'LinkROI': link_roi, 'LinkLevel': link_level}
            col_id = col['datacell_roi_id']
            doc_table_helper = DocTableHelper()
            child_col_id = doc_table_helper._get_child_cell_roi_id(
                session, col_id)
            for property_dict,  hierarchy in [(table_cell_properties_dict, 'table'), (para_properties_dict, 'paragraph')]:
                for key, val in property_dict.items():
                    obj = session.query(IqvkeyvaluesetDb).filter(and_(
                        IqvkeyvaluesetDb.parent_id == child_col_id, IqvkeyvaluesetDb.key == key, IqvkeyvaluesetDb.hierarchy == hierarchy)).first()
                    if not obj:
                        keyvalueset = self.get_keyvalueset(
                            key, val, prev_dict, child_col_id, hierarchy)
                        table_cell_properties_list.append(keyvalueset)
                    else:
                        obj.value = val
                        session.add(obj)
        return table_cell_properties_list

    def update_footnote_properties(self, footnote, table_index, prev_dict, session, link_roi, link_level, table_roi_id, indx):
        """

        """
        footnote_properties_list = list()
        attachment_id = footnote['AttachmentId']
        footnote_text = footnote['Text']
        splited_text = footnote_text.split(': ')
        footnote = None
        if footnote_text != splited_text[0]:
            footnote = splited_text[0]
        else:
            splited_text = footnote_text.split('. ')
            if footnote_text != splited_text[0]:
                footnote = splited_text[0]

        footnote_properties_dict = {'TableIndex': table_index, 'AttachmentId': attachment_id,
                                    'IsFootnote': '', 'FootnoteText': footnote_text, 'LinkROI': link_roi, 'LinkLevel': link_level}
        table_footnote_properties_dict = {'Footnote_'+str(indx): footnote,
                                'AttachmentId_'+str(indx): str({'TableId': table_roi_id, 'AttachmentIndex': float(indx), 'AttachmentId': attachment_id, 'Key': footnote, 'Text': footnote_text}),
                                 'FootnoteText_'+str(indx): footnote_text}
        for property_dict, hierarchy, parent_id in [(table_footnote_properties_dict, 'table', table_roi_id), (footnote_properties_dict, 'paragraph', attachment_id)]:
            for key, val in property_dict.items():
                obj = session.query(IqvkeyvaluesetDb).filter(and_(
                    IqvkeyvaluesetDb.parent_id == parent_id, IqvkeyvaluesetDb.key == key)).first()
                if not obj:
                    keyvalueset = self.get_keyvalueset(
                        key, val, prev_dict, parent_id, hierarchy)
                    footnote_properties_list.append(keyvalueset)
                else:
                    obj.value = val
                    session.add(obj)
        return footnote_properties_list

    def get_link_details(self, prev_dict):
        link_roi, link_level = None, None
        link_name_list = ['link_id_subsection3', 'link_id_subsection2', 'link_id_subsection1',
                          'link_id_level6', 'link_id_level5', 'link_id_level4', 'link_id_level3', 'link_id_level2', 'link_id']
        for idx, link_name in enumerate(link_name_list):
            if prev_dict.get(link_name):
                link_roi = prev_dict.get(link_name)
                link_level = len(link_name_list) - idx
        return link_roi, link_level

    def update_table_properties(self, session, table_roi_id, table_name, table_index, prev_dict, link_roi, link_level):
        """

        """
        table_properties_list = list()
        table_properties_dict = {'TableIndex': table_index, 'TableName': table_name,
                                 'LinkText': table_name, 'LinkROI': link_roi, 'LinkLevel': link_level}
        for key, val in table_properties_dict.items():
            obj = session.query(IqvkeyvaluesetDb).filter(and_(
                IqvkeyvaluesetDb.parent_id == table_roi_id, IqvkeyvaluesetDb.key == key, IqvkeyvaluesetDb.hierarchy == 'table')).first()
            if not obj:
                keyvalueset = self.get_keyvalueset(
                    key, val, prev_dict, table_roi_id, 'table')
                table_properties_list.append(keyvalueset)
            else:
                obj.value = val
                session.add(obj)
        return table_properties_list

    def update_keyvalueset_db(self, session, data, table_roi_id, table_index):
        """

        """
        doc_table_helper = DocTableHelper()
        table_name = data.get('TableName', "")
        if table_index == None or not table_roi_id:
            raise MissingParamException('table_index or table_roi_id')
        table_roi_data = session.query(DocumenttablesDb).filter(
            DocumenttablesDb.id == table_roi_id).first()
        prev_dict = schema_to_dict(table_roi_data)
        link_roi, link_level = self.get_link_details(prev_dict)
        if data.get('op_params'):
            table_properties_list = self.update_table_properties(
                session, table_roi_id, table_name, table_index, prev_dict, link_roi, link_level)
            for table_properties in table_properties_list:
                    session.add(table_properties)
            table_data = doc_table_helper.get_table(session, table_roi_id)
            for row in table_data.values():
                table_cell_properties_list = self.update_table_cell_properties(
                    row, table_index, table_name, prev_dict, session, link_roi, link_level)
                for table_cell_properties in table_cell_properties_list:
                    session.add(table_cell_properties)
        if data.get('AttachmentListProperties'):
            table_footnote_data = doc_table_helper.get_table_footnote_data(
                session, table_roi_id)
            for indx, footnote in enumerate(table_footnote_data):
                footnote_properties_list = self.update_footnote_properties(
                    footnote, table_index, prev_dict, session, link_roi, link_level, table_roi_id, indx)
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
        table_index = get_table_index(session, doc_id, table_roi_id, DocumenttablesDb)
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
        table_roi_id = data.get('table_roi_id')
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
        table_roi_id = data.get('table_roi_id', None)
        if table_index == None or not table_roi_id:
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
