#Ex.1
my_fav_numbers = {3, 7, 16}
my_fav_numbers.update ([5, 1])
print(my_fav_numbers)

my_fav_numbers.remove (1)
print(my_fav_numbers)

friend_fav_numbers = {2, 4, 8}
our_fav_numbers = my_fav_numbers | friend_fav_numbers
print(our_fav_numbers)

#Ex.2
my_tuple = (1, 2, 3)
#my_tuple.append(4) #impossible to fulfil the operation because tuples are immutable

#Ex.3
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")
apples = basket.count("Apples")
print("Apples appear", apples, "times.")
basket.clear()
print(basket)

#Ex.4
i = 0
list1 = []
while i<8:
    x = 1.5 + 0.5*i
    if x % 1 == 0:
        list1.append (int(x))
    else: list1.append (x)
    i = i + 1
print(list1)

#Ex.5
for i in range(1,21):
    print(i)

for i in range(1,21):
    if i % 2 == 0:
        print(i)

#Ex.6
user1 = ''
while user1 != "Mark":
    user1 = input()
print('Hi, Mark!')

#Ex.7
fav_fruits_input = input("Enter your favorite fruits (separated by spaces): ")

favorite_fruits = fav_fruits_input.split()

chosen_fruit = input("Enter the name of any fruit: ")

if chosen_fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

#Ex.8
user_choice = ''
toppings = []
while user_choice != 'quit':
    user_choice = input("Enter pizza topping: ")
    if user_choice != 'quit':
        print(f"Adding {user_choice} to your pizza.")
        toppings.append(user_choice)
print('You have chosen the following toppings: ', toppings)    
print('The total cost of the pizza:', 10 + 2.5*len(toppings) )

#Ex.9
total_cost = 0
ages = []

num_people = int(input("How many people in your family want to buy a ticket? "))

for i in range(num_people):
    age = int(input(f"Enter age of person #{i + 1}: "))
    ages.append(age)

    if age < 3:
        cost = 0
    elif 3 <= age <= 12:
        cost = 10
    else:
        cost = 15

    total_cost += cost

print(f"Total ticket cost for your family: ${total_cost}")

#Ex.9 bonus
teenagers_list = ['David', 'Solomon', 'Shaul', 'Amenhothep']
allowed_list = []
for i in range(len(teenagers_list)):
     age = int(input(f"Enter age of person #{i + 1}: "))
     if age > 16 and age < 21:
        allowed_list.append(teenagers_list[i])
print(allowed_list)

#Ex.10
sandwich_orders = ["Tuna", "Pastrami", "Avocado", "Pastrami", "Egg", "Chicken", "Pastrami"]
finished_sandwiches = []

while "Pastrami" in sandwich_orders:
    sandwich_orders.remove("Pastrami")

while len(sandwich_orders) > 0:
    current_sandwich = sandwich_orders.pop(0)
    print(f"I made your {current_sandwich} sandwich.")
    finished_sandwiches.append(current_sandwich)

print("\nFinished sandwiches:", finished_sandwiches)