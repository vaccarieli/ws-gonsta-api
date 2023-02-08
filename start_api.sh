#!/bin/bash

sleep 60

# Create a new tmux session
tmux new-session -d -s start_api

# Send a command to the tmux session
tmux send-keys -t start_api "yarn --cwd /home/vaccarieli/ws-gonsta-api/ start" C-m