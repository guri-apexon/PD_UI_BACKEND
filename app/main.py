import click
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints.api import api_router
from app.backend_pre_start import main
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


@app.on_event("startup")
def startup_events():
    main()


@app.on_event("shutdown")
def shutdown_event():
    # Note: Can add closing DB connections and checking message queues
    click.echo('Exiting pd-backend-ui Service...')


@click.group()
def cli():
    """Entry point for Extraction-Microservice functions."""
    pass


@cli.command()
def run():
    """
    Start the FastAPI Text Extraction Microservice for extraction similar segments
    """
    uvicorn.run(app, host='0.0.0.0', port=settings.APPLICATION_PORT)


@cli.command()
def backend_pre_start():
    """
    Checks the status of prerequisite services
    """
    from app.backend_pre_start import main
    main()


if __name__ == '__main__':
    cli()
