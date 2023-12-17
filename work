#!/usr/bin/env python
# coding: utf-8

# copied from https://gist.github.com/fisadev/044af2854ba38bcd6ef8
from os import system


PROJECT_PATH = '~/PROJECTS/github.com/pyenv/sta'
ACTIVATE_VENV = '. ~/PROJECTS/github.com/pyenv/env/bin/activate'
WEB_PATH = '~/PROJECTS/github.com/pyenv/web/app'

def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)

# example: one tab with vim, other tab with two consoles (vertical split)
# with virtualenvs on the project, and a third tab with the server running

#tmux('new -s ST')

# vim in project
tmux('select-window -t 0')
tmux_shell('cd %s' % PROJECT_PATH)
tmux('rename-window "vim"')

# console in project
tmux('new-window')
tmux('select-window -t 1')
tmux_shell('cd %s' % PROJECT_PATH)
tmux_shell(ACTIVATE_VENV)
tmux('rename-window "console"')
# second console as split
tmux('split-window -v')
tmux('select-pane -t 1')
tmux_shell('cd %s' % PROJECT_PATH)
tmux_shell(ACTIVATE_VENV)
tmux('rename-window "console"')

# local server
tmux('new-window')
tmux('select-window -t 2')
tmux_shell('cd %s' % PROJECT_PATH)
tmux_shell(ACTIVATE_VENV)
tmux_shell('cd %s' % WEB_PATH)
tmux_shell('python3 run.py')
tmux('rename-window "server"')

# go back to the first window
tmux('select-window -t 0')

#tmux('at')

