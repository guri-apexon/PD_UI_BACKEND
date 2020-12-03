# Protocol Digitalization Back End

Backend API service for Protocol Digitalization.

All the nested JSON schema is created  using `pydantic`. It is a (de)serializing library.


### Pre Requisites

#### Database:
* SQL Server Database
    * Added a [DB script](localsetup/sample_ts_monitoring.sql) with schema and some sample data to setup DB
    



##### Helpful Links:
* Poetry Pycharm Plugin - https://koxudaxi.github.io/poetry-pycharm-plugin/
* Installation with `poetry.lock` - https://python-poetry.org/docs/basic-usage/#installing-with-poetrylock

#### Configuration File
Project is using `.env` file to handle configurations <br>

The current configuration file is simple with only one key, it is `SQLALCHEMY_DATABASE_URI` which is a DB connection string
The `.env` file should be set in local environment variable of project.

Required values for `.env` file are in [.env](.env)

##### Helpful Links:
* EnvFile Plugin for Pycharm - https://plugins.jetbrains.com/plugin/7861-envfile
* EnvFile Plugin setup for Pycharm - https://stackoverflow.com/a/42708476

#### Running locally
To run the service locally, make sure all dependencies are correctly installed and environment file is having required values.

Use the following command on the activate poetry environment

```shell script
uvicorn app.main:app
```
You would be able to access Swagger UI on `http://localhost:8000/docs`

**8000** is default port in Uvicorn

#### Authentication details
username: admin
password: admin

---
### Other helpful links:
* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [Pydantic Doc](https://pydantic-docs.helpmanual.io/)

