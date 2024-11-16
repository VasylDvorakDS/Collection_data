

from pymongo import MongoClient
import json
from pprint import pprint

# создание экземпляра клиента
client = MongoClient('mongodb://localhost:27017/')

# подключение к базе данных и коллекции
db = client['books']
collection = db['books_db']

# вывод первой записи в коллекции
all_docs = collection.find()

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

number = int(input("Введите сколько записей с базы данных вывести: "))
if number>1:
    for doc in all_docs:
        pretty_json = json.dumps(doc, indent=4, default=str, ensure_ascii=False)
        print(pretty_json)
        number=number-1
        if number==0:
            break

def print_data_in_terminal(docs):
    number=0
    for one_book in docs:
        pretty_json = json.dumps(one_book, indent=4, default=str, ensure_ascii=False)
        print(pretty_json)
        number=number+1
    print("Количество таких книг = ", number)


# Найти все книги количество которых в стоке меньше 3 или больше 10 и также в названии которых содержится артикль the. Вывести их в консоль
query = {"$and":
             [{"$or":[{"In_stock_available" : {"$lt" : 3}},
                    {"In_stock_available" : {"$gt" : 10}}]},
            {"Name": {"$regex": "the"}}]}
books = collection.find(query)
print("Все книги количество которых в стоке меньше 3 или больше 10 и также в названии которых содержится артикль the")
print_data_in_terminal(books)

# Найти книгу "A Summer In Europe", сохранить её в переменную, вывести в терминал, затем удалить из MongoDB, а потом добавить в MongoDB.
query={"Name": "A Summer In Europe"}
book = collection.find_one(query)
print(json.dumps(book, indent=4, default=str, ensure_ascii=False))
collection.delete_one({"Name": "A Summer In Europe"})
collection.insert_one(book)

# Пометить книгу "A Summer In Europe" как "Status":"Мною прочитана"  в MongoDB.
collection.update_one({"Name": "A Summer In Europe"}, {"$set":{"Status":"Мною прочитана"}})

# Поменять Category книги "A Summer In Europe" как "Category":"Action"  в MongoDB.
collection.update_one({"Name": "A Summer In Europe"}, {"$set":{"Category":"Action"}})

# Вывести книгу "A Summer In Europe" в терминал
book = collection.find_one(query)
print(json.dumps(book, indent=4, default=str, ensure_ascii=False))

