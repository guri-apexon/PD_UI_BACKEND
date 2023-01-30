from app.models.pd_document_status import PD_Document_Status


def test_verify_document_model():
    doc_obj = PD_Document_Status()

    assert doc_obj.__tablename__ == 'pd_document_process'