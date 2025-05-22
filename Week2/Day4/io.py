import os
# with open("c:\DI-Bootcamp\Week2\Day4\starwars_names.txt", "r") as file:
#     for line in file:
#         print(line.strip())  # strip() убирает лишние переносы строк

# with open("c:\DI-Bootcamp\Week2\Day4\starwars_names.txt", "r") as file:
#     for line in file:
#         output = file.readline()
#         print(output.strip())  # strip() убирает лишние переносы строк

# with open("c:\DI-Bootcamp\Week2\Day4\starwars_names.txt", "r") as file:
#     lines = file.readlines()
#     if len(lines) >= 5:
#         print("5-я строка:", lines[4].strip())
#     else:
#         print("В файле меньше 5 строк.")

dir_path = os.path.dirname(os.path.realpath(__file__))
# with open(f'{dir_path}/starwars_names.txt', "r") as file:
#     for line in file:
#         output = file.readline()
#         print(output.strip())  # strip() убирает лишние переносы строк


# Открываем файл и читаем строки
with open(f'{dir_path}/starwars_names.txt', "r") as file:
    lines = file.readlines()  # список строк

# Удаляем лишние пробелы и делим каждую строку на слова
word_lists = [line.strip().split() for line in lines]

# Печатаем результат
for words in word_lists:
    print(words)

#Append "SkyWalker" next to each first name "Luke"
with open(f'{dir_path}/starwars_names.txt', "r") as file:
    lines = file.readlines()

# Обрабатываем строки
modified_lines = []

for line in lines:
    words = line.strip().split()
    modified_words = []

    for word in words:
        modified_words.append(word)
        if word == "Luke":
            modified_words.append("SkyWalker")  # вставляем сразу после "Luke"

    modified_lines.append(" ".join(modified_words))

# Выводим результат
for line in modified_lines:
    print(line)
