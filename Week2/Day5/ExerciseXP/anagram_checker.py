import os

class AnagramChecker:
    def __init__(self, word_list_file="sowpods.txt"):
        base_path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_path, word_list_file)

        try:
            with open(filepath, 'r') as file:
                self.word_list = [word.strip().lower() for word in file if word.strip().isalpha()]
        except FileNotFoundError:
            print(f"❌ File '{filepath}' not found.")
            self.word_list = []

    def is_valid_word(self, word):
        return word.lower() in self.word_list

    def get_anagrams(self, word):
        word = word.lower()
        return [w for w in self.word_list if self.is_anagram(word, w) and w != word]

    def is_anagram(self, word1, word2):
        return sorted(word1) == sorted(word2)
