import pandas as pd
import re
import json


def get_jsonb_datastructure(df, doc_unique_id):
    tmp = 1
    df['sec_no'] = df[['type', 'content']].apply(lambda s: re.findall("^\d+[.\d+]*", s['content']) if s['type'] == 'header' else None, axis=1)
    df['sec_no_lst'] = df['sec_no'].apply(lambda x: tuple(s for s in x[0].split('.') if s) if x else x)

    df['table'] = df[['type', 'content']].apply(lambda s: re.findall("Table\s*\d+", s['content']) if s['type'] == 'header' else None, axis=1)
    df['section'] = None

    df['section_no'] = df['file_section_num'].apply(lambda x: x if x == x and not any(True for i in ['table', 'figure'] if i in x.lower()) else None)
    df['table'] = df[['file_section_num', 'table']].apply(lambda x: [x['file_section_num']] if (not x['table']) and x['file_section_num'] == x['file_section_num'] and 'table' in x['file_section_num'].lower() else x['table'], axis=1)


    unmapped_header_cnt = 1
    unmapped_header = 'unmapped_section_no_{}'
    cur_sec = [unmapped_header.format(unmapped_header_cnt)]
    df_dict = df.to_dict(orient='records')
    table_no = None
    table_flag = False

    for record in df_dict:
        if cur_sec:
            if record['sec_no'] and record['sec_no'] != cur_sec:
                cur_sec = record['sec_no']
            elif record['sec_no'] is not None and not any(re.search("{}\s*\d+".format(s), record['content'].lower()) for s in ['table', 'figure']):
                unmapped_header_cnt += 1
                cur_sec = [unmapped_header.format(unmapped_header_cnt)]

            if record['table'] or record['type'] == 'table':
                # print('3rd', cur_sec)
                if record['table']:
                    table_no = record['table'][0]
                table_flag = True
            record['section'] = cur_sec + [table_no] if table_flag and table_no else cur_sec
            table_flag = False

    unmapped_header_cnt = 1
    unmapped_header = 'unmapped_section_no_{}'
    cur_sec = [unmapped_header.format(unmapped_header_cnt)]

    table_no = None
    table_flag = False

    for record in df_dict:
        if cur_sec:
            if record['section_no'] and record['section_no'] != cur_sec:
                cur_sec = [record['section_no']]
            # elif record['section_no'] is not None and not any(re.search("{}\s*\d+".format(s), str(record['content']).lower()) for s in ['table', 'figure']):
            elif record['section_no'] not in [None, ''] and not any(re.search("{}\s*\d+".format(s), str(record['content']).lower()) for s in ['table', 'figure']):
                unmapped_header_cnt += 1
                cur_sec = [unmapped_header.format(unmapped_header_cnt)]

            if record['table'] or record['type'] == 'table':
                if record['table']:
                    table_no = record['table'][0]
                table_flag = True
            record['section_no'] = cur_sec + [table_no] if table_flag and table_no else cur_sec
            table_flag = False

    section_num = 'sec_num_count_{}'
    for record in df_dict:
        if (not record['section_no'][0].startswith('unmapped_section_no')) and record['section'][0].startswith('unmapped_section_no'):
            record['section_no'] = record['section_no'][:]
            record['section_no'].append(record['section'][0])
        if record['section_no'][0][0].isnumeric():
            record['sec_no_lst'] = [i for i in record['section_no'][0].split('.') if i] + record['section_no'][1:]
        else:
            record['sec_no_lst'] = record['section_no'][:]

        for idx, sec in enumerate(record['sec_no_lst']):
            record[section_num.format(idx)] = sec

    df_sec = pd.DataFrame(df_dict)

    columns = [col for col in df_sec.columns if col.startswith('sec_num_count_')]
    columns = [columns[0:idx + 1] for idx in range(len(columns))]

    grp_by_list = list()

    for idx in range(len(columns)):
        df_tmp = df_sec[~ df_sec[columns[idx][-1]].isna()].reset_index(drop=True)
        df_tmp['grp_by_col'] = df_tmp[columns[idx]].apply(lambda x: tuple((x[col] for col in columns[idx])), axis=1)
        grp_by_list.append(df_tmp.groupby('grp_by_col', sort=False)['seq_num'].apply(list).to_dict())

    dict_ = {i: {'seq_num': j[i], 'header_num': i,
                 'section_unique_id': j[i][0],
                 'doc_unique_id': doc_unique_id}
             for j in grp_by_list for i in j}

    keys_list = list(dict_.keys())

    for key in keys_list:
        p_k = key[:len(key) - 1]
        if p_k in dict_:
            if dict_[key]['seq_num'][0] != dict_[p_k]['seq_num'][0]:
                key_list = dict_[key]['seq_num']
                p_key_list = dict_[p_k]['seq_num']
                p_key_list = [num for num in p_key_list if num not in key_list]
                dict_[p_k]['seq_num'] = p_key_list

                dict_[p_k]['child_ids'] = dict_[p_k].get('child_ids', []) + [key_list[0]]
                dict_[p_k]['child_header_num'] = dict_[p_k].get('child_header_num', []) + [key]

                dict_[key]['parent_section_ids'] = dict_[key].get('parent_section_ids', []) + [p_key_list[0]]
                dict_[key]['parent_header_num'] = dict_[key].get('parent_header_num', []) + [p_k]
            else:
                del dict_[key]

    for key in dict_:
        dict_[key]['seq_num'] = dict_[key]['seq_num'][1:]

    dict_content = {row[1]: {'content': row[0] if row[0] == row[0] else None,
                             'segment_unique_id': row[1],
                             'doc_unique_id': doc_unique_id}
                    for row in df[['content', 'seq_num']].values}

    for key in dict_:
        dict_[key]['header_name'] = dict_content[dict_[key]['section_unique_id']]['content']

        dict_[key]['header_num'] = '.'.join(dict_[key]['header_num'])

        if 'child_header_num' in dict_[key]:
            dict_[key]['child_header_num'] = ['.'.join(i) for i in dict_[key]['child_header_num']]

        for num in dict_[key]['seq_num']:
            dict_content[num]['section_unique_id'] = dict_[key]['section_unique_id']

    hrd_section_unique_id = [v['section_unique_id'] for k, v in dict_.items()]

    # section and sub section contents
    section_content_record = [(idx + 1, val) for idx, val in enumerate(dict_content.values()) if val['segment_unique_id'] not in hrd_section_unique_id]

    # Header sections
    header_record = [(idx + 1, val) for idx, val in enumerate((dict_.values()))]

    return (header_record, section_content_record)