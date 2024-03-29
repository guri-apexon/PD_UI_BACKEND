${PYTHON_PATH}/python -m venv ${CI_BUILDS_DIR}/${RUNNING_ENV}
REGISTRY_PYPI_URL=$REGISTRY_PYPI_URL REGISTRY_SERVER=$REGISTRY_SERVER
${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --upgrade -r ${GIT_CLONE_PATH}/requirements.txt --extra-index-url "$REGISTRY_PYPI_URL/simple" --trusted-host "$REGISTRY_SERVER"
${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --no-cache-dir --extra-index-url https://$REGISTRY_SERVER/repository/PD_PYPI/simple python-ldap==3.3.1
# Static libraries
${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --upgrade flake8 pep8-naming pytest-cov setuptools

