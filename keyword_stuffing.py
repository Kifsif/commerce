from general.drv import get_driver, get_proxy
from general.general import get_current_dir, write_list_to_file, write_phrase_to_log
import os
import requests
from requests.exceptions import ProxyError
from random import randint
from time import sleep
from bs4 import BeautifulSoup



USE_SLEEP_TIME = True # При реальном парсинге всегда включать. Выключить задержку только для отладки.
PARSING_PATH_PARTICLE = "../KeywordStuffing/"
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"
RESULT_FILE = os.path.join(get_current_dir(), PARSING_PATH_PARTICLE, 'Result/result.txt')
URL_AND_KEYS_FILE = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "url_keys.txt")
ENCODING = 'windows-1251'
REGION = 213
SIZE_OF_CHUNK = 10
from itertools import islice

SITE = 'ritm-it.ru'
# URL = "http://ip-api.com/" # Раскомментировать для тестов.

URL = 'https://arsenkin.ru/tools/filter/index.php'


phrases = ['купить ибп',
           'купить ббп',
           'купить ups',
           'купить упс',
           'купить ибп онлайн',
           'купить ббп онлайн',
           'купить ups онлайн',
           'купить упсонлайн',
           'ибп apc',
           'мощный apc',
           'серверный ибп']


def get_chunks_generator(phrases):
    for i in range(0, len(phrases), SIZE_OF_CHUNK):
        yield phrases[i:i + SIZE_OF_CHUNK]

def get_sleep_time():
    if not USE_SLEEP_TIME:
        return 0 # Отключить задержку для целей отладки.

    seconds = randint(60, 90)
    return seconds

def write_results(txt_str):
    # Если сайт возвратил таблицу с данными, все хорошо. Тогда возвращаем True.
    # Если сайт не вернул таблицу с данными (вернул ошибку), возвращаем False.
    soup = BeautifulSoup(txt_str, 'html.parser')
    try:
        all_tr = list(soup.find('tbody').find_all("tr"))
    except:
        return False
    write_list_to_file(link_list=all_tr,
                       enc=ENCODING,
                       full_path_to_file=RESULT_FILE)
    return True

def request_and_write_phrase(phrases_str):

    proxies = {'http': 'http://{}'.format(get_proxy())}
    print(proxies)

    try:
        r = requests.post(URL, proxies=proxies, data={'a_mode': 'getThis',
                                                      'ajax': 'Y',
                                                      'text': phrases_str,
                                                      'site': SITE,
                                                      'city': str(REGION)})
    except ProxyError:
        print("Bad proxy: {}".format(proxies))
        request_and_write_phrase(phrases_str)

    txt_str = r.text
    success = write_results(txt_str)

    if not success:
        print(txt_str)
        sleep(get_sleep_time())
        request_and_write_phrase(phrases_str)


def handle_chunks(chunks):
    for chunk in chunks:
        phrases_str = "\n".join(chunk)
        request_and_write_phrase(phrases_str)
        sleep_time = get_sleep_time()
        sleep(sleep_time)

def write_table_open_tag():
    write_phrase_to_log("<html>\n<table>\n",
                        write_mode='w',
                        enc=ENCODING,
                        full_path_to_file=RESULT_FILE)

def write_table_closing_tag():
    write_phrase_to_log("</table>\n</html>",
                        write_mode='a',
                        enc=ENCODING,
                        full_path_to_file=RESULT_FILE)

write_table_open_tag()
chunks = list(get_chunks_generator(phrases))
handle_chunks(chunks)
write_table_closing_tag()