#Ex.1
class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age

# Step 1: Create cat objects
# cat1 = create the object

# # Step 2: Create a function to find the oldest cat
# def find_oldest_cat(cat1, cat2, cat3):
#     # ... code to find and return the oldest cat ...
#     cats = [cat1, cat2, cat3]
#     oldest = cats[0]
#     for cat in cats[1:]:
#         if cat.age > oldest.age:
#             oldest = cat
#     return oldest

def find_oldest_cat(cat1, cat2, cat3):
    return max(cat1, cat2, cat3, key=lambda cat: cat.age)

# Step 3: Print the oldest cat's details
cat1 = Cat('A', 5)
cat2 = Cat('B', 7)
cat3 = Cat('C', 9)

print(find_oldest_cat(cat1, cat2, cat3).name)

#Ex.2
class Dog:
    def __init__(self, dog_name, dog_height):
        self.name = dog_name
        self.height = dog_height    
    
    def bark(self):
       print(f'{self.name} goes woof!')

    def jump(self):
       print(f'{self.name} jumps {self.height*2} cm high!')

davids_dog = Dog('Hruy', 30)
sarahs_dog = Dog('Mooo', 50)
dogs_list = [davids_dog, sarahs_dog]

print(davids_dog.name, davids_dog.height)
print(sarahs_dog.name, sarahs_dog.height)

for each_dog in dogs_list:
    each_dog.bark()

if davids_dog.height > sarahs_dog.height:
    print(f'{davids_dog.name} higher than {sarahs_dog.name}')
else:
    print(f'{sarahs_dog.name} higher than {davids_dog.name}')

#Ex.3    
class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)

stairway = Song([
    "There’s a lady who's sure",
    "all that glitters is gold",
    "and she’s buying a stairway to heaven"
])

stairway.sing_me_a_song()

#Ex.4
class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []

    def add_animal(self, new_animal):
        if new_animal not in self.animals:
            self.animals.append(new_animal)
            print(f"{new_animal} added to the zoo.")
        else:
            print(f"{new_animal} is already in the zoo.")

    def get_animals(self):
        if not self.animals:
            print("The zoo has no animals.")
        else:
            print("Animals in the zoo:")
            for animal in self.animals:
                print(animal)

    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
            print(f"{animal_sold} has been sold.")
        else:
            print(f"{animal_sold} is not in the zoo.")

    def sort_animals(self):
        self.animals.sort()
        grouped = {}
        for animal in self.animals:
            first_letter = animal[0].upper()
            if first_letter not in grouped:
                grouped[first_letter] = []
            grouped[first_letter].append(animal)
        return grouped

    def get_groups(self):
        grouped_animals = self.sort_animals()
        for letter, group in grouped_animals.items():
            print(f"{letter}: {group}")

my_zoo = Zoo("My zoo")

# Добавляем животных
my_zoo.add_animal("Lion")
my_zoo.add_animal("Zebra")
my_zoo.add_animal("Bear")
my_zoo.add_animal("Baboon")
my_zoo.add_animal("Cougar")
my_zoo.add_animal("Cat")
my_zoo.add_animal("Giraffe")

# Пробуем добавить дубликат
my_zoo.add_animal("Lion")  # Не добавится второй раз

print("\n📋 Список животных:")
my_zoo.get_animals()

# Продаём животное
print("\n💸 Продажа животного:")
my_zoo.sell_animal("Zebra")

print("\n📋 Список животных после продажи:")
my_zoo.get_animals()

# Группируем животных
print("\n📦 Группировка животных:")
my_zoo.get_groups()
