
class Animal:
    def __init__(self, name, family, legs):
        self.name = name
        self.family = family
        self.legs = legs
        self.full_name = f'{name} {family}'




class Dog(Animal):
    def __init__(self, name, family, legs, trained, age):
        super().__init__(name, family, legs)  # вызываем конструктор родителя
        self.trained = trained
        self.age = age

    def bark(self):
        print(f'A {self.name} is barking')

    def sleep(self):
        return f'{self.name} is sleeping - from the Dog class'

dog1 = Dog(name="Rex", family="Shepherd", legs=4, trained=True, age=3)


print(dog1.name)        # Rex
print(dog1.family)      # Shepherd
print(dog1.legs)        # 4
print(dog1.full_name)   # Rex Shepherd
print(dog1.trained)     # True
print(dog1.age)         # 3

dog1.bark()             # A Rex is barking
print(dog1.sleep())     # Rex is sleeping - from the Dog class
