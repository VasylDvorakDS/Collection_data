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
    city = str(input("Введите название города = "))

    params={
    "query":query,
    "limit":limit,
    "near": city,
    "fields": 'name,location,rating',
    "sort":"RATING"}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        print('\n','СПИСОК МЕСТ:','\n')
        j_data=response.json()
        for item, place in enumerate(j_data.get('results')):
            print(item+1,') Имя заведения: ',place.get('name'))
            print('Адрес заведения:  ', place.get('location').get('formatted_address'))
            print('Рейтинг: ', place.get('rating') if 'rating' in place else "Рейтинг не определялся", '\n')
    else:
        print("Ошибка сервера")




