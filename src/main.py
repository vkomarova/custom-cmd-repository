import getpass
import socket
import argparse
import os


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


def load_vfs(path):
    vfs = {}
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            vfs[name] = load_vfs(full_path)
        else:
            with open(full_path, encoding="utf-8") as file:
                vfs[name] = file.read()
    return vfs


def print_vfs(folder, indent):
    for name in sorted(folder):
        if isinstance(folder[name], dict):
            print(indent + name + "/")
            print_vfs(folder[name], indent + "  ")
        else:
            print(indent + name)


def run_command(words, vfs):
    name = words[0]
    args = words[1:]
    if name == "exit":
        return False
    if name == "vfs-tree":
        print_vfs(vfs, "")
        return True
    if name == "ls" or name == "cd":
        print("Команда:", name)
        print("Аргументы:", args)
        return True
    raise ValueError(name + ": команда не найдена")


def execute(line, vfs):
    words = parse(line)
    if not words:
        return True
    return run_command(words, vfs)


def run_script(path, vfs):
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError:
        print("Ошибка: не удалось открыть скрипт", path)
        return
    for line in lines:
        print(get_prompt() + line)
        try:
            if not execute(line, vfs):
                return
        except ValueError as error:
            print("Ошибка:", error)
            print("Выполнение скрипта остановлено")
            return


def repl(vfs):
    while True:
        line = input(get_prompt())
        try:
            if not execute(line, vfs):
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
    if args.vfs is None or not os.path.isdir(args.vfs):
        print("Ошибка: директория VFS не найдена:", args.vfs)
        return
    vfs = load_vfs(args.vfs)
    if args.script:
        run_script(args.script, vfs)
    else:
        repl(vfs)


if __name__ == "__main__":
    main()
