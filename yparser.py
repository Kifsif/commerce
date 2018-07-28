from urllib.request import urlopen
from urllib.parse import quote
from time import sleep
from random import randint
import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from general.general import get_current_dir, get_list, clear_files, write_list_to_file
from general.drv import get_driver, USE_PROXY, ATTEMPTS_TO_CHANGE_PROXY, send_proxy_to_black_list
from time import sleep




SELECTED_REGION = 213
PROJECT_DIR = get_current_dir()
PAGES_TO_PARSE = 3
LOGS_DIR = os.path.join(get_current_dir(), "../YandexParsing/log")

def get_phrases():
    yandex_parsing_init_dir = os.path.join(PROJECT_DIR, "../YandexParsing/init/phrases.txt")
    yandex_parsing_init_file = os.path.join(yandex_parsing_init_dir)
    phrases = get_list(yandex_parsing_init_file)
    return phrases

phrases = get_phrases()


def get_phrase():
    global phrases
    phrase = phrases[0]
    phrases = phrases[1:]
    return phrase

def change_city(driver):
    city_input = driver.find_element_by_id("city__front-input")
    city_input.clear()
    city_input.send_keys("Астрахань")
    city_input.send_keys(Keys.PAGE_DOWN)
    sleep(2)
    city_input.send_keys(Keys.ENTER)

def send_phrase_to_search(driver, phrase):
    text_input_field = driver.find_element_by_xpath("//input[@name='text']")
    text_input_field.clear()
    text_input_field.send_keys(phrase)
    text_input_field.send_keys((Keys.ENTER))

def remove_ads(parsed_links):
    parsed_links = [element for element in parsed_links if ("yabs" not in element) and ("market.yandex.ru" not in element)]
    return parsed_links

YANDEX_PARSING_LOG_PARTICLE = "../YandexParsing/log/"



def collect_links(driver):
    parsed_webdriver_links = driver.find_elements_by_xpath("//a[contains(@class, 'organic__url')]")

    parsed_links = [element.get_attribute("href") for element in parsed_webdriver_links]

    parsed_links = remove_ads(parsed_links)

    return parsed_links

def go_to_next_page(driver):
    sleep(3)
    next_page_link = driver.find_element_by_xpath('//a[text()="дальше"]')
    next_page_link.click()


def collect_related_items(driver):
    sleep(2)
    related_items = driver.find_elements_by_class_name("related__item")

    related_item_list = [element.text for element in related_items]

    return related_item_list


def handle_phrase(phrase):

    while True:
        try: # Транзакция.
            driver = get_driver(USE_PROXY)
            driver.get("https://yandex.ru/tune/geo/?retpath=https%3A%2F%2Fwww.yandex.ru%2F%3Fdomredir%3D1%26text%3D%25D0%25BA%25D1%2583%25D0%25BF%25D0%25B8%25D1%2582%25D1%258C%2520%25D0%25BA%25D0%25BE%25D0%25BC%25D0%25BF%25D1%258C%25D1%258E%25D1%2582%25D0%25B5%25D1%2580%26lr%3D213%26domredir%3D1&nosync=1")
            change_city(driver)

            for i in range(PAGES_TO_PARSE):
                if i == 0:
                    send_phrase_to_search(driver, phrase)

                sleep(3)
                parsed_links = collect_links(driver)

                link_log_file = "{}.txt".format(SELECTED_REGION)
                write_list_to_file(LOGS_DIR, parsed_links, link_log_file)


                related_item_list = collect_related_items(driver)

                related_items_log_file = "{}_related_items.txt".format(SELECTED_REGION)
                write_list_to_file(LOGS_DIR, related_item_list, related_items_log_file)

                go_to_next_page(driver)

            log_file = "{}_last_phrase.txt".format(SELECTED_REGION)
            write_phrase_to_log(phrase, log_file)
            break
        except:
            handle_phrase(phrase)


def parse_sites():
    driver = get_driver(USE_PROXY)



