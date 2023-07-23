#!/bin/bash

# Set the yarn executable path
YARN_PATH="/var/services/homes/vaccarieli/.yarn/bin/yarn"

# Set the python executable path
PYTHON_PATH="/bin/python3"

# Run the project with yarn start and save output to log file
("$YARN_PATH" --cwd /var/services/homes/vaccarieli/ws-gonsta-api start) &

YARN_PID=$!

sleep 15

# # Execute the Python script
"$PYTHON_PATH" "/var/services/homes/vaccarieli/ws-gonsta-api/bot/sent_test.py"

kill $YARN_PID
