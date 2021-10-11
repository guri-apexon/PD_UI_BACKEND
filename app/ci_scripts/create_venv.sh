${PYTHON_PATH}/python -m venv ${CI_BUILDS_DIR}/${RUNNING_ENV}

${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --upgrade -r ${GIT_CLONE_PATH}/requirements.txt

${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --extra-index-url https://nexusrnds-test.quintiles.com/repository/gxp_pypi/simple python-ldap
# Static libraries
${CI_BUILDS_DIR}/${RUNNING_ENV}/Scripts/pip install --upgrade flake8 pep8-naming pytest-cov setuptools