def parse_yandex(counter=0):
    clear_files(LOGS_DIR)

    while phrases:
        phrase = get_phrase()
        handle_phrase(phrase)

    parse_sites()

parse_yandex()


# PARSING_DEPTH = 1
# SLEEP_TIME_FROM = 15 # in seconds
# SLEEP_TIME_THROUGH = 30
# SEPARATOR_TO_WRITE = "\t"
#
# def get_sleep_time():
#     return randint(SLEEP_TIME_FROM, SLEEP_TIME_THROUGH)
#
# def get_links():
#     parsed_links = []
#
#     current_dir = get_current_dir()
#
#     with open('yandex.txt') as f:
#         for line in f:
#             stripped_line = line.strip() # Удаляем перенос строки.
#             links_for_line = collect_yandex_organic_links(stripped_line)
#             parsed_links += links_for_line
#     return parsed_links
#
# def link_is_acceptable(element_href):
#
#     unsuitable_marks = ["market.yandex.ru", # Яндекс.Маркет
#                         "ads", # Платные объявления.
#                        ]
#
#     for mark in unsuitable_marks:
#         if mark in element_href:
#             return False
#     return True
#
# def collect_yandex_organic_links(user_request):
#
#     target_url = "https://www.yandex.ru/search/?text=" + quote(user_request) + "&lr=" + str(REGION)
#
#     parsed_links = []
#
#     for i in range(PARSING_DEPTH):
#
#         target_url += "&p=" + str(i)
#
#         html_doc = urlopen(target_url).read().decode("utf8")
#
#         soup = BeautifulSoup(html_doc, 'html.parser')
#
#         all_links = soup.findAll("a", {"class": "organic__url"})
#
#         if len(all_links) == 0:
#             break
#
#         for element in all_links:
#             element_href = element.attrs.get("href")
#
#             if not link_is_acceptable(element_href):
#                 continue
#
#             # if "market.yandex.ru" in element_href:
#             #     continue
#
#             parsed_links.append(element_href)
#
#         current_sleep_time = get_sleep_time()
#         sleep(current_sleep_time)
#     return parsed_links
#
# def write_file_with_links():
#     links = get_links()
#     current_date = datetime.date.today().strftime("%Y%m%d")
#     file_name = "links" + current_date + ".txt"
#
#     thefile = open(file_name, 'w')
#
#     for link in links:
#         thefile.write("%s\n" % link)
#
# def join_tags(tag_list):
#     result = ""
#
#     for tag in tag_list:
#         result += str(tag)
#
#     return result
#
#
#
# def parse_link(page_url):
#     tags = ["title",
#             "keywords",
#             "description",
#             "h1",
#             "h2",
#             "h3"]
#
#     encoding_list = ["utf8", "windows-1251"]
#
#     for encoding in encoding_list:
#         try:
#             html_doc = urlopen(page_url).read().decode(encoding)
#             break
#         except UnicodeDecodeError:
#             continue
#
#     soup = BeautifulSoup(html_doc, 'html.parser')
#
#     title = soup.title.text
#     description = soup.find("meta", {"name": "description"}).attrs.get("content")
#     keywords = soup.find("meta", {"name": "keywords"}).attrs.get("content")
#     h1 = join_tags(soup.findAll("h1"))
#     h2 = join_tags(soup.findAll("h2"))
#     h3 = join_tags(soup.findAll("h3"))
#
#     compound_line = page_url + \
#                     title + SEPARATOR_TO_WRITE + \
#                     description + SEPARATOR_TO_WRITE + \
#                     keywords + SEPARATOR_TO_WRITE + \
#                     h1 + SEPARATOR_TO_WRITE + \
#                     h2 + SEPARATOR_TO_WRITE + \
#                     h3 +"\n"
#
#     with open('result.txt', "a") as f:
#         f.write(compound_line)
#
#
#
#     pass
#
# #write_file_with_links()
#
# parse_link("http://dixet.ru/kompyutery")
# parse_link("https://larga.ru/catalog/kompyutery")
# pass