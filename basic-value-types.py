# basic value types

# strings: sequence of chars that represents text
# 'Hello, Python'

# strings methods
# print('hello, python'.capitalize())
# print('hello, python'.upper())

# print('Goodnight Moon'.replace('Moon', 'Honey'))

# # 3 STRINGS: SEQUENNCE of chars: IT ALLOWS US TO USE INDEXES (POSITIONS)

# greetings = 'Hello, Python'
# print(greetings[7:13])

# description = "strings are..."
# print(description.upper())
# print(description.replace("are", "is"))
# print(description[0:7])

# # NUMBERS: INTEGER, FLOAT, COMPLEX
# a = 5 #INT
# b = 2.7 #FLOAT
# c = 5+3
# print(c)

# print(5*2)

# user_name = input("What is your name?")
# print(user_name)

# print(3>4)

# #BOOLEANS: 
# print(4 == "4")

# a = 350
# b = 350

# print(a is b)

# Check what is the type of each value, then change it: if it is a string, make it an integer and vice-versa:

bank_balance = '33000'
print(type(int(bank_balance)))
phone_number = 532287514
print(type(str(phone_number)))

#STRING FORMATTING
print(f'your bank balance {bank_balance} therefore you can take a loan.')

#VARIABLES: NAMING
my_address = "Ramat Gan"

#VARIABLES: CONSTANTS
pi = 3.14