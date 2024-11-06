import requests
from pprint import pprint

from Task_1.Task_1_at_home.passwords_kinopoisk import api_key

url = "https://api.kinopoisk.dev/v1.4/movie"

headers = {
    "accept": "application/json",
    "X-API-KEY": api_key
}
while True:
    print()
    genres_name = str(input("Введите название жанра например: драма, комедия, мелодрама, ужасы  = "))
    limit = int(input("Введите лимит запроса от 1 до 250 = "))

    params={"page":1,
            "limit":limit,
            "genres.name":genres_name}
    if (genres_name in ['драма', 'комедия', 'мелодрама', 'ужасы']) & (0<limit<251):

        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            print('\n','СПИСОК ФИЛЬМОВ:','\n')
            j_data=response.json()
            for name in j_data.get('docs'):
                print()
                if (name.get('name') is None) & (name.get('alternativeName') != None):
                    real_name=name.get('alternativeName')
                elif (name.get('alternativeName') is None) & (name.get('name') != None):
                    real_name =name.get('name')
                else: continue
                print('Название фильма: ',real_name)
                print('Рейтинг фильма по imdb: ', name.get('rating').get('imdb'))
                if (name.get('description') is None) & (name.get('shortDescription') != None):
                    real_description=name.get('shortDescription')
                elif (name.get('description') != None) & (name.get('shortDescription') is None):
                    real_description = name.get('description')
                else: real_description = 'Нету описания'
                print('Описание фильма: ',real_description)
        else:
            print("Ошибка сервера")
    else:
        print("Неправильно введён запрос")
