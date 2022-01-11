ROLLBACK_OPT=$1

if [ "$ROLLBACK_OPT" == "package" ]; then
  INSTALL_PACKAGE="$PACKAGE==$PACKAGE_VERSION"
else
  echo "Unknown deployment option: $ROLLBACK_OPT"
  exit 1
fi

## Stop running service
SERVICE_STATE=$($NSSM_PATH status "$SERVICE_NAME" | tr -d '\0')
echo "Service state: $SERVICE_STATE"
echo "Stopping service..."
$NSSM_PATH stop "$SERVICE_NAME"


## Re-install the package
echo "Re-installing service package..."
pip uninstall "$PACKAGE" -y && pip uninstall etmfa-core -y

REGISTRY_PYPI_URL=$REGISTRY_PYPI_URL REGISTRY_SERVER=$REGISTRY_SERVER

echo "REGISTRY_PYPI_URL is $REGISTRY_PYPI_URL"
echo "REGISTRY_SERVER is $REGISTRY_SERVER"
echo "INSTALL_PACKAGE is $INSTALL_PACKAGE"

pip install -e . --no-cache-dir --upgrade --extra-index-url "$REGISTRY_PYPI_URL/simple" --trusted-host "$REGISTRY_SERVER" "$INSTALL_PACKAGE"
pip install -e . --no-cache-dir --upgrade $INSTALL_PACKAGE

pip install --upgrade --extra-index-url "$REGISTRY_PYPI_URL/simple" etmfa-core
## Start service
echo "Starting service..."
$NSSM_PATH start "$SERVICE_NAME"

## Check if running
for i in {1..10}; do
  SERVICE_STATE=$($NSSM_PATH status "$SERVICE_NAME" | tr -d '\0')
  echo "Service state: $SERVICE_STATE (retry: $i)"

  if [ "$SERVICE_STATE" == "SERVICE_RUNNING" ]; then
    # Wait for service to start and verify the endpoints are accessible
    echo "Waiting for service to start and be accessible at '$VERIFICATION_URL'..."
    sleep 60
    for j in {1..10}; do
      echo "Verifying service reachability (retry: $j)"
      APP_RESPONSE=$(curl --insecure -L "$VERIFICATION_URL")
      if [ "$APP_RESPONSE" == "F5-UP" ]; then
        echo "Received success health status: $APP_RESPONSE"
        echo "Successfully Rollback to : $PACKAGE==$PACKAGE_VERSION"
        exit 0
      else
        echo "Receiving health status: $APP_RESPONSE"
        sleep 15
      fi
    done

    echo "ERROR: Unable to verify service reachability"
    exit 1
  else
    sleep 5
  fi
done

echo "ERROR: Unable to start service $SERVICE_NAME"
exit 1