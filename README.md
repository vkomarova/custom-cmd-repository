# Эмулятор для языка оболочки ОС

Реализация эмулятора оболочки UNIX-подобной ОС на Python. На данный момент готов первый этап - базовый REPL.

## Этап 1. REPL

В ходе выполнения первой части работы было реализовано:

- консольный интерфейс (CLI) с приглашением к вводу вида `username@hostname:~$` на основе
  реальных данных ОС;
- парсер, который обрабатывает аргументы в кавычках;
- команды-заглушки `ls` и `cd`, которые выводят свое имя и аргументы;
- команда `exit` для выхода из эмулятора;
- обработка ошибок: незакрытая кавычка, неизвестная команда.


## Этап 2. Конфигурация

В ходе выполнения второй части работы было реализовано:

- параметр командной строки `--vfs` - путь к физическому расположению VFS;
- параметр командной строки `--script` - путь к стартовому скрипту;
- отладочный вывод всех заданных параметров при запуске;
- выполнение стартового скрипта: на экране отображаются ввод и вывод,
  выполнение останавливается при первой ошибке;
- если стартовый скрипт не задан, запускается интерактивный режим.

Скрипты для проверки (папка `scripts`):

```
start_ok.txt      стартовый скрипт без ошибок
start_error.txt   стартовый скрипт с неизвестной командой
start_quote.txt   стартовый скрипт с незакрытой кавычкой
test_ok.sh        запуск эмулятора со скриптом без ошибок
test_errors.sh    запуск эмулятора со скриптами с ошибками
test_no_file.sh   запуск эмулятора с несуществующим скриптом
```
## Этап 3. VFS

В ходе выполнения третей части работы было реализовано:

- VFS загружается из директории на диске, путь задаётся параметром `--vfs`;
- все папки и файлы (вместе с содержимым) хранятся в памяти в виде
  словаря, данные на диске не изменяются;
- служебная команда `vfs-tree` выводит дерево папок и файлов VFS;
- ошибка, если директория VFS не задана или не существует.

Варианты VFS (папка `vfs`):

```
vfs/minimal   минимальная VFS: один файл
vfs/files     несколько файлов
vfs/deep      не менее 3 уровней файлов и папок
```

Скрипты для проверки (папка `scripts`):

```
start_vfs.txt        стартовый скрипт со всеми командами этапов 1-3
test_vfs_minimal.sh  запуск с минимальной VFS
test_vfs_files.sh    запуск с VFS из нескольких файлов
test_vfs_deep.sh     запуск с многоуровневой VFS
test_vfs_errors.sh   запуск с несуществующей VFS и с файлом вместо папки
```

## Этап 4. Основные команды

В ходе выполнения четвертой части работы было реализовано:

- `ls [путь]` - выводит содержимое папки или имя файла;
- `cd [путь]` - переходит в папку, без аргументов переходит в корень VFS;
- `tail [-n N] файл` - выводит последние N строк файла (по умолчанию 10);
- `whoami` - выводит имя текущего пользователя;
- пути бывают абсолютные (`/home/user`) и относительные (`docs`, `..`, `.`);
- текущая папка показывается в приглашении: `user@computer:~/home/user$`;
- ошибки: несуществующий путь, `cd` в файл, `tail` для папки,
  неверное число строк в `tail -n`, лишние аргументы.

Скрипты для проверки (папка `scripts`):

```
start_commands.txt      все режимы команд ls, cd, tail, whoami
start_ls_error.txt      ошибка ls: несуществующий путь
start_cd_error.txt      ошибка cd: переход в файл
start_tail_error.txt    ошибка tail: неверное число строк
start_whoami_error.txt  ошибка whoami: лишний аргумент
test_commands.sh        запуск всех скриптов этапа 4
```

## Этап 5. Дополнительные команды

В ходе выполнения пятой части работы было реализовано:

- `rm файл` - удаляет файл;
- `rm -r папка` - удаляет папку со всем содержимым;
- `cp файл новое_имя` - копирует файл под новым именем;
- `cp файл папка` - копирует файл в существующую папку;
- `cp -r папка новое_имя` - копирует папку со всем содержимым;
- все изменения выполняются только в памяти, файлы на диске не меняются;
- ошибки: несуществующий путь, папка без ключа `-r`, удаление или
  копирование корня, неверное число аргументов.

