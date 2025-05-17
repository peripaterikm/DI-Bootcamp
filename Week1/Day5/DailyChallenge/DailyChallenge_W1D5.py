# Ex.1
# Step 1: Get Input
input_string = input("Enter words separated by commas: ")

# Step 2: Split the String into a list
words = input_string.split(',')

# Step 3: Sort the list alphabetically
words.sort()

# Step 4: Join the list back into a comma-separated string
sorted_string = ','.join(words)

# Step 5: Output the result
print("Sorted words:", sorted_string)

# Ex.2
def longest_word(sentence):
    # Step 2: Split the Sentence into Words
    words = sentence.split()

    # Step 3: Initialize Variables
    longest = ""
    max_length = 0

    # Step 4: Iterate Through the Words
    for word in words:
        # Step 5: Compare Word Lengths
        if len(word) > max_length:
            longest = word
            max_length = len(word)

    # Step 6: Return the Longest Word
    return longest

print(longest_word(input('Input sentence: ')))