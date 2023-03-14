import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.utilities.elastic_utilities import get_elastic_doc_by_id, update_elastic, delete_elastic_doc_by_id
from http import HTTPStatus



client = TestClient(app)

@pytest.mark.parametrize(
    ["aidocid", "insert_flag", "comment"],
    [
        ('6088b345-5061-4b9c-82c9-db8a722bb5fe', True, "Successful insertion in ES"),
        ('6088b345-5061-4b9c-82c9-db8a722bb5', False, "Document not in DB. ES indexing failed")

     ])
def test_query_elastic(new_token_on_headers, aidocid, insert_flag, comment):

    res = client.post("/api/elastic_ingest/",
                     params={"aidoc_id": aidocid},
                     headers=new_token_on_headers)

    if res.status_code == HTTPStatus.OK:
        res_json = res.json()
        if insert_flag and res_json['success'] == True: # Case where document is inserted into ES
            response = get_elastic_doc_by_id(aidocid)
            assert response['found'] and response['_source']['AiDocId'] == aidocid
            delete_elastic_doc_by_id(aidocid)
        elif not insert_flag and res_json['success'] == False: # Case where document is not inserted into ES as document is not present in DB
            assert True
    else:
        assert False
