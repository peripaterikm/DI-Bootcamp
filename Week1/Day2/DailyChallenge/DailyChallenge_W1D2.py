#Challenge 1: Multiples of a Number
number_list = []
i = 0
user_number = int(input('Input number: '))
user_length = int(input('Input set length: '))
while i < user_length:
    number_list.append(user_number * (i+1))
    i += 1
print(number_list)

#Challenge 2: Remove Consecutive Duplicate Letters
user_string = input('Input string containing consecutive duplicate letters')
unique_chars = ''
unique_chars = user_string[0]
for i in range (1, len(user_string)):
    if user_string[i] != user_string[i-1]:
        unique_chars = unique_chars + user_string[i]
print(unique_chars)