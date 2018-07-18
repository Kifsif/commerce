from urllib.request import urlopen
from urllib.parse import quote
from time import sleep
from random import randint
import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from general.general import get_current_dir, get_list
from general.drv import get_driver, USE_PROXY, ATTEMPTS_TO_CHANGE_PROXY
from time import sleep


SELECTED_REGION = 213



def get_phrases():
    project_dir = get_current_dir()
    yandex_parsing_init_dir = os.path.join(project_dir, "../YandexParsing/phrases.txt")
    yandex_parsing_init_file = os.path.join(yandex_parsing_init_dir)
    phrases = get_list(yandex_parsing_init_file)
    return phrases

phrases = get_phrases()


def get_phrase():
    global phrases
    phrase = phrases[0]
    phrases = phrases[1:]
    return phrase


def handle_phrase(phrase, counter=0):
    driver = get_driver()
    driver.get("https://yandex.ru/tune/geo/?retpath=https%3A%2F%2Fwww.yandex.ru%2F%3Fdomredir%3D1%26text%3D%25D0%25BA%25D1%2583%25D0%25BF%25D0%25B8%25D1%2582%25D1%258C%2520%25D0%25BA%25D0%25BE%25D0%25BC%25D0%25BF%25D1%258C%25D1%258E%25D1%2582%25D0%25B5%25D1%2580%26lr%3D213%26domredir%3D1&nosync=1")

    try:
        assert "Яндекс" in driver.title, "Заголовок Яндекса не тот."
    except AssertionError:
        # Что-то пошло не так: парсить не может. Может быть, прокси-сервер не рабочий. Поменяем прокси-сервер и снова
        # попробуем. Так несколько раз.
        driver.quit()
        if counter == ATTEMPTS_TO_CHANGE_PROXY:
            exit()  # Выполнили много попыток поменять прокси, но парсинг все равно не получается.
        counter += 1
        handle_phrase(phrase, counter)
    counter = 0  # Даже если были неудачные попытки, в следующий раз начнем отсчет заново.

    city_input = driver.find_element_by_id("city__front-input")
    city_input.clear()
    city_input.send_keys("Астрахань")
    city_input.send_keys(Keys.PAGE_DOWN)
    sleep(1)
    city_input.send_keys(Keys.ENTER)

    text_input_field = driver.find_element_by_id("text")
    text_input_field.send_keys(phrase)
    text_input_field.send_keys((Keys.ENTER))


    pass




def parse_yandex(counter=0):
    while phrases:
        phrase = get_phrase()
        handle_phrase(phrase)

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