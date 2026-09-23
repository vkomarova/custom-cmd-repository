import getpass
import socket


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
    else:
        print(name + ": команда не найдена")
    return True


def main():
    while True:
        line = input(get_prompt())
        try:
            words = parse(line)
        except ValueError as error:
            print("Ошибка:", error)
            continue
        if not words:
            continue
        if not run_command(words):
            break


if __name__ == "__main__":
    main()
