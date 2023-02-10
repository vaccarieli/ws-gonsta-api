#!/bin/bash

# Create a new tmux session
tmux new-session -d -s api

# Send a command to the tmux session
tmux send-keys -t api "yarn --cwd /home/vaccarieli/ws-gonsta-api/ start" C-m