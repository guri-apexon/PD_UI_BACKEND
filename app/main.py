from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints.api import api_router
from app.utilities.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"/openapi.json")

# Set all CORS enabled origins
# Can be precisely customised
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(api_router, prefix=settings.API)
