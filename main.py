import os
import yadisk
import requests
from pprint import pprint
with open("TokenVK.txt", "r") as file_tok:
    token = file_tok.read().strip()
class VkUser:
    URL = 'https://api.vk.com/method/'
    def __init__(self, token, version, owner_id=None):
        self.params = {
            'access_token': token,
            'v': version,
            'owner_id': owner_id
        }
    def photos_get(self, owner_id, count=5, offset=0):
        photos_url = self.URL + 'photos.get'
        photos_params = {
            'count': count,
            'owner_id': owner_id,
            'offset': offset,
            'album_id': 'profile',
            'extended': 1
        }
        res = requests.get(photos_url, params={**self.params, **photos_params})
        return res.json()
user_ID = int(input("Введите ID пользователя: "))
count_photos = int(input('Введите количество фотографий: '))
user = VkUser(token, '5.131', user_ID)
if count_photos > 1000:
    counter = int(count_photos / 1000)
    for i in range(0, counter+1):
        offset = i
        info = user.photos_get(user_ID, 1000, offset)
else:
        info = user.photos_get(user_ID, count_photos)

# info = user.photos_get(user_ID, count_photos)
new_list = []
for all in info['response']['items']:
    date = all['date']
    file_name = (f"{all['likes']['count']} + {all['date']}.jpg")
    best = all['sizes'][-1]
    photo_url = best['url']
    new_list.append({'date': date, 'file_name': file_name, 'photo_url': photo_url})
pprint(new_list)

URL = 'https://cloud-api.yandex.net/v1/disk/resources'

with open("Yandex_token.txt", "r") as file_tok:
    token1 = file_tok.read().strip()
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token1}'}
y = yadisk.YaDisk(token=token1)
def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    requests.put(f'{URL}?path={path}', headers=headers)
create_folder(user_ID)

for photo in new_list:
    r = requests.get(photo['photo_url'])
    with open(photo['file_name'], 'wb') as code:
        a = code.write(r.content)
        try:
            y.upload(photo['file_name'], (f"/{user_ID}/{photo['file_name']}"))
        except KeyError:
            print(r)
