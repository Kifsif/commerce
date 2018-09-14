from general.drv import get_driver
from time import sleep
import os
import glob
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from general.general import get_current_date, write_phrase_to_log, \
    INSTRUMENTS_DIR, write_list_to_file, get_list, get_current_date_time
import sys
from yparser import remove_garbage

MEGAINDEX_LOGIN_URL = 'https://ru.megaindex.com/auth'
MEGAINDEX_KEYWORDS_URL = 'https://ru.megaindex.com/a/urlkeywords'
# MAX_NUMBER_OF_DRIVERS = 1 # Сколько окон браузера открывать одновременно.
EMAILS_LIST = ['petrovinwoderland@gmail.com', 'artlebedev@tutanota.com']
PASSWORD = '$7iejdlF40)'
DOWNLOAD_DIR = '/home/michael/Downloads'
URLS_TO_PARSE = []
COLUMN_WITH_URLS = 1


MEGAINDEX_DIR = os.path.join(INSTRUMENTS_DIR, 'ParseMegaindex')
MEGAINDEX_LOG_DIR = os.path.join(MEGAINDEX_DIR, 'Log')
LOG_FILE = os.path.join(MEGAINDEX_LOG_DIR, 'log_{}.csv'.format(get_current_date()))
URLS_FILE = os.path.join(MEGAINDEX_LOG_DIR, 'urls.csv')
PROJECT = ""

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


def get_last_parsed_url(log):
    # В лог-файле все строки содержат комментарий, отделенный от url словом "DELIMITER".

    last_line_in_log = log[-1].strip()
    delimter_position = last_line_in_log.index("DELIMITER")
    return last_line_in_log[:delimter_position]



def get_start_position_to_parse():

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log = list(f)
    except FileNotFoundError:
        return 0

    last_line_in_log = get_last_parsed_url(log)
    last_url_ind = len(URLS_TO_PARSE) - 1

    index_of_already_parsed_url = URLS_TO_PARSE.index(last_line_in_log)

    if index_of_already_parsed_url == last_url_ind:
        exit

    next_url = index_of_already_parsed_url + 1

    return next_url


def count_files():
    files_mask = os.path.join(DOWNLOAD_DIR, "*.csv")
    arr = glob.glob(files_mask)
    return len(arr)

def rename_downloaded_file():
    # Google Chrome перестает автоматически переименовывать скачанные файлы с одинаковым именем, если их более 100.
    # Поэтому каждый скачанный файлы надо переименовать и переместить в отдельную папку.
    old_name = "keywords.csv"
    file_mask = os.path.join(DOWNLOAD_DIR, old_name)
    file = glob.glob(file_mask)
    os.rename(os.path.join(DOWNLOAD_DIR, old_name), os.path.join(DOWNLOAD_DIR, "{}_keywords_{}.csv".format(PROJECT,
                                                                                                           get_current_date_time())))


def parse_url(driver, url):

    try: # Транзакция
        driver.get(MEGAINDEX_KEYWORDS_URL)
        init_number_of_files = count_files()
        url_input = driver.find_element_by_xpath('//input[@name="url"]')
        url_input.clear()
        url_input.send_keys(url)

        search_button = driver.find_element_by_tag_name('button')  # Это кнопка поиска.
        search_button.click()

        nothing_found = None # Элемент, соответствуюий тегу с текстом "Ничего не найдено".

        try:
            nothing_found = driver.find_element_by_xpath('//td[contains(text(), "Ничего не найдено")]')
        except NoSuchElementException:
            pass  # ничего не делаем.

        if nothing_found:
            write_phrase_to_log("{}DELIMITER {} ничего не найдено.".format(url, PROJECT), 'a', 'utf-8', LOG_FILE)
            return

        export_to_csv_button = driver.find_element_by_xpath('//input[@type="button"]')  # Кнопка экспорта в CSV.

        export_to_csv_button.click()

        confirm_button = driver.find_element_by_xpath('//span[text()="Скачать файл"]')
        confirm_button.click()

        while True:
            current_number_of_files = count_files()
            if current_number_of_files > init_number_of_files:
                rename_downloaded_file()
                break
            sleep(1)

        write_phrase_to_log("{}DELIMITER {} успешно.".format(url, PROJECT), 'a', 'utf-8', LOG_FILE)

    except Exception as e:
        print(e)
        parse_url(driver, url)


def parse_all_urls(driver):
    while True:
        parse_from_ind = get_start_position_to_parse()
        try:
            url = URLS_TO_PARSE[parse_from_ind]
        except IndexError:
            sys.exit()

        parse_url(driver, url)


def create_urls_to_parse(path_to_raw_file):
    # df = pd.read_csv(path_to_raw_file, delimiter=";", usecols=[COLUMN_WITH_URLS])
    df = pd.read_csv(path_to_raw_file) # Если парсили через КК.

    tmp_urls = [element[0] for element in df.values]
    tmp_urls = list(set(tmp_urls))
    write_list_to_file(link_list=tmp_urls, enc='utf-8', full_path_to_file=URLS_FILE)
    return tmp_urls


def init_urls_to_parse(path_to_raw_file):
    global URLS_TO_PARSE
    global PROJECT

    PROJECT = input("Введите название проекта: ")


    tmp_urls = get_list(URLS_FILE, 'utf-8')
    if tmp_urls:
        URLS_TO_PARSE = tmp_urls
    else:
        tmp_urls = create_urls_to_parse(path_to_raw_file)
        URLS_TO_PARSE = tmp_urls



def collect_data_from_megaindex(path_to_raw_file):
    global URLS_TO_PARSE
    init_urls_to_parse(path_to_raw_file)
    URLS_TO_PARSE = remove_garbage(URLS_TO_PARSE)
    driver = get_driver()
    login(driver)

    parse_all_urls(driver)


collect_data_from_megaindex("/home/michael/PycharmProjects/YandexParsing/log/1_result.csv")