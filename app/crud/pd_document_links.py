from email import message
import pandas as pd
import numpy as np
import psycopg2
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id, GetIQVDocumentFromDB_headers
from app.db.session import psqlengine
from fastapi.responses import JSONResponse
from fastapi import status

def get_document_links(aidoc_id: str, link_levels: int, toc: int):
    connection = None
    if abs(toc) > 1:
        return JSONResponse(content={"message":"TOC required 0 or 1","status":status.HTTP_204_NO_CONTENT})
    try:
        connection = psqlengine.raw_connection()
        iqv_doc_headers = GetIQVDocumentFromDB_headers(connection, aidoc_id)
        if iqv_doc_headers == None:
            return JSONResponse(content={"message":"Docid does not exists","status":status.HTTP_204_NO_CONTENT})
    except (Exception, psycopg2.Error) as error:
        print("Failed to get connection to PostgreSQL, error:", error)
    finally:
        if connection:
            connection.close()

    try:
        df = pd.DataFrame(
            [link.__dict__ for link in iqv_doc_headers.DocumentLinks])
        df = df[(df['LinkType'] == 'toc') & (df['LinkLevel'] <= link_levels)]
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
            return headers
        elif toc == 1:
            array_test = []

            for i in headers:
                linkelevel = i.get('LinkLevel')
                y = i.get('sec_id')
                if linkelevel == 1:
                    array_test.append(i)
                else:
                    y_int = y.replace(".", "")
                    if y_int.isnumeric():
                        y_split = y.split(".")
                        y_slice = y_split[:-2]
                        y_join = ".".join(y_slice) + "."
                        filtered_object = filter(
                            lambda x: x.get('sec_id') == y_join, headers)
                        for x in filtered_object:
                            if x in array_test:
                                index = array_test.index(x)
                                if array_test[index].get('childlevel'):
                                    array_test[index].get('childlevel').append(i)
                                else:

                                    array_test[index]['childlevel'] = [i]

            return array_test
    except Exception as error:
        print("error",error)