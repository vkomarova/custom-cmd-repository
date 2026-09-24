#!/bin/sh
# VFS с несколькими файлами.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/files --script scripts/start_vfs.txt
