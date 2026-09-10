import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from calc import add, divide, main, multiply, subtract


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero(self):
        with self.assertRaisesRegex(ValueError, "^Cannot divide by zero$"):
            divide(5, 0)

    def test_main_divide_by_zero_exits_gracefully(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch("builtins.input", side_effect=["10", "/", "0"]):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main()

        message = "Error: Cannot divide by zero. Please try again."
        self.assertIsNone(result)
        self.assertEqual(stdout.getvalue().splitlines(), ["Basic Calculator", message])
        self.assertEqual(stdout.getvalue().count(message), 1)
        self.assertNotIn("Traceback", stdout.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_main_valid_division(self):
        stdout = io.StringIO()

        with patch("builtins.input", side_effect=["10", "/", "2"]):
            with redirect_stdout(stdout):
                main()

        self.assertEqual(stdout.getvalue().splitlines(), ["Basic Calculator", "Result: 5.0"])


if __name__ == '__main__':
    unittest.main()
