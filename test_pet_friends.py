import os

import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
# сверяем полученный результат с нашим ожиданием
    assert status == 200
# проверяем, что в результате возврращается ключ
    assert 'key' in result
    assert isinstance(result['key'], str)
    print(status, result)

def test_get_api_key_for_invalid_user(email = invalid_email, password = invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(status, result)


def test_get_all_of_pets_with_valid_key(filter= ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['my_pets']) > 0
    for pet in result['my_pets']:
        assert isinstance(pet['id'], int)
        assert isinstance(pet['name'], str)
        assert isinstance(pet['animal_type'], str)
        assert isinstance(pet['age'], int)
        assert isinstance(pet['pet_photo'], str)
        assert os.path.exists(pet['pet_photo'])
    print(result)

def test_add_information_about_new_pet_with_valid_data(name='Poni', animal_type='Home', age='5', pet_photo='images/1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == os.path.basename(pet_photo)
    pet_id = result['id']
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert any(pet['id'] == pet_id for pet in my_pets['pets'])
    print(result)

def test_delete_pet_from_database_with_valid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pytest.skip("No pets to delete")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_api_pets(auth_key, pet_id)
    assert status == 200
    _, my_pets_after_deletion = pf.get_list_of_pets(auth_key, 'my_pets')
    assert pet_id not in [pet['id'] for pet in my_pets_after_deletion['pets']]

def test_successful_update_information_about_pet_with_valid_user():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, new_pet = pf.post_api_pets(auth_key, name='Poni', animal_type='Home', age='5', pet_photo='images/1.jpg')
    pet_id = new_pet['id']
    updated_name = 'Updated Poni'
    updated_animal_type = 'Updated Home'
    updated_age = '6'
    status, result = pf.put_api_pets(auth_key, pet_id, name=updated_name, animal_type=updated_animal_type, age=updated_age)
    assert status == 200
    assert result['name'] == updated_name
    assert result['animal_type'] == updated_animal_type
    assert result['age'] == updated_age
    assert result['id'] == pet_id
    print(result)



