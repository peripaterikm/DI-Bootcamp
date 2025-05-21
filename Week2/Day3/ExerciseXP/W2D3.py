#Ex.1
class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __str__(self):
        return f"{self.amount} {self.currency}s"

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.amount

    def __add__(self, other):
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(f"Cannot add between Currency type <{self.currency}> and <{other.currency}>")
            return self.amount + other.amount
        elif isinstance(other, (int, float)):
            return self.amount + other
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'Currency' and '{type(other).__name__}'")

    def __iadd__(self, other):
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(f"Cannot add between Currency type <{self.currency}> and <{other.currency}>")
            self.amount += other.amount
        elif isinstance(other, (int, float)):
            self.amount += other
        else:
            raise TypeError(f"Unsupported operand type(s) for +=: 'Currency' and '{type(other).__name__}'")
        return self

c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

print(str(c1))      # '5 dollars'
print(int(c1))      # 5
print(repr(c1))     # '5 dollars'

print(c1 + 5)       # 10
print(c1 + c2)      # 15
print(c1)           # 5 dollars

c1 += 5
print(c1)           # 10 dollars

c1 += c2
print(c1)           # 20 dollars

#print(c1 + c3)      # ❌ вызовет TypeError

#Ex.3
import string
import random

all_letters = string.ascii_letters  # включает и строчные, и заглавные буквы: abc...ABC...
random_string = ""
for _ in range(5):
    random_string += random.choice(all_letters)

print("Generated string:", random_string)

#Ex.4
# Step 1: Import the datetime module
import datetime

# Step 2 + 3: Create a function to get and display the current date
def show_current_date():
    today = datetime.date.today()
    print("Today's date is:", today)

# Пример вызова
show_current_date()

#Ex.5
import datetime

def time_until_new_year():
    # Step 2: текущая дата и время
    now = datetime.datetime.now()
    
    # Step 3: создаём объект для 1 января следующего года
    next_year = now.year + 1
    jan_first = datetime.datetime(year=next_year, month=1, day=1)
    
    # Step 4: разница между 1 января и текущим моментом
    time_left = jan_first - now

    # Step 5: выводим результат
    print("Time left until January 1st:")
    print(time_left)

# Пример вызова
time_until_new_year()

#Ex.6
from datetime import datetime

def minutes_lived(birthdate_str):
    # Step 1: Преобразуем строку в объект datetime
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")  # можно заменить формат при необходимости

    # Step 2: Получаем текущие дату и время
    now = datetime.now()

    # Step 3: Вычисляем разницу
    difference = now - birthdate

    # Step 4: Переводим разницу в минуты
    minutes = round(difference.total_seconds() / 60)

    # Step 5: Выводим результат
    print(f"You have lived approximately {minutes} minutes.")

# Пример вызова
minutes_lived("1990-05-01")

#Ex.7
#pip install faker

# Step 2: Импортируем модуль faker
from faker import Faker

# Step 3: Пустой список для пользователей
users = []

# Step 4: Функция генерации пользователей
def generate_users(count):
    fake = Faker()
    for _ in range(count):
        user = {
            "name": fake.name(),
            "address": fake.address(),
            "language_code": fake.language_code()
        }
        users.append(user)

# Step 5: Вызываем функцию и печатаем результат
generate_users(5)  # например, сгенерировать 5 пользователей

for user in users:
    print(user)
    print("------")
