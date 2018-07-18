from selenium.webdriver import Chrome
from copy import deepcopy
from selenium import webdriver
from .general import get_list, get_current_dir
import os

WAIT_PERIOD = 360 # seconds
USE_PROXY = False
ATTEMPTS_TO_CHANGE_PROXY = 10

chrome_options = webdriver.ChromeOptions()
copied_proxy_list = []

project_dir = get_current_dir()
full_path_to_proxy_list = os.path.join(project_dir, "../CommerceParsing/Init/proxy_list.txt")

init_proxy_list = get_list(full_path_to_proxy_list)

def change_proxy():
    try:
        assert "Пиксель Тулс — бесплатные SEO-инструменты, программы и сервисы для SEO-анализа сайта и продвижения" in driver.title, "Заголовок Пикселя не тот."
    except AssertionError:
        # Что-то пошло не так: парсить не может. Может быть, прокси-сервер не рабочий. Поменяем прокси-сервер и снова
        # попробуем. Так несколько раз.
        driver.quit()
        if counter == ATTEMPTS_TO_CHANGE_PROXY:
            exit() # Выполнили много попыток поменять прокси, но парсинг все равно не получается.
        counter += 1
        parse_phrase_bunch(phrases, counter)



def get_proxy():
    global copied_proxy_list
    try:
        a_proxy = copied_proxy_list.pop()
    except IndexError:
        copied_proxy_list = deepcopy(init_proxy_list)
        a_proxy = copied_proxy_list.pop()

    return a_proxy

def get_driver(use_proxy=False):
    if use_proxy:
        a_proxy = get_proxy()
        chrome_options.add_argument('--proxy-server=%s' % a_proxy)
        driver = Chrome(chrome_options=chrome_options)
    else:
        driver = Chrome()
    driver.implicitly_wait(WAIT_PERIOD)
    driver.set_page_load_timeout(WAIT_PERIOD)

    return driver