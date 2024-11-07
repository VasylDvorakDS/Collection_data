import requests
from pprint import pprint

from Task_1.Task_1_at_home.password_foursquare import api_key

url = "https://api.foursquare.com/v3/places/search"

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

while True:
    print()
    query = str(input("Введите заведение, которое хотите найти = "))
    limit = int(input("Введите лимит запроса от 1 до 50 = "))

    params={
    "query":query,
    "limit":limit,
    "sort":"RATING"}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        print('\n','СПИСОК МЕСТ:','\n')
        j_data=response.json()
        for item, place in enumerate(j_data.get('results')):
            print('Имя заведения: ',place.get('name'))
            print('Рейтинг: ', item+1)
            print('Адрес заведения:  ', place.get('location').get('formatted_address'),'\n')
    else:
        print("Ошибка сервера")




