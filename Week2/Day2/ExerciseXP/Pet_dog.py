import random
from XP_W2D2 import Dog

# Новый класс PetDog
class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        dog_names = [self.name] + [dog.name for dog in args]
        print(f"{', '.join(dog_names)} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = [
                "stands on his back legs",
                "shakes your hand",
                "plays dead"
            ]
            trick = random.choice(tricks)
            print(f"{self.name} {trick}")
        else:
            print(f"{self.name} is not trained yet and cannot do a trick.")


# Предполагаем, что класс PetDog уже импортирован или определён в этом файле

# Создаём экземпляры
dog1 = PetDog("Rex", 5, 20)
dog2 = PetDog("Buddy", 3, 15)
dog3 = PetDog("Luna", 4, 18)

# Тестируем train()
print("=== Training Rex ===")
dog1.train()         # Rex is barking, trained = True

# Тестируем play(*args)
print("\n=== Play together ===")
dog1.play(dog2, dog3)  # Rex, Buddy, Luna all play together

# Тестируем do_a_trick()
print("\n=== Try tricks ===")
dog1.do_a_trick()    # Rex does a random trick (т.к. он тренирован)
dog2.do_a_trick()    # Buddy is not trained yet and cannot do a trick
