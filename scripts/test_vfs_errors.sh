#!/bin/sh
# Ошибки VFS: директория не существует, путь указывает на файл.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/no_such_dir --script scripts/start_vfs.txt
python3 src/main.py --vfs vfs/minimal/readme.txt --script scripts/start_vfs.txt
