class Calculator:
    def add(self, x, y=0, z=0, a=0):
        return x * y + z - a

# Using the same method in different ways
calc = Calculator()
print(calc.add(5))        # Output: 5  (only x is provided)
print(calc.add(5, 3))     # Output: 8  (x and y are provided)
print(calc.add(5, 3, 2))  # Output: 10 (all parameters provided)
print(calc.add(5, 3, 2,5))  # Output: 10 (all parameters provided)