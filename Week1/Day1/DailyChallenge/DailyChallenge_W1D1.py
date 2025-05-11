import random

# 1. Ask for User Input
user_input = input("Enter a string exactly 10 characters long: ")

# 2. Check the Length
if len(user_input) < 10:
    print("String not long enough.")
elif len(user_input) > 10:
    print("String too long.")
else:
    print("Perfect string!")

    # 3. Print first and last characters
    print("First character:", user_input[0])
    print("Last character:", user_input[-1])

    # 4. Build the string character by character
    print("\nBuilding string step by step:")
    for i in range(1, len(user_input) + 1):
        print(user_input[:i])

    # 5. Bonus: Jumble the string
    chars = list(user_input)
    random.shuffle(chars)
    jumbled = ''.join(chars)
    print("\nJumbled string:", jumbled)
