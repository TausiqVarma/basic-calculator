import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import calc
from calc import add, subtract, multiply, divide

class TestCalc(unittest.TestCase):
    def test_add(self): self.assertEqual(add(2,3), 5)
    def test_subtract(self): self.assertEqual(subtract(5,3), 2)
    def test_multiply(self): self.assertEqual(multiply(2,3), 6)
    def test_divide(self): self.assertEqual(divide(6,3), 2)

    def test_divide_by_zero(self):
        with self.assertRaisesRegex(ValueError, "^Cannot divide by zero$"):
            divide(5, 0)

    def test_main_divide_by_zero_exits_gracefully_without_retry(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch("builtins.input", side_effect=["10", "/", "0"]) as mocked_input:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = calc.main()

        message = "Error: Cannot divide by zero. Please try again."
        self.assertIsNone(result)
        self.assertEqual(mocked_input.call_count, 3)
        self.assertEqual(stdout.getvalue().splitlines(), ["Basic Calculator", message])
        self.assertEqual(stdout.getvalue().count(message), 1)
        self.assertNotIn("Traceback", stdout.getvalue())
        self.assertNotIn("ValueError", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_main_valid_division_is_unchanged(self):
        stdout = io.StringIO()

        with patch("builtins.input", side_effect=["10", "/", "2"]):
            with redirect_stdout(stdout):
                result = calc.main()

        self.assertIsNone(result)
        self.assertEqual(stdout.getvalue().splitlines(), ["Basic Calculator", "Result: 5.0"])

    def test_main_reraises_unrelated_value_error(self):
        stdout = io.StringIO()

        with patch("builtins.input", side_effect=["10", "/", "2"]):
            with patch("calc.divide", side_effect=ValueError("unexpected failure")):
                with redirect_stdout(stdout):
                    with self.assertRaisesRegex(ValueError, "^unexpected failure$"):
                        calc.main()

        self.assertNotIn("Error: Cannot divide by zero. Please try again.", stdout.getvalue())

    def test_divide_by_zero_process_exits_normally_without_traceback(self):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("calc.py"))],
            input="10\n/\n0\n",
            capture_output=True,
            text=True,
            check=False,
        )

        message = "Error: Cannot divide by zero. Please try again."
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.count(message), 1)
        self.assertNotIn("Traceback", completed.stdout)
        self.assertNotIn("ValueError", completed.stdout)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertNotIn("ValueError", completed.stderr)

if __name__ == '__main__':
    unittest.main()
