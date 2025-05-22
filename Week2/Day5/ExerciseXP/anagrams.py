from anagram_checker import AnagramChecker

def clean_input(user_input):
    return user_input.strip()

def is_single_alpha_word(word):
    return word.isalpha() and " " not in word

def main():
    checker = AnagramChecker()

    while True:
        print("\n--- Anagram Checker ---")
        print("1. Enter a word")
        print("2. Exit")
        choice = input("Choose an option (1 or 2): ")

        if choice == '2':
            print("Goodbye!")
            break
        elif choice == '1':
            user_word = input("Enter a word: ")
            word = clean_input(user_word)

            if not is_single_alpha_word(word):
                print("❗ Please enter only a single word with letters only.")
                continue

            print(f"\nYOUR WORD : \"{word.upper()}\"")

            if checker.is_valid_word(word):
                print("This is a valid English word.")
                anagrams = checker.get_anagrams(word)
                if anagrams:
                    print("Anagrams for your word:", ", ".join(anagrams))
                else:
                    print("No anagrams found.")
            else:
                print("This is NOT a valid English word.")
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
