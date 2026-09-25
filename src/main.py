import getpass
import socket
import argparse
import os

TAIL_LINES = 10
MAX_ARGS = 1


def get_prompt(cwd):
    username = getpass.getuser()
    hostname = socket.gethostname()
    path = "~"
    for name in cwd:
        path += "/" + name
    return username + "@" + hostname + ":" + path + "$ "


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


def get_path(path, cwd):
    if path.startswith("/"):
        parts = []
    else:
        parts = list(cwd)
    for name in path.split("/"):
        if name == "..":
            if parts:
                parts.pop()
        elif name != "" and name != ".":
            parts.append(name)
    return parts


def find(vfs, parts):
    node = vfs
    for name in parts:
        if not isinstance(node, dict) or name not in node:
            return None
        node = node[name]
    return node


def run_ls(args, vfs, cwd):
    if len(args) > MAX_ARGS:
        raise ValueError("ls: слишком много аргументов")
    path = "."
    if args:
        path = args[0]
    node = find(vfs, get_path(path, cwd))
    if node is None:
        raise ValueError("ls: " + path + ": нет такого файла или каталога")
    if isinstance(node, dict):
        for name in sorted(node):
            print(name)
    else:
        print(path)


def run_cd(args, vfs, cwd):
    if len(args) > MAX_ARGS:
        raise ValueError("cd: слишком много аргументов")
    if not args:
        cwd.clear()
        return
    parts = get_path(args[0], cwd)
    node = find(vfs, parts)
    if node is None:
        raise ValueError("cd: " + args[0] + ": нет такого каталога")
    if not isinstance(node, dict):
        raise ValueError("cd: " + args[0] + ": это не каталог")
    cwd.clear()
    cwd.extend(parts)


def read_file(path, vfs, cwd):
    node = find(vfs, get_path(path, cwd))
    if node is None:
        raise ValueError("tail: " + path + ": нет такого файла")
    if isinstance(node, dict):
        raise ValueError("tail: " + path + ": это каталог")
    return node


def run_tail(args, vfs, cwd):
    count = TAIL_LINES
    if args and args[0] == "-n":
        args = args[1:]
        if not args or not args[0].isdigit():
            raise ValueError("tail: неверное число строк")
        count = int(args[0])
        args = args[1:]
    if not args:
        raise ValueError("tail: не указан файл")
    if len(args) > MAX_ARGS:
        raise ValueError("tail: слишком много аргументов")
    lines = read_file(args[0], vfs, cwd).splitlines()
    start = max(len(lines) - count, 0)
    for line in lines[start:]:
        print(line)


def run_whoami(args):
    if args:
        raise ValueError("whoami: лишний аргумент")
    print(getpass.getuser())


def run_command(words, vfs, cwd):
    name = words[0]
    args = words[1:]
    if name == "exit":
        return False
    if name == "vfs-tree":
        print_vfs(vfs, "")
    elif name == "ls":
        run_ls(args, vfs, cwd)
    elif name == "cd":
        run_cd(args, vfs, cwd)
    elif name == "tail":
        run_tail(args, vfs, cwd)
    elif name == "whoami":
        run_whoami(args)
    else:
        raise ValueError(name + ": команда не найдена")
    return True


def execute(line, vfs, cwd):
    words = parse(line)
    if not words:
        return True
    return run_command(words, vfs, cwd)


def run_script(path, vfs, cwd):
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError:
        print("Ошибка: не удалось открыть скрипт", path)
        return
    for line in lines:
        print(get_prompt(cwd) + line)
        try:
            if not execute(line, vfs, cwd):
                return
        except ValueError as error:
            print("Ошибка:", error)
            print("Выполнение скрипта остановлено")
            return


def repl(vfs, cwd):
    while True:
        line = input(get_prompt(cwd))
        try:
            if not execute(line, vfs, cwd):
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
    cwd = []
    if args.script:
        run_script(args.script, vfs, cwd)
    else:
        repl(vfs, cwd)


if __name__ == "__main__":
    main()
