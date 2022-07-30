import os
import yadisk
import requests
from pprint import pprint
with open("TokenVK.txt", "r") as file_tok:
    token = file_tok.read().strip()
class VkUser:
    URL = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }
    def photos_get(self, user_id=None):
        photos_url = self.URL + 'photos.get'
        photos_params = {
            'count': 5,
            'owner_id' : user_id,
            'album_id': 'profile',
            'extended': 1
        }
        res = requests.get(photos_url, params={**self.params, **photos_params})
        return res.json()
oleg = VkUser(token, '5.131')
info = oleg.photos_get()
new_list = []
for all in info['response']['items']:
    date = all['date']
    file_name = (f"{all['likes']['count']} + {all['date']}.jpg")
    for adress in all['sizes']:
        if adress['type'] == 'z':
            photo_url = adress['url']
    new_list.append({'date': date , 'file_name': file_name, 'photo_url': photo_url})
pprint(new_list)

URL = 'https://cloud-api.yandex.net/v1/disk/resources'

with open("Yandex_token.txt", "r") as file_tok:
    token1 = file_tok.read().strip()
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token1}'}
path_to_file = os.path.join(os.getcwd(), 'python1.png')
y = yadisk.YaDisk(token=token1)
def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    requests.put(f'{URL}?path={path}', headers=headers)
create_folder('My_photos')

for photo in new_list:
    r = requests.get(photo['photo_url'])
    with open(photo['file_name'], 'wb') as code:
        a = code.write(r.content)
        try:
            y.upload(photo['file_name'], (f"/My_photos/{photo['file_name']}"))
        except KeyError:
            print(r)
