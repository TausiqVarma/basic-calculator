def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


_MEMORY_ALIASES = ("m", "mem")
_ABORT_CALCULATION = object()


class Calculator:
    """A calculator session that remembers its latest successful result."""

    def __init__(self):
        self.memory = None

    def resolve_operand(self, raw_operand):
        """Resolve a numeric operand or an exact lowercase memory alias."""
        if raw_operand in _MEMORY_ALIASES:
            if self.memory is None:
                print("Memory is empty")
                return _ABORT_CALCULATION
            return self.memory
        return float(raw_operand)

    def calculate(self, raw_num1, op, raw_num2):
        """Calculate with raw operands and remember a successful result."""
        num1 = self.resolve_operand(raw_num1)
        if num1 is _ABORT_CALCULATION:
            return None

        num2 = self.resolve_operand(raw_num2)
        if num2 is _ABORT_CALCULATION:
            return None

        if op == '+':
            result = add(num1, num2)
        elif op == '-':
            result = subtract(num1, num2)
        elif op == '*':
            result = multiply(num1, num2)
        elif op == '/':
            result = divide(num1, num2)
        else:
            print("Invalid operator")
            return None

        self.memory = result
        return result


def main():
    print("Basic Calculator")
    calculator = Calculator()

    while True:
        try:
            num1 = input("Enter first number: ")
            op = input("Enter operator (+, -, *, /): ")
            num2 = input("Enter second number: ")
        except EOFError:
            return

        result = calculator.calculate(num1, op, num2)
        if result is not None:
            print(f"Result: {result}")


if __name__ == "__main__":
    main()
