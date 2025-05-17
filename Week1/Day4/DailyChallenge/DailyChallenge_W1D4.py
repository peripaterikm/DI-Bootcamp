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
temp_string = ''
num_rows = len(matrix)
num_cols = len(matrix[0])

for col in range(num_cols):
    for row in range(num_rows):
        temp_string += matrix[row][col]

# Step 4: Заменим все НЕбуквы на пробелы, потом удалим лишние пробелы
filtered = ''
for char in temp_string:
    if char.isalpha():
        filtered += char
    else:
        filtered += ' '

# Step 5: Сжимаем лишние пробелы
decoded_message = ' '.join(filtered.split())

# Step 6: Вывод
print(decoded_message)
