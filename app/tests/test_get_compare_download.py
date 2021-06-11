import pytest
from app.api.endpoints import document_compare
from app.db.session import SessionLocal
from fastapi import HTTPException

db = SessionLocal()


@pytest.mark.parametrize("id1, id2, flag",[
("23518cb7-a09a-4de5-9a7a-5cf71977c867", "85cc67a2-1b16-4b11-b593-86906931942f", 1),
("1", "2", 0),
("","",0)
])

def test_get_compare(id1, id2, flag):
    try:
        follow_response = document_compare.get_compare_doc(db, id1 = id1, id2 = id2)
        if flag:
            assert follow_response != None
        else:
            assert follow_response == None
    except Exception as ex:
        assert flag == 0 and type(ex) == HTTPException and ex.status_code == 404
