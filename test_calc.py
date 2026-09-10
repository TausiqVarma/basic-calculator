import io
import unittest
from unittest.mock import patch

from calc import add, divide, main, multiply, subtract


SUBTRACTION_CASES = (
    ("negative left operand", -5, 3, -8),
    ("negative right operand", 5, -3, 8),
    ("two negative operands", -5, -3, -2),
    ("reversed negative operands", -3, -5, 2),
    ("zero minus negative", 0, -3, 3),
    ("negative minus zero", -3, 0, -3),
    ("positive baseline", 5, 3, 2),
)


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract_integer_sign_and_zero_matrix(self):
        for scenario, left, right, expected in SUBTRACTION_CASES:
            with self.subTest(scenario=scenario, left=left, right=right):
                self.assertEqual(subtract(left, right), expected)

    def test_subtract_decimal_sign_and_zero_matrix(self):
        for scenario, left, right, expected in SUBTRACTION_CASES:
            with self.subTest(scenario=scenario, left=left, right=right):
                self.assertEqual(
                    subtract(float(left), float(right)), float(expected)
                )

    def test_subtract_is_deterministic(self):
        for run in range(5):
            with self.subTest(run=run):
                self.assertEqual(subtract(-5, -3), -2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero(self):
        self.assertRaises(ValueError, divide, 5, 0)


class TestCalculatorCli(unittest.TestCase):
    def test_subtraction_sign_and_zero_matrix(self):
        for scenario, left, right, expected in SUBTRACTION_CASES:
            with self.subTest(scenario=scenario, left=left, right=right):
                user_input = [str(left), "-", str(right)]
                with patch("builtins.input", side_effect=user_input), patch(
                    "sys.stdout", new_callable=io.StringIO
                ) as output:
                    main()

                self.assertIn(f"Result: {float(expected)}", output.getvalue())


if __name__ == "__main__":
    unittest.main()
