import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['books']
collection = db['books_db']

# Чтение файла JSON
with open('books_library.json', 'r') as file:
    data = json.load(file)

# Функция разделения данных на более мелкие фрагменты
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Разделение данных на фрагменты по 5000 записей в каждом
data_chunks = list(data)
chunk_size = 5
if len(data) > chunk_size:
    data_chunks = list(chunk_data(data, chunk_size))


# Вставка фрагментов в коллекцию MongoDB
for chunk in data_chunks:
    collection.insert_many(chunk)

print("Данные успешно вставлены.")
client.close()