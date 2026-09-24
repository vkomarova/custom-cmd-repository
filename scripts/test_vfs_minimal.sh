#!/bin/sh
# Минимальная VFS: один файл.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/minimal --script scripts/start_vfs.txt
