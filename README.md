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

## Структура

```
src/main.py         исходный код
tests/test_main.py  тесты
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

## Пример работы

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
