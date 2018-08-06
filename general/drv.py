from selenium.webdriver import Chrome
from copy import deepcopy
from selenium import webdriver
from .general import get_list, get_current_dir
from selenium.webdriver import DesiredCapabilities
import os

WAIT_PERIOD = 760 # seconds
USE_PROXY = True
ATTEMPTS_TO_CHANGE_PROXY = 10


copied_proxy_list = []

project_dir = get_current_dir()
full_path_to_proxy_list = os.path.join(project_dir, "../CommerceParsing/Init/proxy_list.txt")

init_proxy_list = get_list(full_path_to_proxy_list)


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

def get_driver():
    if USE_PROXY:
        a_proxy = get_proxy()
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