#!/bin/sh
# Скрипты с ошибками: выполнение останавливается на первой ошибке.
cd "$(dirname "$0")/.."
python3 src/main.py --vfs vfs/files --script scripts/start_error.txt
python3 src/main.py --vfs vfs/deep --script scripts/start_quote.txt