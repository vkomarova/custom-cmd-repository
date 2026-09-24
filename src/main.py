import getpass
import socket
import argparse


def get_prompt():
    username = getpass.getuser()
    hostname = socket.gethostname()
    return username + "@" + hostname + ":~$ "


def parse(line):
    words = []
    word = ""
    quote = ""
    for char in line:
        if quote:
            if char == quote:
                quote = ""
            else:
                word += char
        elif char == "'" or char == '"':
            quote = char
        elif char == " ":
            if word:
                words.append(word)
                word = ""
        else:
            word += char
    if quote:
        raise ValueError("незакрытая кавычка")
    if word:
        words.append(word)
    return words


def run_command(words):
    name = words[0]
    args = words[1:]
    if name == "exit":
        return False
    if name == "ls" or name == "cd":
        print("Команда:", name)
        print("Аргументы:", args)
        return True
    raise ValueError(name + ": команда не найдена")


def execute(line):
    words = parse(line)
    if not words:
        return True
    return run_command(words)


def run_script(path):
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError:
        print("Ошибка: не удалось открыть скрипт", path)
        return
    for line in lines:
        print(get_prompt() + line)
        try:
            if not execute(line):
                return
        except ValueError as error:
            print("Ошибка:", error)
            print("Выполнение скрипта остановлено")
            return


def repl():
    while True:
        line = input(get_prompt())
        try:
            if not execute(line):
                break
        except ValueError as error:
            print("Ошибка:", error)


def main():
    parser = argparse.ArgumentParser(description="Эмулятор командной строки")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    args = parser.parse_args()
    print("Путь к VFS:", args.vfs)
    print("Путь к стартовому скрипту:", args.script)
    if args.script:
        run_script(args.script)
    else:
        repl()


if __name__ == "__main__":
    main()
