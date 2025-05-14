#Ex.1

def display_message():
    print('I am learning about functions in Python.')

display_message()

#Ex.2
def favorite_book(title):
    print(f'One of my favorite books is {title}')

favorite_book("Alice in Wonderland")

#Ex.3
def describe_city(city, country = 'Unknown'):
    print(f'{city} is in {country}')

describe_city('TA', 'Israel')

#Ex.4
import random
def guess_random_number(user_number):
    dice = random.randint(1, 100)
    if user_number == dice:
        print(f'Success! It is {user_number}')
    else:
        print(f'Fail! Your number: {user_number} , Random number: {dice}')
    
guess_random_number(3)

#Ex.5
def make_shirt(size, text = "I love Python"):
    print(f'The size of the shirt is {size} and the text is {text}')

make_shirt('large')
make_shirt('medium')
make_shirt(size = 'small', text = "Custom message")
make_shirt(size = 'small', text = "Hello!")

#Ex.6
magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel']
def show_magicians(magician_names):
    for name in magician_names:
        print(name)

show_magicians(magician_names)

def make_great(magician_names):
    for i in range(len(magician_names)):
        magician_names[i] = magician_names[i] + 'the Great '
        print(magician_names[i])

make_great(magician_names)

#Ex.7
import random
def get_random_temp():
    return random.randint(-10, 40)

def main():
    current_temp = get_random_temp()
    print(f'The temperature right now is {current_temp} degrees Celsius.')
    if current_temp < 0:
        print('Brrr, that’s freezing! Wear some extra layers today.')
    elif current_temp >= 0 and current_temp < 16:
        print('Quite chilly! Don’t forget your coat.')
    elif current_temp >= 16 and current_temp < 23:
        print('Nice weather.')
    elif current_temp >= 24 and current_temp < 32:
        print('A bit warm, stay hydrated.')
    elif current_temp >= 32 and current_temp < 40:
        print('It’s really hot! Stay cool.')

main()

#Ex.7 bonus (step 4)
import random
def get_random_temp():
    return round(random.uniform(-10, 40), 1)

def main():
    current_temp = get_random_temp()
    print(f'The temperature right now is {current_temp} degrees Celsius.')
    if current_temp < 0:
        print('Brrr, that’s freezing! Wear some extra layers today.')
    elif current_temp >= 0 and current_temp < 16:
        print('Quite chilly! Don’t forget your coat.')
    elif current_temp >= 16 and current_temp < 23:
        print('Nice weather.')
    elif current_temp >= 24 and current_temp < 32:
        print('A bit warm, stay hydrated.')
    elif current_temp >= 32 and current_temp < 40:
        print('It’s really hot! Stay cool.')

main()

#Ex.7 bonus 2 (step 5)
import random

def get_random_temp(season):
    if season == "winter":
        return round(random.uniform(-10, 10), 1)
    elif season == "spring":
        return round(random.uniform(10, 20), 1)
    elif season == "summer":
        return round(random.uniform(20, 40), 1)
    elif season == "autumn":
        return round(random.uniform(5, 20), 1)
    else:
        print("Unknown season. Using default range (-10 to 40).")
        return round(random.uniform(-10, 40), 1)

def main():
    season = input("Enter the season (winter, spring, summer, autumn): ").lower()
    current_temp = get_random_temp(season)
    
    print(f'The temperature right now is {current_temp}°C.')

    if current_temp < 0:
        print('Brrr, that’s freezing! Wear some extra layers today.')
    elif 0 <= current_temp < 16:
        print('Quite chilly! Don’t forget your coat.')
    elif 16 <= current_temp <= 23:
        print('Nice weather.')
    elif 24 <= current_temp < 32:
        print('A bit warm, stay hydrated.')
    elif 32 <= current_temp <= 40:
        print('It’s really hot! Stay cool.')

main()
