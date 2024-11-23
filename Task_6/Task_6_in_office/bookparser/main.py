# import requests
#
url = "https://cdn21.img.ria.ru/images/139676/19/1396761945_0:0:3303:2840_600x0_80_0_1_19173d1660f765703c0b2c1ac28d9ad6.jpg"
#
# response = requests.get(url)
# with open('owl.jpg', 'wb') as f:
#     f.write(response.content)

import wget

wget.download(url)

