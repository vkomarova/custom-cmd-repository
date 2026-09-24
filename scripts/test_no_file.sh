#!/bin/sh
# Стартового скрипта не существует.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs --script scripts/no_such_file.txt
