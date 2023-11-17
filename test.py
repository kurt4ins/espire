import requests
from pprint import pprint
ans = requests.get('https://suggest-maps.yandex.ru/v1/suggest?apikey=781f59c0-5f81-470b-a396-9c28b38e3fe8&text=омск&ll=37.37, 55.55')
pprint(ans.json())