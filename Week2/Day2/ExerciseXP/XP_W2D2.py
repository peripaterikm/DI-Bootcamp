#Ex.1
class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Siamese(Cat):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def sing(self, sounds):
        return f'{self.name} (Siamese) sings: {sounds}'

# Step 2
bengal_cat = Bengal(name="Leo", age=3)
chartreux_cat = Chartreux(name="Blue", age=5)
siamese_cat = Siamese(name="Mimi", age=2, color="Cream")

all_cats = [bengal_cat, chartreux_cat, siamese_cat]

# Step 3
sara_pets = Pets(all_cats)

# Step 4
sara_pets.walk()


#Ex.2
class Dog():
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
    
    def bark(self):
        return f'{self.name} is barking'

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        if self.run_speed() * self.weight > other_dog.run_speed() * other_dog.weight:
             print(f'{self.name} won!')
        else:
             print(f'{other_dog.name} won!')
        return


# Step 2
dog1 = Dog(name="Hruy", age=3, weight=10)
dog2 = Dog(name="Moo", age=5, weight=15)
dog3 = Dog(name="Scoobeedoo", age=2, weight=20)

all_dogs = [dog1, dog2, dog3]

# вызов метода bark()
print(dog1.bark())      # Hruy is barking
print(dog2.bark())      # Moo is barking
print(dog3.bark())      # Scoobeedoo is barking

# вызов метода run_speed()
print(f'{dog1.name} speed:', dog1.run_speed())   # 10 / 3 * 10 ≈ 33.33
print(f'{dog2.name} speed:', dog2.run_speed())   # 15 / 5 * 10 = 30.0
print(f'{dog3.name} speed:', dog3.run_speed())   # 20 / 2 * 10 = 100.0

# вызов метода fight()
dog1.fight(dog2)   # сравнение по run_speed * weight
dog2.fight(dog3)
dog3.fight(dog1)


#Ex.4
class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = ""

    def is_18(self):
        return self.age >= 18

class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_member = Person(first_name, age)
        new_member.last_name = self.last_name
        self.members.append(new_member)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print(f"No family member named {first_name} was found.")

    def family_presentation(self):
        print(f"Family last name: {self.last_name}")
        for member in self.members:
            print(f"{member.first_name}, {member.age} years old")


# Создаем семью
my_family = Family("Smith")

# Добавляем членов семьи
my_family.born("Alice", 17)
my_family.born("Bob", 21)
my_family.born("Charlie", 15)

# Проверяем, может ли кто-то пойти гулять
print("\n=== Check Majority ===")
my_family.check_majority("Alice")
my_family.check_majority("Bob")

# Показать информацию о семье
print("\n=== Family Presentation ===")
my_family.family_presentation()
