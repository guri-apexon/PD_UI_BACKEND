import json
from .model.__base__ import MissingParamException


def get_prop_dict(column: dict):
    """
    get table's sub dict structure 
    """
    prop_dict = {
        "content": column['value'],
        "roi_id": {
            "table_roi_id": "",
            "row_roi_id": "",
            "column_roi_id": "",
            "datacell_roi_id": column["cell_id"]
        }
    }
    return prop_dict


def get_add_wrapped_table_props(wrapped_table_props: dict, table_props: list):
    """
    get add table properties
    """
    op_params = list()
    for column_data in table_props:
        row_props = dict()
        for column in column_data['columns']:
            row_props[str(column['col_indx'])] = get_prop_dict(column)
        op_params.append({"row_roi_id": "",
                          "row_idx": str(column_data.get('row_indx')),
                          "row_props": row_props})
    wrapped_table_props.append({"op_type": "create_table",
                                "op_params": op_params})
    return wrapped_table_props


def get_column_props(column_props: dict, wrapped_table_props: dict):
    """
    get table's column properties
    """
    for ope_type, value in column_props.items():
        if len(value) != 0:
            if ope_type == 'modify':
                op_params = list()
                row_index_list = set()
                for prop in value:
                    for row_indx, row_prop in prop.items():
                        if len(op_params) != 0 and row_indx in row_index_list:
                            for para in op_params:
                                if para['row_idx'] == row_indx:
                                    (para["row_props"]).update(row_prop)
                        else:
                            op_params.append({"row_roi_id": "",
                                              "row_idx": row_indx,
                                              "row_props": row_prop})
                            row_index_list.add(row_indx)
                wrapped_table_props.append({"op_type": ope_type,
                                            "op_params": op_params})

            if ope_type in ['insert_column', 'delete_column']:
                column_dict = dict()
                for prop in value:
                    for row_indx, row_prop in prop.items():
                        for column_idx in row_prop.keys():
                            if column_dict.get(column_idx):
                                column_dict[column_idx].update(prop)
                            else:
                                column_dict[column_idx] = prop

                for prop in column_dict.values():
                    op_params = list()
                    for row_indx, row_prop in prop.items():
                        op_params.append({"row_roi_id": "",
                                          "row_idx": row_indx,
                                          "row_props": row_prop})
                    wrapped_table_props.append({"op_type": ope_type,
                                                "op_params": op_params})
    return wrapped_table_props


def get_sorted_wrapped_table_props(wrapped_table_props: dict):
    """
    get sorted table properties based on priority opertion list
    """
    sorted_wrapped_table_props = list()
    op_priority = ['delete_row', 'delete_column',
                   'modify', 'insert_column', 'insert_row']
    for op in op_priority:
        for table_props in wrapped_table_props:
            if table_props['op_type'] == op and table_props not in sorted_wrapped_table_props:
                sorted_wrapped_table_props.append(table_props)
    return sorted_wrapped_table_props


def get_modify_wrapped_table_props(wrapped_table_props: dict, table_props: list):
    """
    get modify table properties 
    """
    column_props = {'modify': [], 'insert_column': [], 'delete_column': []}
    for column_data in table_props:
        op_params = list()
        row_props = dict()
        new_op_type = ""
        row_idx = str(column_data.get('row_indx'))
        op_type = column_data.get('op_type')
        if op_type in ['add', 'delete']:
            if op_type == 'add':
                new_op_type = 'insert_row'
                for column in column_data['columns']:
                    row_props[str(column['col_indx'])] = get_prop_dict(column)
            else:
                new_op_type = 'delete_row'

        elif op_type == 'modify':
            for column in column_data['columns']:
                new_op_type = None
                if column.get('op_type') in ['add', 'delete']:
                    if column.get('op_type') == 'add':
                        new_op_type = 'insert_column'
                    else:
                        new_op_type = 'delete_column'
                    column_props[new_op_type].append(
                        {row_idx: {str(column['col_indx']): get_prop_dict(column)}})

                elif column.get('op_type') == 'modify':
                    column_props['modify'].append(
                        {row_idx: {str(column['col_indx']): get_prop_dict(column)}})

        else:
            raise MissingParamException(" or invalid operation type ")

        if len(row_props) != 0 or new_op_type == 'delete_row':
            op_params.append({"row_roi_id": "",
                              "row_idx": row_idx,
                              "row_props": row_props})
            wrapped_table_props.append({"op_type": new_op_type,
                                        "op_params": op_params})

    wrapped_table_props = get_column_props(column_props, wrapped_table_props)
    sorted_wrapped_table_props = get_sorted_wrapped_table_props(
        wrapped_table_props)

    return sorted_wrapped_table_props


def get_table_props(action_type: str, data: dict):
    """
    get table properties as per action type
    """
    table_props = None
    wrapped_table_props = list()
    if action_type != 'delete':
        if not data.get('content', None):
            raise MissingParamException('content')
        content = data['content']
        if not content.get('TableProperties', None):
            raise MissingParamException('.TableProperties.')
        table_props = content['TableProperties']
        if isinstance(table_props, str):
            table_props = json.loads(table_props)
        if action_type == 'add':
            wrapped_table_props = get_add_wrapped_table_props(
                wrapped_table_props, table_props)
        if action_type == 'modify':
            wrapped_table_props = get_modify_wrapped_table_props(
                wrapped_table_props, table_props)

    if action_type == 'delete':
        wrapped_table_props.append({"op_type": "delete_table",
                                    "op_params": ""})
    return wrapped_table_props
