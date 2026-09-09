import io
import subprocess
import sys
import unittest
from pathlib import Path
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

    def test_divide_by_zero_preserves_function_contract(self):
        for divisor in (0, 0.0, -0.0):
            with self.subTest(divisor=divisor):
                with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
                    divide(5, divisor)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["10", "/", "0"])
    def test_main_handles_division_by_zero(self, mock_input, mock_stdout):
        main()

        output = mock_stdout.getvalue()
        message = "Error: Cannot divide by zero. Please try again."
        self.assertEqual(output.count(message), 1)
        self.assertNotIn("Result:", output)
        self.assertEqual(mock_input.call_count, 3)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["10", "/", "2"])
    def test_main_preserves_valid_division(self, mock_input, mock_stdout):
        main()

        self.assertIn("Result: 5.0", mock_stdout.getvalue())
        self.assertNotIn("Error: Cannot divide by zero", mock_stdout.getvalue())
        self.assertEqual(mock_input.call_count, 3)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["10", "/", "2"])
    @patch("calc.divide", side_effect=ValueError("Unexpected division failure"))
    def test_main_propagates_unrelated_value_error(
        self, mock_divide, mock_input, mock_stdout
    ):
        with self.assertRaisesRegex(ValueError, "Unexpected division failure"):
            main()

        mock_divide.assert_called_once_with(10.0, 2.0)
        self.assertNotIn(
            "Error: Cannot divide by zero. Please try again.",
            mock_stdout.getvalue(),
        )
        self.assertEqual(mock_input.call_count, 3)

    def test_cli_handles_division_by_zero_without_traceback(self):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("calc.py"))],
            input="10\n/\n0\n",
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )

        message = "Error: Cannot divide by zero. Please try again."
        combined_output = completed.stdout + completed.stderr
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(combined_output.count(message), 1)
        self.assertNotIn("Traceback (most recent call last)", combined_output)
        self.assertNotIn("ValueError: Cannot divide by zero", combined_output)
        self.assertEqual(completed.stderr, "")


if __name__ == '__main__':
    unittest.main()
