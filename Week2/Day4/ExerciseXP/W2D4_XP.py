#Ex.1
import random
import os

def get_words_from_file(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, filename)

    try:
        with open(filepath, "r") as file:
            content = file.read()
            words = content.split()  # разбиваем по пробелам и переносам строк
            return words
    except FileNotFoundError:
        print(f"❌ File '{filepath}' not found.")
        return []

def get_random_sentence(length, filename="words.txt"):
    words = get_words_from_file(filename)
    if not words:
        return "No words to generate sentence."

    sentence_words = [random.choice(words) for _ in range(length)]
    sentence = " ".join(sentence_words).lower()
    return sentence

def main():
    print("📝 This program generates a random sentence of the length you choose (2 to 20 words).")
    user_input = input("Enter the number of words (2–20): ")

    try:
        length = int(user_input)
        if 2 <= length <= 20:
            sentence = get_random_sentence(length)
            print("\nGenerated sentence:")
            print(sentence)
        else:
            print("❗ Please enter a number between 2 and 20.")
    except ValueError:
        print("❗ Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()

#Ex.2
import json

# Step 1: Load the JSON string
sampleJson = """{ 
   "company":{ 
      "employee":{ 
         "name":"emma",
         "payable":{ 
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""

# Преобразуем строку JSON в словарь Python
data = json.loads(sampleJson)

# Step 2: Access the nested “salary” key
salary = data["company"]["employee"]["payable"]["salary"]
print("💰 Salary is:", salary)

# Step 3: Add the “birth_date” key
data["company"]["employee"]["birth_date"] = "1990-05-10"

# Step 4: Save the JSON to a file
with open("modified_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("✅ Modified JSON saved to 'modified_data.json'")
