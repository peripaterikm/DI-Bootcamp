#DICTIONARIES
# shopping_list = ['milk', 'eggs', 'bread']
# shopping_list.append ('butter')
# shopping_list.remove ('eggs')
# print(shopping_list)

sample_dict = {
  "name": "Kelly",
  "age":25,
  "salary": 8000,
  "city": "New york"

}
keys_to_remove = ["name", "salary"]

for key in keys_to_remove:
    sample_dict.pop(key) 

print(sample_dict)


#prog from Python instructor
user_a = {
    'first_name': 'Bob',
    'last_name': 'Ross', #STOP HERE, EXPLAIN
    'age': 53, #EXPLAIN DATA TYPES AS VALUES
    'address': 'Tel Aviv', #STOP HERE EXPLAIN ACESSING DATA
    'hobbies': ['painting', 'guitar'], #STOP HERE EXPLAIN DATA TYPES: DICTS AND LISTS
    'pets': [('Rufus', 9), ('Garfield', 8), ('Katty', 6)], #EXPLAIN LIST OF OTHER DATA TYPES (EX.:TUPPLES) 
    'family': {'partner':{
        'first_name': 'Lior', 
        'last_name': 'Alon', 
        'age': 50
        },
'sports': ['volleyball', 'soccer']
        },
    }
}
#print(user_a['first_name'])
#print(user_a['hobbies'][1])
#print(user_a['pets'][2][0])

# for pet in user_a['pets']:
#     print(pet[0])

# print(user_a['family']['partner']['last_name'])
# print(user_a['family']['children']['sports'][0])
# print(user_a['family'])


user_a['first_name'] = 'John'

user_a['pets'][2][0] = 'Garfield_2'

print(user_a)