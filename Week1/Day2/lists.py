#LISTS

# A list is a sequence of elements
some_list = list('item 1') # to convert other sequence to a list
other_list = ['item 1'] # the best way ti create an empty list

print(some_list)
print(other_list)

print(len(some_list))
print(some_list[1])

my_list = []
my_list.append('A')
print(my_list)

my_list.extend(['B', 'C',  'D'])
print(my_list)

#create empty list and add 4 names of you favourite charachters
heroes_names = []
heroes_names.append ('Karlson')
heroes_names.append ('Sherlock')
heroes_names.extend (['Tirion', 'Arya'])
print(heroes_names)

fruits = ['apple', 'banana', 'cherry']
fruits.insert(1, 'orange')
fruits.sort
print(fruits)

for i in range(5):
    print(i)

list1 = [5, 10, 15, 20, 25, 50, 20] 
for i in range(len(list1)):
    if list1[i] == 20:
        list1[i] = 200
print(list1)

# заменим только первое вхождение
list1 = [5, 10, 15, 20, 25, 50, 20] 
list1[list1.index(20)] = 200
print(list1)

