import requests
from fake_useragent import UserAgent

# proxies = {
#      "http": "http://52.196.1.182:80",
#      "https": "http://52.196.1.182:80"
#  }
headers = {
    "UserAgent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
response = requests.get("https://https://unsplash.com/s/photos/blog",headers=headers)
print(response.status_code)