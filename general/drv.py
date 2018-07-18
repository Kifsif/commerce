from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from copy import deepcopy
from selenium import webdriver
from .general import get_list

WAIT_PERIOD = 360 # seconds

chrome_options = webdriver.ChromeOptions()
copied_proxy_list = []

init_proxy_list = get_list("proxy_list.txt")

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