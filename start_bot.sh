#!/bin/bash

# Create a new tmux session
tmux new-session -d -s start_bot

# Send the command to the tmux session
tmux send-keys -t start_bot "python3 /home/vaccarieli/ws-gonsta-api/bot/bot.py" C-m
