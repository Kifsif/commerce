from general.drv import get_driver
from time import sleep
import os
import glob
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

MEGAINDEX_LOGIN_URL = 'https://ru.megaindex.com/auth'

MEGAINDEX_KEYWORDS_URL = 'https://ru.megaindex.com/a/urlkeywords'

MAX_NUMBER_OF_DRIVERS = 1 # Сколько окон браузера открывать одновременно.

FILE_MUTEX = False # Признак занятости файла на запись

OCCUPIED_KEYWORDS = []

EMAILS_LIST = ['petrovinwoderland@gmail.com', 'artlebedev@tutanota.com']

PASSWORD = '$7iejdlF40)'

DOWNLOAD_DIR = '/home/michael/Downloads'

URLS_TO_PARSE = []


def login(driver):
    global EMAILS_LIST
    driver.get(MEGAINDEX_LOGIN_URL)
    email = EMAILS_LIST.pop(0)
    sleep(3)


    try:
        email_input = driver.find_element_by_xpath('//input[@name="email"]')
    except NoSuchElementException:
        print("Email is absent.")
        exit

    email_input.send_keys(email)

    try:
        pass_input = driver.find_element_by_xpath('//input[@name="password"]')
    except NoSuchElementException:
        print("password is absent.")
        exit

    pass_input.send_keys(PASSWORD)

    auth_button = driver.find_element_by_xpath('//input[@value="авторизация"]')
    auth_button.click()


def count_files():
    files_mask = os.path.join(DOWNLOAD_DIR, "*.csv")
    arr = glob.glob(files_mask)
    return len(arr)



def parse_keywords(driver):

    init_number_of_files = count_files()

    while URLS_TO_PARSE:
        driver.get(MEGAINDEX_KEYWORDS_URL)
        phrase = URLS_TO_PARSE.pop()
        url_input = driver.find_element_by_xpath('//input[@name="url"]')
        url_input.send_keys(phrase)

        search_button = driver.find_element_by_tag_name('button') # Это кнопка поиска.
        search_button.click()

        nothing_found = None
        try:
            nothing_found = driver.find_element_by_xpath('//td[contains(text(), "Ничего не найдено")]')
        except NoSuchElementException:
            pass # ничего не делаем.
        if nothing_found:
            continue


        export_to_csv_button = driver.find_element_by_xpath('//input[@type="button"]') # Кнопка экспорта в CSV.

        export_to_csv_button.click()



        confirm_button = driver.find_element_by_xpath('//span[text()="Скачать файл"]')
        confirm_button.click()

        sleep(3)

        while True:
            current_number_of_files = count_files()
            if current_number_of_files > init_number_of_files:
                break
            sleep(1)


def collect_data_from_megaindex(path_to_result_file):
    global URLS_TO_PARSE


    df = pd.read_csv(path_to_result_file, delimiter=";", usecols=[1])
    URLS_TO_PARSE = df.values.tolist()


    driver = get_driver()
    login(driver)
    parse_keywords(driver)



collect_data_from_megaindex("/home/michael/PycharmProjects/YandexParsing/log/1_result.csv")