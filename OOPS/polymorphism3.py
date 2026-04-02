class Shape:
    def calculate_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def calculate_area(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_area(self):
        return 3.14 * self.radius * self.radius

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def calculate_area(self):
        return self.side * self.side

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height= height
    
    def calculate_area(self):
        return 0.5 * self.base * self.height
        

# Using polymorphism
rectangle = Rectangle(5, 4)
circle = Circle(3)
square = Square(4)
triangle = Triangle(10,7)

# Same method name, different calculations
print(rectangle.calculate_area())  # Output: 20
print(circle.calculate_area())     # Output: 28.26
print(square.calculate_area())     # Output: 16
print(triangle.calculate_area())     # Output: 16

# We can also use a list
shapes = [Rectangle(5, 4), Circle(3), Square(4),  Triangle(10,7)]
for shape in shapes:
    print(f"Area: {shape.calculate_area()}")