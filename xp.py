#Ex.1
print(("Hello world\n" * 4).strip())

#Ex.2
print((99 ** 3) * 8)

#Ex.3
#>>> 5 < 3
#false

#>>> 3 == 3
#true

#>>> 3 == "3"
#false

#>>> "3" > 3
#false

#>>> "Hello" == "hello"
#false

#Ex.4
computer_brand = "Asus"
print(f"I have a {computer_brand} computer.")

#Ex.5
name = "Mark"
age = 44
shoe_size = 41

info = f"My name is {name}, I am {age} years old, and my shoe size is {shoe_size}."
print(info)

#Ex.6
a = 4
b = 1
if a > b:
    print('Hello World')

#Ex.7
a = int(input())
if a % 2 == 0:
    print('even')
else:
    print('odd')

#Ex.8
user_name = input()
if user_name == 'Mark':
    print('Hello, namesake!')
else:
    print(f"Hello, {user_name}. You've got rare name!")

#Ex.9
height = int(input("Enter your height in centimeters: "))

if height > 145:
    print("You are tall enough to ride!")
else:
    print("You need to grow some more to ride.")
