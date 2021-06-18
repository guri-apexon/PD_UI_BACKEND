import logging

import concurrent.futures
from app import schemas
from app.utilities.config import settings
from app.utilities.elastic_utilities import update_elastic
from app.models.pd_protocol_data import PD_Protocol_Data
import json
import pandas as pd
import re
from app.crud.qc_config import summary_es_key_list
from http import HTTPStatus

logger = logging.getLogger(settings.LOGGER_NAME)

def get_qc_data(aidocid, db):
    protocol_data = db.query(PD_Protocol_Data.id,
                               PD_Protocol_Data.iqvdataSummary,
                               PD_Protocol_Data.iqvdataToc).filter(PD_Protocol_Data.id == aidocid).first()
    return protocol_data

def clean_html(table_dict):
    try:
        if type(table_dict) == dict:
            html_text = ' '.join([table_dict.get('TableName', ''), table_dict.get('Table', '')])
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', html_text)
            cleanr = re.compile('\n')
            cleantext = re.sub(cleanr, '', cleantext)
            return ' '.join(cleantext.split())
        else:
            return table_dict
    except Exception as e:
        logger.error("Exception in clean_html = {}".format(e))

def qc_update_elastic(aidocid: str, db):
    try:
        protocol_data = get_qc_data(aidocid, db)
        if protocol_data:
            summary_data = json.loads(json.loads(protocol_data.iqvdataSummary))['data']
            summary_data = {data[0]:data[1] for data in summary_data}

            es_dict = {value: summary_data.get(key, '') for key, value in summary_es_key_list.items()}

            toc_data = json.loads(json.loads(protocol_data.iqvdataToc))['data']

            toc_data_df = pd.DataFrame([(i[1], i[2], i[3]) for i in toc_data])
            toc_data_df.columns = ['CPT_section', 'type', 'content']
            toc_data_df['content'] = toc_data_df[['type', 'content']].apply(lambda x: clean_html(x['content']) if x['type'] == 'table' else x['content'], axis=1)

            toc_data_df = toc_data_df.groupby('CPT_section')['content'].apply(list).reset_index()
            toc_data_df['content'] = toc_data_df['content'].apply(lambda x: ' '.join(x) if type(x) == list else x) # Need to change this after handling table
            toc_data_df = {data['CPT_section']:data['content'] for data in toc_data_df.to_dict(orient = 'records')}
            es_dict.update(toc_data_df)
            es_dict['QC_Flag'] = True

            es_res = update_elastic({'doc':es_dict}, aidocid)
            res = dict()
            if es_res:
                res['ResponseCode'] = HTTPStatus.OK
                res['Message'] = 'Success'
            else:
                res['ResponseCode'] = HTTPStatus.FORBIDDEN
                res['Message'] = 'Error occurred while updating Elastic Search.'
        else:
            logger.info("Entry for {} not found in PD_Protocol_QCData table".format(aidocid))
            res = dict()
            res['ResponseCode'] = HTTPStatus.NO_CONTENT
            res['Message'] = 'Entry for {} not found in db to update Elastic search.'.format(aidocid)

    except Exception as ex:
        logger.error("Exception Inside qc_update_elastic: {}".format(ex))
        res = dict()
        res['ResponseCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        res['Message'] = str(ex)

    return res
