import unittest
import io
import contextlib

from src.main import execute, parse, run_command, run_script


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
        self.assertFalse(run_command(["exit"]))

    def test_ls(self):
        """Проверяет, что ls не завершает работу."""
        self.assertTrue(run_command(["ls", "a"]))

    def test_unknown(self):
        """Проверяет ошибку при неизвестной команде."""
        with self.assertRaises(ValueError):
            run_command(["pwd"])

    def test_empty_line(self):
        """Проверяет, что пустая строка не завершает работу."""
        self.assertTrue(execute(""))


class TestRunScript(unittest.TestCase):

    def test_stop_on_error(self):
        """Проверяет, что скрипт останавливается при первой ошибке."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_script("scripts/start_error.txt")
        self.assertIn("pwd: команда не найдена", output.getvalue())
        self.assertNotIn("не выполнится", output.getvalue())

    def test_no_file(self):
        """Проверяет ошибку, если скрипта не существует."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_script("scripts/no_such_file.txt")
        self.assertIn("не удалось открыть скрипт", output.getvalue())


if __name__ == "__main__":
    unittest.main()
