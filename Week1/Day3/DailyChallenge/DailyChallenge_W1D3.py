# #Challenge 1
# user_word = input('Enter a word: ')
# letter_indices = {}
# i = 0
# for i in range(len(user_word)):
#     letter = user_word[i]
#     if letter in letter_indices:
#         letter_indices[letter].append(i)
#     else:
#         letter_indices[letter] = [i]
# print(letter_indices)

#Challenge 2
# 1. Данные: товары и кошелёк
items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}

wallet = "$300"

# Очищаем и преобразуем строку с деньгами в целое число
wallet_string = wallet.replace("$", "").replace(",", "")
wallet_amount = int(wallet_string)

# Создаём новый словарь с ценами как числа
cleaned_items = {}
for item, price in items_purchase.items():
    cleaned_price = int(price.replace("$", "").replace(",", ""))
    cleaned_items[item] = cleaned_price

# Проверяем, что подходит по цене 
affordable_items = []
for item, price in cleaned_items.items():
    if price <= wallet_amount:
        affordable_items.append(item)

if not affordable_items:
    print("Nothing")
else:
    print(sorted(affordable_items))

# #Challenge 1b
# user_word = input('Enter a word: ')
# out_dict = {}

# for i, char in enumerate(user_word):
#     if char in out_dict:
#         out_dict[char].append(i)
#     else:
#         out_dict.update({char : [i]})
    
# print(out_dict)