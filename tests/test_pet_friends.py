from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_api_key_for_invalid_user(email='asdsffasf@mail.ru', password='dsfgedfgbd'):
    """Тест направлен на проверку возможности получения ключа api при наличии неверных данных пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_valid_user_without_email(email='', password=valid_password):
    """Тест направлен на проверку возможности получения ключа api при отсутствии введенной почты"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_valid_user_without_password(email=valid_email, password=''):
    """Тест направлен на проверку возможности получения ключа api при отсутствии введенного пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_without_valid_name(name='', animal_type='кот',
                                     age='8', pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить питомца без имени
    (питомца без имени добавить можно уточнить у разработчиков)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

def test_successful_delete_self_pet_without_name():
    """Проверяем возможность удаления питомца без имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "", "кот", "8", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_without_valid_animal_type(name='Спартак', animal_type='',
                                     age='8', pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить питомца без породы
    (питомца без породы добавить можно уточнить у разработчиков)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

def test_successful_delete_self_pet_without_animal_type():
    """Проверяем возможность удаления питомца без породы"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Спартак", "", "8", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_with_negative_age(name='Спартак', animal_type='кот',
                                     age='-5', pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить питомца с отрицательным значением возраста
    (питомца с отрицательным значением возраста добавить можно - уточнить у разработчиков)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

def test_successful_delete_self_pet_with_negative_age():
    """Проверяем возможность удаления питомца с отрицательным значением возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Спартак", "кот", "-5", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_without_photo(name='Спартак', animal_type='кот',
                                     age='-5', pet_photo=''):
    """Проверяем, что можно добавить питомца без фото
    (питомца без фото добавить нельзя)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200