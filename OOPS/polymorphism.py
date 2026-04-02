class Animal:
    def speak(self):
        return "Animal makes their own sounds."

class Dog(Animal):
    def speak(self):
        return "wooff woff"
class Cat(Animal):
    def speak(self):
        return "meaow meaow!"
class Tiger(Animal):
    def speak(self):
        return "Roar!"
class Human(Animal):
    def speak(self):
        return "shout!"
    
dog=Dog()
human = Human()
tiger= Tiger()
cat = Cat()

print("the dog speak like :", dog.speak())
print("the cat speak like :", cat.speak())
print("the tiger speak like :", tiger.speak())
print("the human speak like :", human.speak())

animals = [Dog(),Cat(),Tiger(),Human() ]
for animal in animals:
    print("These are the animals speaks :",animal.speak())
