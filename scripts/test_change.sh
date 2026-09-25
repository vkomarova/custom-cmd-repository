#!/bin/sh
# Проверка команд rm, cp и ошибок каждой из них.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/deep --script scripts/start_change.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_rm_error.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_cp_error.txt
echo "Файлы на диске не изменились:"
ls -R vfs/deep
