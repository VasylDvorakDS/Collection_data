import requests
from lxml import html
from pymongo import MongoClient

def insert_to_db(list_movies):
    client=MongoClient('mongodb://localhost:27017')
    db =client['imdb_movies']
    collection=db['top_100_movies']
    collection.insert_many(list_movies)
    client.close()
    
def get_titlemeter(list_element):
    try:
        return(list_element[0].split()[-1])
    except:
        return "no change"
    
def get_position_change(list_element):
    try:
        return(int(list_element[0].strip()[:-1]))
    except:
        return 0



resp =requests.get(url='https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm', headers={'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})

tree=html.fromstring(html=resp.content)

movies=tree.xpath('//table[@data-caller-name="chart-moviemeter"]/tbody/tr')


all_movies=['mongodb://localhost:27017']

for movie in movies:
    m={
    'name' : movie.xpath( ".//td[@class='titleColumn']/a/text()" )[ 0],
    'release_year' : int(movie.xpath( ".//td/span[@class='secondaryInfo']/text()" )[0][1:-1]),
    'position' : int(movie.xpath( ".//td/div[@class='velocity']/text()" )[0].split()[0]),
    'titlemeter' : get_titlemeter(movie.xpath( ".//span[contains(@class, 'global-spritetitlemeter')]/@class" )),
    'position_change' : get_position_change(movie.xpath( ".//div/span[@class='secondaryInfo']/text()[2]" ))
    }
    all_movies.append(m)
 
insert_to_db(all_movies)


