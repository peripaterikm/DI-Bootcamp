import string
import re

# 📘 Part I: Analyzing a Simple String
class Text:
    def __init__(self, text):
        self.text = text

    def word_frequency(self, word):
        words = self.text.lower().split()
        count = words.count(word.lower())
        if count > 0:
            return count
        else:
            return f"The word '{word}' was not found."

    def most_common_word(self):
        words = self.text.lower().split()
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        return max(freq, key=freq.get)

    def unique_words(self):
        words = self.text.lower().split()
        return list(set(words))

    # 📄 Part II: Analyzing Text from a File
    @classmethod
    def from_file(cls, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return cls(content)
        except FileNotFoundError:
            print(f"❌ File '{file_path}' not found.")
            return cls("")

# 🧼 Bonus: Text Modification
class TextModification(Text):
    def remove_punctuation(self):
        translator = str.maketrans('', '', string.punctuation)
        cleaned_text = self.text.translate(translator)
        return cleaned_text

    def remove_stop_words(self):
        stop_words = {
            "a", "an", "the", "and", "or", "in", "on", "with", "of", "to",
            "is", "it", "for", "by", "at", "this", "that", "was", "are",
            "as", "but", "from", "be", "has", "have"
        }
        words = self.text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return " ".join(filtered_words)

    def remove_special_characters(self):
        cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', self.text)
        return cleaned_text

sample_text = "This is a test! Let's clean it: remove punctuation, stop words, and special #characters :)"

tm = TextModification(sample_text)

print("🔹 Original text:")
print(tm.text)

print("\n✂️ No punctuation:")
print(tm.remove_punctuation())

print("\n🧹 No stop words:")
print(tm.remove_stop_words())

print("\n🚫 No special characters:")
print(tm.remove_special_characters())

print("\n🔁 Frequency of 'test':", tm.word_frequency("test"))
print("🔥 Most common word:", tm.most_common_word())
print("✨ Unique words:", tm.unique_words())
