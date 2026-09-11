import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from calc import Calculator, add, divide, main, multiply, subtract


class TestCalc(unittest.TestCase):
    def test_add(self): self.assertEqual(add(2, 3), 5)
    def test_subtract(self): self.assertEqual(subtract(5, 3), 2)
    def test_multiply(self): self.assertEqual(multiply(2, 3), 6)
    def test_divide(self): self.assertEqual(divide(6, 3), 2)
    def test_divide_by_zero(self): self.assertRaises(ValueError, divide, 5, 0)


class TestCalculatorMemory(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_new_session_starts_with_empty_memory(self):
        self.calculator.calculate("2", "+", "3")
        self.assertEqual(self.calculator.memory, 5)
        self.assertIsNone(Calculator().memory)

    def test_empty_memory_aliases_abort_with_exact_message(self):
        for alias in ("m", "mem"):
            with self.subTest(alias=alias):
                calculator = Calculator()
                output = io.StringIO()
                with redirect_stdout(output):
                    result = calculator.calculate(alias, "+", "1")
                self.assertIsNone(result)
                self.assertEqual(output.getvalue(), "Memory is empty\n")
                self.assertIsNone(calculator.memory)

    def test_empty_memory_in_second_operand_aborts(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = self.calculator.calculate("1", "+", "mem")
        self.assertIsNone(result)
        self.assertEqual(output.getvalue(), "Memory is empty\n")
        self.assertIsNone(self.calculator.memory)

    def test_aliases_work_in_both_operand_positions(self):
        for alias in ("m", "mem"):
            with self.subTest(alias=alias, position="first"):
                calculator = Calculator()
                calculator.calculate("8", "+", "2")
                self.assertEqual(calculator.calculate(alias, "-", "3"), 7)
            with self.subTest(alias=alias, position="second"):
                calculator = Calculator()
                calculator.calculate("8", "+", "2")
                self.assertEqual(calculator.calculate("13", "-", alias), 3)

    def test_memory_recall_with_all_operations(self):
        cases = (
            ("+", "5", 15),
            ("-", "4", 6),
            ("*", "3", 30),
            ("/", "4", 2.5),
        )
        for operator, operand, expected in cases:
            with self.subTest(operator=operator):
                calculator = Calculator()
                calculator.calculate("8", "+", "2")
                self.assertEqual(calculator.calculate("m", operator, operand), expected)
                self.assertEqual(calculator.memory, expected)

    def test_memory_recall_preserves_division_operand_order(self):
        self.calculator.calculate("8", "+", "2")
        self.assertEqual(self.calculator.calculate("100", "/", "mem"), 10)

    def test_chained_calculations_replace_memory(self):
        self.assertEqual(self.calculator.calculate("2", "+", "3"), 5)
        self.assertEqual(self.calculator.calculate("m", "*", "4"), 20)
        self.assertEqual(self.calculator.calculate("mem", "-", "2"), 18)
        self.assertEqual(self.calculator.memory, 18)

    def test_zero_negative_and_fractional_results_are_recalled(self):
        cases = (
            (("2", "-", "2"), ("m", "+", "1"), 1),
            (("2", "-", "5"), ("mem", "*", "2"), -6),
            (("1", "/", "2"), ("m", "+", "1"), 1.5),
        )
        for initial, recalled, expected in cases:
            with self.subTest(initial=initial):
                calculator = Calculator()
                calculator.calculate(*initial)
                self.assertEqual(calculator.calculate(*recalled), expected)

    def test_invalid_operand_preserves_memory(self):
        self.calculator.calculate("2", "+", "3")
        with self.assertRaises(ValueError):
            self.calculator.calculate("not-a-number", "+", "1")
        self.assertEqual(self.calculator.memory, 5)

    def test_failed_division_preserves_memory(self):
        self.calculator.calculate("2", "+", "3")
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            self.calculator.calculate("10", "/", "0")
        self.assertEqual(self.calculator.memory, 5)

    def test_invalid_operator_preserves_memory(self):
        self.calculator.calculate("2", "+", "3")
        output = io.StringIO()
        with redirect_stdout(output):
            result = self.calculator.calculate("4", "^", "2")
        self.assertIsNone(result)
        self.assertEqual(output.getvalue(), "Invalid operator\n")
        self.assertEqual(self.calculator.memory, 5)

    def test_aliases_are_case_sensitive(self):
        self.calculator.calculate("2", "+", "3")
        for alias in ("M", "MEM", "Mem"):
            with self.subTest(alias=alias):
                with self.assertRaises(ValueError):
                    self.calculator.calculate(alias, "+", "1")
        self.assertEqual(self.calculator.memory, 5)

    @patch("builtins.input", side_effect=["2", "+", "3", "m", "*", "4", EOFError])
    def test_main_keeps_memory_for_the_cli_session(self, _mock_input):
        output = io.StringIO()
        with redirect_stdout(output):
            main()
        self.assertEqual(
            output.getvalue(),
            "Basic Calculator\nResult: 5.0\nResult: 20.0\n",
        )


if __name__ == '__main__':
    unittest.main()
