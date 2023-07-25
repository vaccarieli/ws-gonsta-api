#!/bin/bash

# Set the yarn executable path
YARN_PATH="/var/services/homes/vaccarieli/.yarn/bin/yarn"

# Set the python executable path
PYTHON_PATH="/bin/python3"

# Run the project with yarn start and save output to log file
("$YARN_PATH" --cwd /var/services/homes/vaccarieli/ws-gonsta-api start) & 

YARN_PID=$!

(docker start jomjol-synology-opencv-tensorflow-1) &

sleep 10

echo "Sleeping for 10 seconds"

(docker exec -d 5561fdf34712 python upscalingImage.py) &

echo "Sleeping for 30 seconds"
sleep 30
echo "Running Python Script"

# # Execute the Python script
"$PYTHON_PATH" "/var/services/homes/vaccarieli/ws-gonsta-api/bot/sent_test.py"

docker stop jomjol-synology-opencv-tensorflow-1

kill $YARN_PID
