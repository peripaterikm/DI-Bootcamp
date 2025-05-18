class Dog:

    def __init__(self, name, color, breed, age):
        self.name = name
        self.color = color
        self.breed = breed
        self.age = age    

    def bark(self):
        print(f'{self.name} is barking')     

    def rename(self, name):
        self.name = name
        print(f'New dog"s name is {name}')
        return self

#An instance (or object) of class Dog is created
shelter_dog = Dog('Rex', 'black', 'shelter', 5)

husky_dog = Dog('Boby', 'grey', 'husky', 9)
print(husky_dog.name, husky_dog.color, husky_dog.age)

husky_dog.bark()
husky_dog.rename('Barker')





# Что делали в классе
#OOP: OBJECT ORIENTED PROGRAMING

#WHAT IS AN OBJECT?
#WHAT IS A CLASS?

#HOW TO CREATE A CLASS

class Dog:

    # Creating attributes for all instances
    def __init__(self, name, color, breed, age):
        print('creating object')
        self.name = name
        self.color = color
        self.breed = breed
        self.age = age

    #how to create methods of the class
    def bark(self):
        print(f'{self.name} is barking')

    def walk(self, meters):
        print(f'{self.name} is walking {meters} meters')

    def birthday(self):
        self.age += 1
        return self
    
    def rename(self, name):
        self.name = name
        return self


#An instance (or object) of class Dog is created:
# shelter_dog = Dog()

# Creating attributes of the specific instance
# shelter_dog.color = 'Black'
# print(shelter_dog.color)

# pitbull = Dog()
# print(pitbull.color)

#creating the instances of Dog after creating the __ini__() method:
shelter_dog = Dog('Rex', 'black', 'shelter', 5)
print(shelter_dog.__dict__)
print(shelter_dog.age)
shelter_dog.birthday()
print(shelter_dog.age)
shelter_dog.rename('Toto')
print(shelter_dog.name)



# #create two objects(instances) of the class Dog
# husky_dog = Dog('boby', 'grey', 'husky', 9)
# print(husky_dog.name, husky_dog.color, husky_dog.age)

# puddle_dog = Dog('Flufy', 'white', 'puddle', 2)

# puddle_dog.walk(500)
# puddle_dog.bark()
# husky_dog.bark()

# my_dogs = [shelter_dog, husky_dog]
# print(my_dogs)

# for dog in my_dogs:
#     print(dog.name)

# for dog in my_dogs:
#     dog.bark()

# # print(type(husky_dog))

# # print(help(str))

# accessing a list of all the objects created in a class:
# my_dogs_objects = [obj for obj in globals().values() if isinstance(obj, Dog)]

# print(my_dogs_objects)
