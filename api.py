import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
# отправляем запрос и получаем статус

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
# обхявили переменную result
        result = ""
# берем эту конструкцию, если файл json не будет читаться
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
# отправляем запрос и получаем статус
        res = requests.get(self.base_url + 'api/pets/', headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_api_pets(self, auth_key, name: str, animal_type: str, age: str, pet_photo: str):
        photo = os.path.abspath(pet_photo)
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (os.path.basename(photo), open(photo, 'rb'), 'images/1.jpg/')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_api_pets(self, auth_key, pet_id):
        data = MultipartEncoder(
            fields={
                'pet_id': pet_id
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_api_pets(self, auth_key, pet_id, name: str, animal_type: str, age: str ):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result








