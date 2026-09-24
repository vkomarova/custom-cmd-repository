#!/bin/sh
# VFS с тремя и более уровнями файлов и папок.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/deep --script scripts/start_vfs.txt
