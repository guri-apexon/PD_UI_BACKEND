from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/healthcheck", response_class=PlainTextResponse)
def healthcheck():
    return "ACCEPTING_REQUEST"
