#!/bin/sh
# Проверка команд ls, cd, tail, whoami и ошибок каждой из них.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/deep --script scripts/start_commands.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_ls_error.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_cd_error.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_tail_error.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_whoami_error.txt