Скрипты для проверки (папка `scripts`):

```
start_change.txt    все режимы команд rm и cp
start_rm_error.txt  ошибка rm: удаление папки без -r
start_cp_error.txt  ошибка cp: копирование папки без -r
test_change.sh      запуск всех скриптов этапа 5 и проверка диска
```

## Структура

```
src/main.py         исходный код
tests/test_main.py  тесты
scripts/            стартовые скрипты и скрипты для проверки
vfs/                варианты VFS для проверки
run.sh              запуск в Linux/macOS
run.bat             запуск в Windows
Makefile            запуск и тесты через make
```

## Запуск

Для Linux/macOS:

```
./run.sh
```

Для Windows:

```
run.bat
```

Через Makefile:

```
make run
make test
```

Проверочные скрипты:

```
sh scripts/test_ok.sh
sh scripts/test_errors.sh
sh scripts/test_no_file.sh
sh scripts/test_vfs_minimal.sh
sh scripts/test_vfs_files.sh
sh scripts/test_vfs_deep.sh
sh scripts/test_vfs_errors.sh
sh scripts/test_commands.sh
sh scripts/test_change.sh
```

## Пример работы (этап 1)

```
user@computer:~$ ls
Команда: ls
Аргументы: []
user@computer:~$ ls -l /home
Команда: ls
Аргументы: ['-l', '/home']
user@computer:~$ cd "My Documents"
Команда: cd
Аргументы: ['My Documents']
user@computer:~$ cd 'a b' "c d"
Команда: cd
Аргументы: ['a b', 'c d']
user@computer:~$ ls "abc
Ошибка: незакрытая кавычка
user@computer:~$ pwd
pwd: команда не найдена
user@computer:~$
user@computer:~$ exit
```
## Пример работы (этап 2)

```
$ sh scripts/test_errors.sh
Путь к VFS: /home/user/vfs
Путь к стартовому скрипту: scripts/start_error.txt
user@computer:~$ ls
Команда: ls
Аргументы: []
user@computer:~$ cd docs
Команда: cd
Аргументы: ['docs']
user@computer:~$ pwd
Ошибка: pwd: команда не найдена
Выполнение скрипта остановлено
```


## Пример работы (этап 3)

```
$ sh scripts/test_vfs_deep.sh
Путь к VFS: vfs/deep
Путь к стартовому скрипту: scripts/start_vfs.txt
user@computer:~$ vfs-tree
etc/
  hostname
home/
  user/
    docs/
      notes.txt
      plan.txt
    music/
      list.txt
user@computer:~$ ls
Команда: ls
Аргументы: []
...
user@computer:~$ pwd
Ошибка: pwd: команда не найдена
Выполнение скрипта остановлено
```


## Пример работы (этап 4)

```
$ sh scripts/test_commands.sh
Путь к VFS: vfs/deep
Путь к стартовому скрипту: scripts/start_commands.txt
user@computer:~$ whoami
user
user@computer:~$ ls
etc
home
user@computer:~$ cd home/user/docs
user@computer:~/home/user/docs$ tail -n 1 notes.txt
сделать этап 3
user@computer:~/home/user/docs$ cd ..
user@computer:~/home/user$ ls
docs
music
...
user@computer:~$ exit
Путь к VFS: vfs/deep
Путь к стартовому скрипту: scripts/start_cd_error.txt
user@computer:~$ cd home/user
user@computer:~/home/user$ cd docs/notes.txt
Ошибка: cd: docs/notes.txt: это не каталог
Выполнение скрипта остановлено
```

## Пример работы (этап 5)

```
$ sh scripts/test_change.sh
Путь к VFS: vfs/deep
Путь к стартовому скрипту: scripts/start_change.txt
user@computer:~$ cp home/user/docs/notes.txt home/user/docs/copy.txt
user@computer:~$ ls home/user/docs
copy.txt
notes.txt
plan.txt
...
user@computer:~/home/user$ rm -r music
user@computer:~/home/user$ ls
backup
docs
...
Путь к VFS: vfs/deep
Путь к стартовому скрипту: scripts/start_rm_error.txt
user@computer:~$ rm home/user/docs/plan.txt
user@computer:~$ rm home/user
Ошибка: rm: home/user: это каталог
Выполнение скрипта остановлено
...
Файлы на диске не изменились:
```