from selenium.webdriver import Chrome
from copy import deepcopy
from selenium import webdriver
from .general import get_list, get_current_dir
from selenium.webdriver import DesiredCapabilities
import os

WAIT_PERIOD = 360 # seconds
USE_PROXY = False
ATTEMPTS_TO_CHANGE_PROXY = 10


copied_proxy_list = []

project_dir = get_current_dir()
full_path_to_proxy_list = os.path.join(project_dir, "../CommerceParsing/Init/proxy_list.txt")

init_proxy_list = get_list(full_path_to_proxy_list)

# def change_proxy():
#     try:
#         assert "Пиксель Тулс — бесплатные SEO-инструменты, программы и сервисы для SEO-анализа сайта и продвижения" in driver.title, "Заголовок Пикселя не тот."
#     except AssertionError:
#         # Что-то пошло не так: парсить не может. Может быть, прокси-сервер не рабочий. Поменяем прокси-сервер и снова
#         # попробуем. Так несколько раз.
#         driver.quit()
#         if counter == ATTEMPTS_TO_CHANGE_PROXY:
#             exit() # Выполнили много попыток поменять прокси, но парсинг все равно не получается.
#         counter += 1
#         parse_phrase_bunch(phrases, counter)

def send_proxy_to_black_list(a_proxy):


    pass

def get_proxy():
    global copied_proxy_list
    try:
        a_proxy = copied_proxy_list.pop()
    except IndexError:
        copied_proxy_list = deepcopy(init_proxy_list)
        a_proxy = copied_proxy_list.pop()

    return a_proxy


chrome_options = webdriver.ChromeOptions()

def get_driver(use_proxy=False):
    if use_proxy:
        a_proxy = '94.242.58.108:1448'
        desired_capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities["proxy"] = {'proxyType': 'MANUAL',
         'httpProxy': a_proxy, 'autodetect': False}
        # chrome_options.add_argument('--proxy-server={}'.format(a_proxy))
        # driver = Chrome(chrome_options=chrome_options, )
        driver = Chrome(desired_capabilities=desired_capabilities)
        pass
    else:
        driver = Chrome()
    driver.implicitly_wait(WAIT_PERIOD)
    driver.set_page_load_timeout(WAIT_PERIOD)

    return driver


# def get_driver(use_prosy=False):
#     if use_prosy:
#         a_proxy = get_proxy()
#
#         desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
#
#         desired_capabilities['proxy'] = {
#             "httpProxy": a_proxy,
#             "autodetect": False,
#             "proxyType":"MANUAL",
#         }
#
#         dri