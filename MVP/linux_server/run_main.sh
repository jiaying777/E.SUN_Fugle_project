#!/bin/bash
tmux kill-session -t my_session
sleep 2
tmux new-session -d -s my_session 'python3 main.py'