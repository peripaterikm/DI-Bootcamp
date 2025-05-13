#Ex.1
keys = {'Ten': 10, 'Twenty': 20, 'Thirty': 30}
print(keys)
#values = [10, 20, 30]

#Ex.2
family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}
cost_for_family = 0
for name, age in family.items():
    if age < 3:
        print(name, ' ticket price - ', 0)
    elif age >=3 and age<=12:
        cost_for_family = cost_for_family + 10
        print(name, ' ticket price  - ', 10)
    else:
        cost_for_family = cost_for_family + 15
        print(name, ' ticket price  - ', 15)

print("Total family price: ", cost_for_family)

#Ex.2 bonus
family = {}
cost_for_family = 0

num_members = int(input("How many family members? "))

for i in range(num_members):
    name = input(f"Enter name of family member #{i + 1}: ")
    age = int(input(f"Enter age of {name}: "))
    family[name] = age

print("\nTicket Prices:")

for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15

    cost_for_family += price
    print(f"{name} (age {age}) - ticket price: ${price}")

print("\nTotal family price:", cost_for_family)

# Ex.3
brand = {'name': 'Zara', 'creation_date': 1975, 'creator_name': 'Amancio Ortega Gaona', 
             'type_of_clothes': ['men', 'women', 'children', 'home'], 'international_competitors': ['Gap', 'H&M', 'Benetton'],
             'number_stores': 7000, 'major_color': {'France': 'blue', 'Spain': 'red', 'US': ['pink', 'green']}}

# Change the value of number_stores to 2.
brand['number_stores'] = 2

# Print a sentence describing Zara’s clients using the type_of_clothes key.

print(f'Clients can find in Zara clothes for', brand['type_of_clothes'][2])

# Add a new key country_creation with the value Spain.
brand['country_creation'] = 'Spain'

# Check if international_competitors exists and, if so, add “Desigual” to the list.
if brand['international_competitors']: 
    brand['international_competitors'].append('Desigual')

# Delete the creation_date key.
del brand['creation_date']

# Print the last item in international_competitors.
print(brand['international_competitors'][len(brand['international_competitors'])-1])

# Print the major colors in the US.
print(brand['major_color']['US'])

# Print the number of keys in the dictionary.
print(len(brand))

# Print all keys of the dictionary.
print(brand.keys())

#Ex.3 bonus
#Create another dictionary called more_on_zara with creation_date and number_stores. 
#Merge this dictionary with the original brand dictionary and print the result.
more_on_zara = {'creation_date': 1975, 'number_stores': 7000}
brand.update(more_on_zara)
print(brand)

#Ex.4

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

user_dict = {}
#1. Create a dictionary that maps characters to their indices:
# {"Mickey": 0, "Minnie": 1, "Donald": 2, "Ariel": 3, "Pluto": 4}

i = 0
for name in users:
    user_dict[name] = i
    i += 1
print(user_dict)

#2. Create a dictionary that maps indices to characters:
#{0: "Mickey", 1: "Minnie", 2: "Donald", 3: "Ariel", 4: "Pluto"}

user_dict = {}
i = 0
for i in range(len(users)):
    user_dict[i] = users[i]

print(user_dict)

#3. Create a dictionary where characters are sorted alphabetically and mapped to their indices:
#{"Ariel": 0, "Donald": 1, "Mickey": 2, "Minnie": 3, "Pluto": 4}

user_dict = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]
sorted_users = sorted(user_dict)

# Создаём словарь: имя → индекс
alphabetical_dict = {}

for i in range(len(sorted_users)):
    alphabetical_dict[sorted_users[i]] = i

print(alphabetical_dict)