#!/bin/bash

# Source the .env file
if [ -f ../.env ]; then
  echo ".env found"
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found"
  exit 1
fi

# Now you can use the variables from the .env file
echo "Database URL: $SERVICE_PRINCIPAL"

# Your script logic here
# For example, connecting to a database using these variables