import psycopg2
from app.utilities.config import settings
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id, GetIQVDocumentFromDB_headers
import pandas as pd

def get_document_links(aidoc_id: str, link_levels: int):
    connection = None

    try:
        # Getting PostgreSQL Connection
        connection = psycopg2.connect(database=settings.PostgreSQL_DATABASE,
                                      user=settings.PostgreSQL_USER,
                                      password=settings.PostgreSQL_PASSWORD,
                                      host=settings.PostgreSQL_HOST,
                                      port= settings.PostgreSQL_PORT)

        iqv_doc_headers = GetIQVDocumentFromDB_headers(connection, aidoc_id)

    except (Exception, psycopg2.Error) as error:
        print("Failed to get connection to PostgreSQL, error:", error)

    finally:
        # closing database connection.
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")


    # iqv_doc_headers = GetIQVDocumentFromDB_headers(connection, aidoc_id)

    # link_levels = 1
    df = pd.DataFrame([link.__dict__ for link in iqv_doc_headers.DocumentLinks])
    df = df[(df['LinkType'] == 'toc') & (df['LinkLevel'] <= link_levels)]
    df = df.reset_index(drop = True)
    df['link_id'] = df.apply(lambda x: x['link_id'] if x['LinkLevel'] == 1 else x['link_id_level{}'.format(x['LinkLevel'])], axis=1)
    df = df[['doc_id', 'group_type', 'link_id', 'LinkLevel', 'LinkPage', 'LinkPrefix', 'LinkText', 'LinkType']]
    df = df.rename(columns = {'LinkText': 'source_file_section', 'LinkPage': 'page', 'LinkPrefix': 'sec_id'})
    df['page'] = df['page'] + 1
    df = df.sort_values(by='page').reset_index(drop=True)
    df['qc_change_type'] = ''
    df['sequence'] = [i for i in range(df.shape[0])]
    df['section_locked'] = False
    df['audit_info'] = [{'last_reviewed_date': '', 'last_reviewed_by': '', 'total_no_review': '' } for _ in range(df.shape[0])]


    headers = df.to_dict(orient='records')

    return headers