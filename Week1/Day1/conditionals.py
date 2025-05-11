# CONDITIONALS: IF STATEMENTS

# SYNTAX
# if condition:
#     <indented block of code>

# secret_number = 55
# user_number = int(input('Guess a number: '))

# if user_number == secret_number:
#     print('Congrats, you won!')

user_number = int(input('Input a number between 1 and 100: '))

if user_number % 3 == 0 and user_number % 5 == 0:
    print("FizzBuzz")
elif user_number % 3 == 0:
    print("Fizz")
elif user_number % 5 == 0:
    print("Buzz")
else:
    print("The number is not a multiple of 3 or 5.")

