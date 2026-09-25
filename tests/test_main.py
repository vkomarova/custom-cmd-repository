import unittest
import io
import contextlib
import getpass

from src.main import (execute, get_path, load_vfs, parse, run_command,
                      run_script)


def run_and_get_output(words, vfs, cwd):
    """Выполняет команду и возвращает то, что она вывела."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        run_command(words, vfs, cwd)
    return output.getvalue()


class TestParse(unittest.TestCase):

    def test_simple(self):
        """Проверяет разбор строки без кавычек."""
        self.assertEqual(parse("ls a b"), ["ls", "a", "b"])

    def test_quotes(self):
        """Проверяет разбор аргументов в кавычках."""
        result = parse("cd \"my folder\" 'a b'")
        self.assertEqual(result, ["cd", "my folder", "a b"])

    def test_bad_quote(self):
        """Проверяет ошибку при незакрытой кавычке."""
        with self.assertRaises(ValueError):
            parse("ls \"abc")


class TestRunCommand(unittest.TestCase):

    def test_exit(self):
        """Проверяет, что exit завершает работу."""
        self.assertFalse(run_command(["exit"], {}, []))

    def test_unknown(self):
        """Проверяет ошибку при неизвестной команде."""
        with self.assertRaises(ValueError):
            run_command(["pwd"], {}, [])

    def test_empty_line(self):
        """Проверяет, что пустая строка не завершает работу."""
        self.assertTrue(execute("", {}, []))


class TestRunScript(unittest.TestCase):

    def test_stop_on_error(self):
        """Проверяет, что скрипт останавливается при первой ошибке."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_script("scripts/start_error.txt", {}, [])
        self.assertIn("pwd: команда не найдена", output.getvalue())
        self.assertNotIn("не выполнится", output.getvalue())

    def test_no_file(self):
        """Проверяет ошибку, если скрипта не существует."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_script("scripts/no_such_file.txt", {}, [])
        self.assertIn("не удалось открыть скрипт", output.getvalue())


class TestVfs(unittest.TestCase):

    def test_load_minimal(self):
        """Проверяет загрузку VFS с одним файлом."""
        vfs = load_vfs("vfs/minimal")
        self.assertEqual(list(vfs), ["readme.txt"])

    def test_load_deep(self):
        """Проверяет загрузку VFS с несколькими уровнями папок."""
        vfs = load_vfs("vfs/deep")
        notes = vfs["home"]["user"]["docs"]["notes.txt"]
        self.assertIn("Заметки", notes)

    def test_vfs_tree(self):
        """Проверяет вывод дерева VFS командой vfs-tree."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_command(["vfs-tree"], load_vfs("vfs/deep"), [])
        self.assertIn("      notes.txt", output.getvalue())


class TestCommands(unittest.TestCase):

    def setUp(self):
        """Загружает многоуровневую VFS перед каждым тестом."""
        self.vfs = load_vfs("vfs/deep")

    def test_get_path(self):
        """Проверяет перевод пути в список папок."""
        self.assertEqual(get_path("../etc", ["home"]), ["etc"])
        self.assertEqual(get_path("/home/./user", ["etc"]), ["home", "user"])

    def test_ls(self):
        """Проверяет вывод содержимого папки."""
        output = run_and_get_output(["ls", "home/user"], self.vfs, [])
        self.assertEqual(output, "docs\nmusic\n")

    def test_ls_error(self):
        """Проверяет ошибку ls для несуществующего пути."""
        with self.assertRaises(ValueError):
            run_command(["ls", "nobody"], self.vfs, [])

    def test_cd(self):

        """Проверяет переход в папку и обратно."""
        cwd = []
        run_command(["cd", "home/user"], self.vfs, cwd)
        self.assertEqual(cwd, ["home", "user"])
        run_command(["cd", ".."], self.vfs, cwd)
        self.assertEqual(cwd, ["home"])
        run_command(["cd"], self.vfs, cwd)
        self.assertEqual(cwd, [])

    def test_cd_to_file(self):
        """Проверяет ошибку cd, если путь ведёт к файлу."""
        with self.assertRaises(ValueError):
            run_command(["cd", "etc/hostname"], self.vfs, [])

    def test_tail(self):
        """Проверяет вывод последних строк файла."""
        words = ["tail", "-n", "1", "home/user/docs/notes.txt"]
        output = run_and_get_output(words, self.vfs, [])
        self.assertEqual(output, "сделать этап 3\n")

    def test_tail_error(self):
        """Проверяет ошибку tail для папки."""
        with self.assertRaises(ValueError):
            run_command(["tail", "home"], self.vfs, [])

    def test_whoami(self):
        """Проверяет вывод имени пользователя."""
        output = run_and_get_output(["whoami"], self.vfs, [])
        self.assertEqual(output, getpass.getuser() + "\n")


class TestChangeCommands(unittest.TestCase):

    def setUp(self):
        """Загружает многоуровневую VFS перед каждым тестом."""
        self.vfs = load_vfs("vfs/deep")

    def test_rm_file(self):
        """Проверяет удаление файла."""
        run_command(["rm", "etc/hostname"], self.vfs, [])
        self.assertEqual(self.vfs["etc"], {})

    def test_rm_dir(self):
        """Проверяет удаление папки с ключом -r."""
        run_command(["rm", "-r", "home"], self.vfs, [])
        self.assertEqual(list(self.vfs), ["etc"])

    def test_rm_dir_error(self):
        """Проверяет ошибку rm для папки без ключа -r."""
        with self.assertRaises(ValueError):
            run_command(["rm", "home"], self.vfs, [])

    def test_rm_only_in_memory(self):
        """Проверяет, что rm не меняет файлы на диске."""
        run_command(["rm", "-r", "home"], self.vfs, [])
        self.assertIn("home", load_vfs("vfs/deep"))

    def test_cp_file(self):
        """Проверяет копирование файла под новым именем."""
        run_command(["cp", "etc/hostname", "etc/name"], self.vfs, [])
        self.assertEqual(self.vfs["etc"]["name"], self.vfs["etc"]["hostname"])

    def test_cp_to_dir(self):
        """Проверяет копирование файла в существующую папку."""
        run_command(["cp", "etc/hostname", "home"], self.vfs, [])
        self.assertIn("hostname", self.vfs["home"])

    def test_cp_dir(self):
        """Проверяет копирование папки с ключом -r."""
        run_command(["cp", "-r", "home/user", "copy"], self.vfs, [])
        run_command(["rm", "copy/docs/notes.txt"], self.vfs, [])
        self.assertNotIn("notes.txt", self.vfs["copy"]["docs"])
        self.assertIn("notes.txt", self.vfs["home"]["user"]["docs"])

    def test_cp_dir_error(self):
        """Проверяет ошибку cp для папки без ключа -r."""
        with self.assertRaises(ValueError):
            run_command(["cp", "home", "copy"], self.vfs, [])

    def test_cp_no_source(self):
        """Проверяет ошибку cp для несуществующего источника."""
        with self.assertRaises(ValueError):
            run_command(["cp", "nobody.txt", "copy.txt"], self.vfs, [])


if __name__ == "__main__":
    unittest.main()
