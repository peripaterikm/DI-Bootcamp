import requests
import xml.etree.ElementTree as ET


import requests

url = "https://apis.cbs.gov.il/sdmx-json/data/136.1/CPI-Monthly/ALL"

headers = {
    "Accept": "application/vnd.sdmx.data+json;version=1.0.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Ключи верхнего уровня:", list(data.keys()))
else:
    print("Ошибка:", response.status_code)



# # URL к API CBS
# url = "https://apis.cbs.gov.il/sdmx/data/136.1/CPI-Monthly/ALL"

# # Выполняем GET-запрос
# response = requests.get(url)

# # Проверка ответа
# if response.status_code == 200:
#     # Парсим XML-ответ
#     root = ET.fromstring(response.content)

#     # Пробуем найти значения
#     values = root.findall('.//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs')

#     print("Первые 5 записей:\n")
#     for obs in values[:5]:
#         time = obs.find('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension').attrib.get('value')
#         value = obs.find('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue').attrib.get('value')
#         print(f"Дата: {time}, Значение: {value}")
# else:
#     print(f"Ошибка запроса: {response.status_code}")
