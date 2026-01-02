# Recognit

**Validate if a value plausibly matches a header definition**

Given a naked value (like `40.00` or `650`) and a header definition, recognit checks if they're cognitively compatible using consensus-based validation.

## What It Does

Takes a value and a header definition, runs 4 validation tests, returns True if the tests pass a configurable threshold (default: ≥66%).

**The 4 tests:**
1. **Position check**: Is the value's x-coordinate within ±12px of the header's expected position?
2. **Max check**: Is the numeric value ≤ the header's maximum?
3. **Min check**: Is the numeric value ≥ the header's minimum?
4. **Validator check**: Does the value pass the custom validator function? (optional)

**Pass threshold**: Configurable (default 0.66 = 66% of tests must pass)

## Installation

bash
pip install recognit
Usage
from recognit import recognit

# Header definition
header = {
    "x_center": 150,
    "max_value": 40,
    "min_value": 0,
    "validator": None
}

# Value object (must have .x and .text attributes)
class Value:
    def __init__(self, x, text):
        self.x = x
        self.text = text

value = Value(x=148, text="8.50")

# Validate
if recognit(value, header):
    print("Match!")  # True: position close, value in range
License
MIT
