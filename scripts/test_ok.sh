#!/bin/sh
# Скрипт без ошибок: выполняются все команды до exit.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/minimal --script scripts/start_ok.txt
