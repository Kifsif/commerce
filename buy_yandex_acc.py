from general.general import INSTRUMENTS_DIR, get_current_date
from general.drv import get_driver
import os
from uuid import uuid4
from random import choice
import string
import requests
import json

DESIRED_NUMBER_OF_ACCOUNTS = 10
BUY_YAND_ACC_DIR = os.path.join(INSTRUMENTS_DIR, "BuyYandAcc")
BUY_YAND_ACC_DIR_LOG_DIR = os.path.join(BUY_YAND_ACC_DIR, 'Log')
LOG_FILE = os.path.join(BUY_YAND_ACC_DIR_LOG_DIR, 'log_{}.csv'.format(get_current_date()))
SMS_ACTIVATE_API_KEY = "dB56B6272d8651Bd3B01c38e219f951c"
RUSSIA_COUNTRY = 0 # http://sms-activate.ru/index.php?act=api

def generate_unique_login():
    max_login_length = 30

    random_letter = get_random_string(1)
    unique_combination = random_letter + str(uuid4()).replace("-", "") # Логин Яндекса не должен начинаться с цифры.

    unique_combination = unique_combination[:max_login_length]

    return unique_combination

def get_random_string(string_length):
    return "".join(choice(string.ascii_letters) for _ in range(string_length))


def how_many_free_numbers():
    url = "http://sms-activate.ru/stubs/handler_api.php?api_key={api_key}&action=getNumbersStatus&country={country}".format(api_key=SMS_ACTIVATE_API_KEY, country=RUSSIA_COUNTRY)

    response = requests.get(url)
    response_text = response.text

    response_dict = json.loads(response_text)

    return response_dict.get("ya_0")


def get_first_phone_number():
    quantity_of_numbers = how_many_free_numbers()

    if not quantity_of_numbers:
        exit()

    url = "http://sms-activate.ru/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=ya_0&country={country}".format(
        api_key=SMS_ACTIVATE_API_KEY, country=RUSSIA_COUNTRY)
    response = requests.get(url)
    response_text = response.text

    phone_number = response_text[-11:]
    return phone_number


def open_yandex_to_register_acc(counter=0):
    driver = get_driver()
    url = "https://passport.yandex.ru/registration"
    driver.get(url)
    first_name_element = driver.find_element_by_id("firstname")
    first_name_element.send_keys(get_random_string(string_length=10))

    last_name_element = driver.find_element_by_id("lastname")
    last_name_element.send_keys(get_random_string(string_length=10))

    login_element = driver.find_element_by_id("login")
    login_element.send_keys(generate_unique_login())

    a_password = "trololO$8"

    password_element = driver.find_element_by_id("password")
    password_element.send_keys(a_password)

    password_confirm_element = driver.find_element_by_id("password_confirm")
    password_confirm_element.send_keys(a_password)

    phone_element = driver.find_element_by_id("phone")
    phone_number = get_first_phone_number()
    phone_element.send_keys(phone_number)

    button_to_send_code = driver.find_element_by_xpath("//*[contains(text(), 'Получить код')]")
    button_to_send_code.click()



    pass


open_yandex_to_register_acc()
pass

