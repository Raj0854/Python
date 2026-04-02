# ABSTRACT BASE CLASS IS A CLASS THAT CANNOT BE INSTANTIATED AND IS DESIGNED TO BE SUBCLASSSED. IT DEFINES A TEMPLATE FOR OTHER CLASSES TO FOLLOW, ENFORCING THE IMPLEMENTATION OF CERTAIN METHODS IN THE SUBCLASSES. IN THIS EXAMPLE, THE ANIMAL CLASS IS AN ABSTRACT BASE CLASS WITH AN ABSTRACT METHOD MOVE(), WHICH IS IMPLEMENTED BY THE SUBCLASSES HUMAN, SNAKE, DOG, AND LION.
from abc import ABC, abstractmethod
class Animal(ABC):# abstract base class

	@abstractmethod
	def move(self):
		pass

class Human(Animal):

	def move(self):
		print("I can walk and run")

class Snake(Animal):

	def move(self):
		print("I can crawl")

class Dog(Animal):

	def move(self):
		print("I can bark")

class Lion(Animal):

	def move(self):
		print("I can roar")

# Driver code
R = Human()
R.move()

K = Snake()
K.move()

R = Dog()
R.move()

K = Lion()
K.move()