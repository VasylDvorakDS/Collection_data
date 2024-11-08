import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sympy import pprint

# url='https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
url='https://www.boxofficemojo.com'
ua=UserAgent()
header={"User-Agent":'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}

params={"ref_":"bo_nb_hm_tab"}

session=requests.session()
response=session.get(url+"/intl", params=params, headers=header)
soup=BeautifulSoup(response.text,"html.parser")
#test_link=soup.find("a",{'class':'a-link-normal'})
#print(response.status_code)
rows=soup.find_all('tr')
films=[]
for row in rows[2:-1]:
    film={}
    #area_info=row.find('td',{'class':'mojo-field-type-area_id'}).find('a')
    try:
        area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]
        film['area']=[area_info.getText(), url+area_info.get('href')]
    except:
        film['area']=None
    try:
        weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
        film['weekend'] = [weekend_info.getText(), url +  weekend_info.get('href')]
    except:
        film['weekend']=None
    try:
        film['realeses'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText())
    except:
        film['realeses']=None
    try:
        frelease_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
        film['frelease'] = [frelease_info.getText(), url +  frelease_info.get('href')]
    except:
        film['frelease'] = None

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(), url +  distributor_info.get('href')]
    except:
        print('Exception with frelease, object = ', film['frelease'])
        film['distributor']=None
    try:
        film['gross'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText())
    except:
        film['gross']=None

    films.append(film)

pprint(films)



