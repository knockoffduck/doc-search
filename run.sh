#!/bin/bash

# Open WSL terminal window 1 and run 'pyenv activate DocSearch && python server/main.py'
wt.exe -d /home/dvck/projects/DocSearch/server/ wsl -e zsh -c '/home/dvck/.pyenv/shims/python ./main.py' 

# Open WSL terminal window 2 and run 'pnpm run dev'
wt.exe -d /home/dvck/projects/DocSearch/ wsl -e zsh -c 'pnpm run dev'

# Open WSL terminal window 3 and run 'cd server/pocketbase'
wt.exe -d /home/dvck/projects/DocSearch/server wsl -e zsh -c './pocketbase serve'
