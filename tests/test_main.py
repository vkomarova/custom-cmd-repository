import unittest

from src.main import parse, run_command


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


if __name__ == "__main__":
    unittest.main()
