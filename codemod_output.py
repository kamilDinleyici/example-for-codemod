# File: lambda-code.py
"""Example Python code with lambda functions to be transformed."""

# Simple lambda functions
def add(x, y):
    return x + y
multiply = lambda a, b: a * b
square = lambda x: x ** 2

# Lambda functions in data structures
operations = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'divide': lambda x, y: x / y if y != 0 else 0
}

# Lambda in list comprehension
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x ** 2, numbers))

# Lambda as callback
def process_data(data, callback):
    return callback(data)

result = process_data([1, 2, 3], lambda lst: sum(lst))

# More complex lambda
complex_func = lambda x, y=10: (x + y) * 2 if x > 0 else y


