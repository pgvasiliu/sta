#!/usr/bin/env python
# coding: utf-8

# copied from https://gist.github.com/fisadev/044af2854ba38bcd6ef8
from os import system


PROJECT_PATH = '~/PROJECTS/github.com/sta'
WEB_PATH = '~/PROJECTS/github.com/sta/plotting/app'

def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)

#tmux('new -s ST')

tmux('select-window -t 1')
tmux_shell('cd %s' % PROJECT_PATH)
tmux('rename-window "main.py"')
tmux_shell("python3 main.py -t SPY -i 1d -p 60")

# console in project
tmux('new-window')
tmux('select-window -t 2')
tmux_shell('cd %s' % PROJECT_PATH)
#tmux_shell(ACTIVATE_VENV)
tmux('rename-window "console"')
# second console as split
tmux('split-window -v')
tmux('select-pane -t 2')
tmux_shell('cd %s/plotting' % PROJECT_PATH)
#tmux_shell(ACTIVATE_VENV)
tmux('rename-window "plotting"')
tmux_shell("sh RUN.sh SPY")

# local server
tmux('new-window')
tmux('select-window -t 3')
tmux_shell('cd %s' % PROJECT_PATH)
#tmux_shell(ACTIVATE_VENV)
tmux_shell('cd %s' % WEB_PATH)
tmux_shell('python3 run.py')
tmux('rename-window "server"')

# go back to the first window
tmux('select-window -t 1')

#tmux('at')

