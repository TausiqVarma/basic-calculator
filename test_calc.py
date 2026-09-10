import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from calc import add, divide, main, multiply, subtract


class TestCalc(unittest.TestCase):
    subtraction_cases = (
        (-5, 3, -8),
        (5, -3, 8),
        (-5, -3, -2),
        (-5, -5, 0),
        (0, -3, 3),
        (-3, 0, -3),
        (5, 3, 2),
        (3, 5, -2),
        (0, 0, 0),
    )
    decimal_subtraction_cases = (
        (-5.5, 3.25, -8.75),
        (5.5, -3.25, 8.75),
        (-5.5, -3.25, -2.25),
        (-5.5, -5.5, 0.0),
        (0.0, -3.25, 3.25),
        (-3.25, 0.0, -3.25),
        (5.5, 3.25, 2.25),
        (3.25, 5.5, -2.25),
        (0.0, 0.0, 0.0),
    )

    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract_integer_sign_matrix(self):
        for left, right, expected in self.subtraction_cases:
            with self.subTest(left=left, right=right):
                self.assertEqual(subtract(left, right), expected)

    def test_subtract_decimal_sign_matrix(self):
        for left, right, expected in self.decimal_subtraction_cases:
            with self.subTest(left=left, right=right):
                self.assertAlmostEqual(subtract(left, right), expected)

    def test_cli_subtraction_sign_matrix(self):
        cases = self.subtraction_cases + self.decimal_subtraction_cases
        for left, right, expected in cases:
            with self.subTest(left=left, right=right):
                output = io.StringIO()
                inputs = (str(left), "-", str(right))
                with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
                    main()
                self.assertEqual(output.getvalue().splitlines()[-1], f"Result: {float(expected)}")

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero(self):
        self.assertRaises(ValueError, divide, 5, 0)


if __name__ == '__main__':
    unittest.main()
