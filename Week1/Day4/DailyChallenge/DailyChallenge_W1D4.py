# MATRIX_STR = '''
# 7ii
# Tsx
# h%?
# i #
# sM 
# $a 
# #t%'''       

# rows = MATRIX_STR.strip().split('\n')
# matrix = []
# for row in rows:
#     matrix.append(list(row))

# print(matrix)

MATRIX_STR = '''
7ii
Tsx
h%?
i #
sM 
$a 
#t%'''       

# Step 1
rows = MATRIX_STR.strip().split('\n')
matrix = []
for row in rows:
    matrix.append(list(row))

# Step 2–3: Читаем по столбцам
raw_message = ''
num_rows = len(matrix)
num_cols = len(matrix[0])

for col in range(num_cols):
    for row in range(num_rows):
        raw_message += matrix[row][col]

# Step 4: Заменим все НЕбуквы на пробелы, потом удалим лишние пробелы
filtered = ''
for char in raw_message:
    if char.isalpha():
        filtered += char
    else:
        filtered += ' '

# Step 5: Сжимаем лишние пробелы
decoded_message = ' '.join(filtered.split())

# Step 6: Вывод
print(decoded_message)
