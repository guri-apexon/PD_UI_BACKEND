import psycopg2
from app.utilities.config import settings
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id, GetIQVDocumentFromDB_headers
import pandas as pd
import numpy as np
def get_document_links(aidoc_id: str, link_levels: int, toc: int):
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
    if toc == 0:
        df = pd.DataFrame([link.__dict__ for link in iqv_doc_headers.DocumentLinks])
        print("main_dataframe", df)
        df = df[(df['LinkType'] == 'toc') & (df['LinkLevel'] <= link_levels)]
        print("filtered_dataframe", df)
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
        array_test = []  


        for i in headers:
            # print("i", i)               

            linkelevel = i.get('LinkLevel')
            y = i.get('sec_id')
            # print("yyyyy", y)
            if linkelevel == 1:
                array_test.append(i)
                #print("liknlevel1", array_test)  #None
            else:
                y_int = y.replace(".", "")
                # print("section_id", y, y_int)

        
                if y_int.isnumeric():
                    y_split = y.split(".") #1.2.4 = ['1','2','4'] 
                    # print("y_split", y_split)
                    y_slice = y_split[:-2] # ['1', '2']
                    # print("y_slice", y_slice)
                    y_join = ".".join(y_slice) + "."
                    # print("joiner", y_join)
                    filtered_object = filter(lambda x: x.get('sec_id') == y_join, headers)
                    for x in filtered_object:
                        print("x",x)

                        if x in array_test:
                            index = array_test.index(x)
                            print("index", index)
                            if array_test[index].get('childlevel'):
                                array_test[index].get('childlevel').append(i)
                            else:
                                
                                array_test[index]['childlevel']= [i]
                            print("array_index", array_test[index])


                            


                        










                    
        print("array_test", array_test)
        return array_test

            



   
        