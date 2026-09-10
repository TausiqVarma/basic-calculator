# Issue 3: Negative-subtraction investigation

## Scope and environment

- Issue: [#3, Subtraction gives wrong answer sometimes](https://github.com/TausiqVarma/basic-calculator/issues/3)
- Investigated revision: `2651b0058062ba249aa3624ee0a502094532122f`
- Runtime used for verification: Python 3
- Supported paths found: direct arithmetic-function calls and the interactive CLI in `calc.py`
- Existing numeric representations found: Python integers and floating-point values; the CLI parses both operands with `float()`

## Root-cause investigation

The reported symptom could not be reproduced. The arithmetic function already evaluates `a - b`, and the CLI parses each operand independently before selecting the subtraction operation. A leading minus sign is therefore interpreted by `float()` as an operand sign rather than as the binary subtraction operator. The CLI prints the resulting value without changing its sign.

Because no incorrect production path was identified, changing production logic would be speculative. The smallest appropriate change is deterministic regression coverage for every identified input path and existing numeric representation.

## Verification matrix

All integer cases passed through `subtract()` and the CLI:

| Expression | Observed result |
|---|---:|
| `-5 - 3` | `-8` |
| `5 - (-3)` | `8` |
| `-5 - (-3)` | `-2` |
| `-5 - (-5)` | `0` |
| `0 - (-3)` | `3` |
| `-3 - 0` | `-3` |
| `5 - 3` | `2` |
| `3 - 5` | `-2` |
| `0 - 0` | `0` |

All floating-point cases passed through `subtract()` and the CLI:

| Expression | Observed result |
|---|---:|
| `-5.5 - 3.25` | `-8.75` |
| `5.5 - (-3.25)` | `8.75` |
| `-5.5 - (-3.25)` | `-2.25` |
| `-5.5 - (-5.5)` | `0.0` |
| `0.0 - (-3.25)` | `3.25` |
| `-3.25 - 0.0` | `-3.25` |
| `5.5 - 3.25` | `2.25` |
| `3.25 - 5.5` | `-2.25` |
| `0.0 - 0.0` | `0.0` |

The CLI assertions also verify the user-visible `Result:` line, including its sign. Existing addition, multiplication, division, and divide-by-zero tests remain in the suite.

## Validation

Command:

```text
python -m unittest -v
```

Result: `Ran 7 tests in 0.006s` and `OK`. The 7 test methods include 36 deterministic subtraction subtests: 18 direct-function cases and the same 18 cases through the CLI.

No dependency, configuration, or production source change was required.
