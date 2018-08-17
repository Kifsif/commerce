from general.drv import get_driver, get_proxy
from general.general import get_current_dir, write_list_to_file, write_phrase_to_log, get_list
import os
import requests
from requests.exceptions import ProxyError
from random import randint
from time import sleep
from bs4 import BeautifulSoup

# Регионы https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/

USE_SLEEP_TIME = True # При реальном парсинге всегда включать. Выключить задержку только для отладки.
PARSING_PATH_PARTICLE = "../KeywordStuffing/"
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"
URL_AND_KEYS_FILE = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "init.csv")
ENCODING = 'windows-1251'
SIZE_OF_CHUNK = 10
ARSENKIN = 'https://arsenkin.ru/tools/filter/index.php'
RESULT_FILE = "" # Инициализируется в функции write_table_open_tag.
PARSE_RUSSIA = False
PARSE_MOSCOW = True

# Обязательно строкой, а не цифрой!
MOSCOW_REGION = '1' # С областью.
RUSSIA_REGION = '225'


def separate_url_and_region_and_phrases(url_phrases_list):
    url = url_phrases_list[0].strip()

    assert ord(url[0]) != 65279, "The file has Byte order mark. Go to the text" \
                                 " editor, open file, change encoding to UTF-8. " \
                                 "That is without BOM!"

    region = url_phrases_list[1].strip()
    phrases = url_phrases_list[2:]

    return url, region, phrases

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

def request_and_write_phrase(phrases_str, site, region):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }

    proxies = {'http': 'http://{}'.format(get_proxy())}
    print(proxies)

    try:
        r = requests.post(ARSENKIN, headers=headers, proxies=proxies, data={'a_mode': 'getThis',
                                                                            'ajax': 'Y',
                                                                            'text': phrases_str,
                                                                            'site': site,
                                                                            'city': region})
    except ProxyError:
        print("Bad proxy: {}".format(proxies))
        request_and_write_phrase(phrases_str, site, region)

    txt_str = r.text
    success = write_results(txt_str)

    if not success:
        print(txt_str)
        sleep(get_sleep_time())
        request_and_write_phrase(phrases_str, site, region)


def handle_chunks(chunks, site, region):
    for chunk in chunks:
        phrases_str = "\n".join(chunk)
        request_and_write_phrase(phrases_str, site, region)
        sleep_time = get_sleep_time()
        sleep(sleep_time)


def write_table_open_tag(site, region):
    global RESULT_FILE

    RESULT_FILE = os.path.join(get_current_dir(), PARSING_PATH_PARTICLE,
                               'Result/{domain}_{region}_result.html'.format(domain=site, region=region))
    write_phrase_to_log("<html>\n<table>\n",
                        write_mode='w',
                        enc=ENCODING,
                        full_path_to_file=RESULT_FILE)


def write_table_closing_tag():
    write_phrase_to_log("</table>\n</html>",
                        write_mode='a',
                        enc=ENCODING,
                        full_path_to_file=RESULT_FILE)


def parse_all(site, region, phrases):
    assert isinstance(MOSCOW_REGION, str)
    assert isinstance(RUSSIA_REGION, str)

    write_table_open_tag(site, region)
    chunks = list(get_chunks_generator(phrases))
    handle_chunks(chunks, site, region)
    write_table_closing_tag()

def get_initial_info():
    url_region_phrases_list = get_list(URL_AND_KEYS_FILE)
    site, region, phrases = separate_url_and_region_and_phrases(url_region_phrases_list)
    return site, region, phrases

site, region, phrases = get_initial_info()

parse_all(site, region, phrases)


if region != MOSCOW_REGION and PARSE_MOSCOW:
    parse_all(site, MOSCOW_REGION, phrases)
if region != RUSSIA_REGION and PARSE_RUSSIA:
    parse_all(site, RUSSIA_REGION, phrases)

