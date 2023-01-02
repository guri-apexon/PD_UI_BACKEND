from typing import Optional
import pandas as pd
import numpy as np
import psycopg2
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_headers
from app.db.session import psqlengine
from fastapi.responses import JSONResponse
from fastapi import status,Response
from app.utilities.config import settings
import logging
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id
from etmfa_core.aidoc.IQVDocumentFunctions import IQVDocument

logger = logging.getLogger(settings.LOGGER_NAME)

def get_document_links(aidoc_id: str, link_levels: int, toc: int):
    """
    Get document links for the requestd aidoc_id with link_level

    :param aidoc_id: document id 
    :param link_level: link level of document
    :param toc: table of content list with parent child relationship
    :returns: list of sections/headers
    """

    connection = None
    if abs(toc) > 1:
        return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT,content={"message":"TOC required 0 or 1"})
    try:
        connection = psqlengine.raw_connection()
        iqv_doc_headers = GetIQVDocumentFromDB_headers(connection, aidoc_id)
        if iqv_doc_headers == None:
            return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT,content={"message":"Docid does not exists"})
    except (Exception, psycopg2.Error) as error:
        logger.exception(f"Failed to get connection to postgresql : {error}")
    finally:
        if connection:
            connection.close()

    try:
        df = pd.DataFrame(
            [link.__dict__ for link in iqv_doc_headers.DocumentLinks])
        df = df[(df['LinkType'] == 'toc') & (df['LinkLevel'] <= link_levels) & (df['LinkText'] != "blank_header")]
        df = df.reset_index(drop=True)
        df['link_id'] = df.apply(lambda x: x['link_id'] if x['LinkLevel']
                                == 1 else x['link_id_level{}'.format(x['LinkLevel'])], axis=1)
        df = df[['doc_id', 'group_type', 'link_id', 'LinkLevel',
                'LinkPage', 'LinkPrefix', 'LinkText', 'LinkType']]
        df = df.rename(columns={'LinkText': 'source_file_section',
                                'LinkPage': 'page', 'LinkPrefix': 'sec_id'})
        df['page'] = df['page'] + 1
        df = df.sort_values(by='page').reset_index(drop=True)
        df['qc_change_type'] = ''
        df['sequence'] = [i for i in range(df.shape[0])]
        df['section_locked'] = False
        df['audit_info'] = [{'last_reviewed_date': '', 'last_reviewed_by': '',
                            'total_no_review': ''} for _ in range(df.shape[0])]

        headers = df.to_dict(orient='records')
        if toc == 0:
            # if toc not 1 then it will return without parent child relationship
            return headers
        elif toc == 1:
            # if toc is 1 returns sections/headers data with parent child relationship
            toc_headers = []  
            doc_headers = []
            for i in headers:              
                linklevel = i.get('LinkLevel')
                section_id = i.get('sec_id')          
                if linklevel == 1:
                    toc_headers.append(i)
                elif linklevel in (2,3,4,5,6):
                    toc_headers.append(i)                   
                    section_id_num = section_id.replace(".", "")
                    if section_id_num.isnumeric():
                        section_id_split = section_id.split(".")
                        section_id_join = ".".join(section_id_split[:-1]) + ("." if section_id_split.pop()=="" else "")
                        filtered_header = filter(lambda x: x.get('sec_id') == section_id_join, headers)
                        for item in filtered_header:
                            if item in headers:
                                index = headers.index(item)
                                if headers[index].get('childlevel'):
                                    headers[index].get('childlevel').append(i)
                                else:                            
                                    headers[index]['childlevel']= [i] 
                    elif isinstance(section_id, str):
                        doc_headers.append(i)

            # filtering headers by linklevel 1 in parent level            
            toc_headers = list(filter(lambda x:x['LinkLevel']==1, headers))
            # sorting child level  based on sec_id key
            for header in doc_headers:
                toc_headers.append(header)
            childlevel_headers = []
            for header in toc_headers:
                if len(header) != 12:
                    parent_header = (header["childlevel"])
                    sorted_parent_header = sorted(parent_header, key = lambda x:x['sec_id'])
                    for parent_header_item in sorted_parent_header:
                        if len(parent_header_item) != 12:
                            sorted_parent_header_child = sorted((parent_header_item["childlevel"]), key = lambda x:x['sec_id'])
                            for sorted_parent_header_item in sorted_parent_header_child:
                                if len(sorted_parent_header_item) != 12:
                                    sorted_parent_header_child_1 = sorted((sorted_parent_header_item["childlevel"]), key = lambda x:x['sec_id'])
                                    sorted_parent_header_item['childlevel'] = sorted_parent_header_child_1
                            parent_header_item['childlevel'] = sorted_parent_header_child
                    header['childlevel'] = sorted_parent_header
                childlevel_headers.append(header)
            return childlevel_headers

    except Exception as error:
        logger.exception(f"doc id {aidoc_id} having issue : {error}")
        return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT,content={"message":"Docid having some issue"})


def get_header_list(aidoc_id: str, link_level: int, link_id: int) -> Optional[IQVDocument]:
    """
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: link id of document 
    :returns: requested section/header data
    """

    try:
        connection = psqlengine.raw_connection()
        iqv_document = GetIQVDocumentFromDB_with_doc_id(
                connection, aidoc_id, link_level=link_level, link_id=link_id)
        return iqv_document
    except (Exception, psycopg2.Error) as error:
        logger.exception(f"Failed to get connection to postgresql : {error}, {aidoc_id}")
        return None
    finally:
        if connection:
            connection.close()