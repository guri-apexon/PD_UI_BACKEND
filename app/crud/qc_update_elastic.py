import logging

import concurrent.futures
from app import schemas
from app.utilities.config import settings
from app.utilities.elastic_utilities import update_elastic
from app.models.pd_protocol_qcdata import PD_Protocol_QCData
import json
import pandas as pd
import re
from app.crud.qc_config import summary_es_key_list

logger = logging.getLogger(settings.LOGGER_NAME)

def get_qc_data(aidocid, db):
    protocol_qcdata = db.query(PD_Protocol_QCData.id,
                               PD_Protocol_QCData.iqvdataSummary,
                               PD_Protocol_QCData.iqvdataToc).filter(PD_Protocol_QCData.id == aidocid).all()
    return protocol_qcdata

def clean_html(html_text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', html_text)
    cleanr = re.compile('\n')
    cleantext = re.sub(cleanr, '', cleantext)
    return ' '.join(cleantext.split())

def qc_update_elastic(aidocid: str, db):
    try:
        protocol_qcdata = get_qc_data(aidocid, db)
        if protocol_qcdata:
            summary_data = json.loads(json.loads(protocol_qcdata[0].iqvdataSummary))['data']
            summary_data = {data[0]:data[1] for data in summary_data}

            es_dict = {value: summary_data.get(key, '') for key, value in summary_es_key_list.items()}

            toc_data = json.loads(json.loads(protocol_qcdata[0].iqvdataToc))['data']

            toc_data_df = pd.DataFrame([(i[1], i[2], i[3]) for i in toc_data])
            toc_data_df.columns = ['CPT_section', 'type', 'content']
            toc_data_df['content'] = toc_data_df[['type', 'content']].apply(lambda x: clean_html(' '.join([x['content']['TableName'], x['content']['Table']])) if x['type'] == 'table' else x['content'], axis=1)
            toc_data_df = toc_data_df.groupby('CPT_section')['content'].apply(list).reset_index()
            toc_data_df['content'] = toc_data_df['content'].apply(lambda x: ' '.join(x) if type(x) == list else x) # Need to change this after handling table
            toc_data_df = {data['CPT_section']:data['content'] for data in toc_data_df.to_dict(orient = 'records')}
            es_dict.update(toc_data_df)

            update_elastic({'doc':es_dict}, aidocid)
            res = dict()
            res['ResponseCode'] = 200
            res['Message'] = 'Success'
        else:
            logger.info("Entry for {} not found in PD_Protocol_QCData table".format(aidocid))
            res = dict()
            res['ResponseCode'] = 200
            res['Message'] = 'Entry for {} not found in db to update Elastic search.'.format(aidocid)

    except Exception as e:
        logger.error("Exception = ", e)

        res = dict()
        res['ResponseCode'] = 500
        res['Message'] = 'Internal Server Error'

    return res
