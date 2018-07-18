# from selenium import webdriver

import os
# from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
# from copy import deepcopy
import sys
from general.drv import get_driver
from general.general import get_current_dir, PARSING_PATH_PARTICLE, INIT_PATH_PARTICLE, get_list

USE_PROXY = True
# WAIT_PERIOD = 360 # seconds

# PARSING_PATH_PARTICLE = "../CommerceParsing/"
# INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"

ATTEMPTS_TO_CHANGE_PROXY = 10

# chrome_options = webdriver.ChromeOptions()
# copied_proxy_list = []


# def get_current_dir():
#     return os.path.dirname(os.path.abspath(__file__)) + "/"

# def get_list(current_list):
#     source_file = get_current_dir() + INIT_PATH_PARTICLE + current_list
#
#     with open(source_file, "r") as f:
#         elements = f.read().splitlines()
#
#     return elements

# def get_proxy():
#     global copied_proxy_list
#     try:
#         a_proxy = copied_proxy_list.pop()
#     except IndexError:
#         copied_proxy_list = deepcopy(init_proxy_list)
#         a_proxy = copied_proxy_list.pop()
#
#     return a_proxy

# def get_driver(use_proxy=False):
#     if use_proxy:
#         a_proxy = get_proxy()
#         chrome_options.add_argument('--proxy-server=%s' % a_proxy)
#         driver = Chrome(chrome_options=chrome_options)
#     else:
#         driver = Chrome()
#     driver.implicitly_wait(WAIT_PERIOD)
#     driver.set_page_load_timeout(WAIT_PERIOD)
#
#     return driver

# init_proxy_list = get_list("proxy_list.txt")

global_phrases = []
global_emails = []


def get_current_phrase_bunch():
    global global_phrases
    current_phrase_bunch = global_phrases[:100]
    global_phrases = global_phrases[100:]
    return current_phrase_bunch

def get_email_log_path():
    email_log = os.path.join(get_current_dir(), PARSING_PATH_PARTICLE, "log/email_log.txt")
    return email_log

def get_last_used_email():
    email_log = get_email_log_path()

    try:
        with open(email_log, "r") as f:
            email = f.readline()
    except FileNotFoundError:
        return None
    return email.strip()

def is_excluded(email):
    source_file = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "excluded_emails.txt")

    with open(source_file, "r") as f:
        excluded_emails = [line.rstrip('\n') for line in f]

    return email in excluded_emails

def get_current_email():
    last_email = get_last_used_email()

    first_free_email = 0

    if last_email:
        last_email_position = global_emails.index(last_email)
        first_free_email = last_email_position + 1

        try:
            current_email = global_emails[first_free_email]
        except IndexError:
            print("No emails left.")
            exit()
    else:
        current_email = global_emails[0]

    email_excluded = is_excluded(current_email)

    if email_excluded:
        while email_excluded:
            first_free_email += 1
            current_email = global_emails[first_free_email]
            email_excluded = is_excluded(current_email)

    email_log = get_email_log_path()

    with open(email_log, "w") as f:
        f.write("%s\n" % current_email)

    return current_email

# get_current_dir()
global_phrases = get_list("word_list.txt")
global_emails = get_list("email_list.txt")


def handle_login(driver):
    login_button = driver.find_element_by_link_text('Войти')
    login_button.click()

    email = get_current_email()

    input_email_field = driver.find_element_by_id("inputEmail")
    input_email_field.send_keys(email)

    input_email_field = driver.find_element_by_id("inputPassword")
    input_email_field.send_keys("goskomstat")

    login_button = driver.find_element_by_xpath("//input[@type='submit']")
    login_button.click()

def log_out(driver):
    logout_button = driver.find_element_by_xpath("//a[@href='/user/logout']")
    logout_button.click()

def handle_phrases(phrases, driver):
    requests_field = driver.find_element_by_id("requests")
    str_phrases = "\n".join(phrases)
    requests_field.send_keys(str_phrases)

    download_results_checkbox = driver.find_element(By.XPATH, '//span[text()="Получить результаты в виде CSV-файла"]')
    download_results_checkbox.click()

    check_button =  driver.find_element_by_xpath("//input[@value='Проверить']")
    check_button.click()
    log_out(driver)
    driver.quit()


def clear_logs():
    logs_dir = os.path.join(get_current_dir(),"log")
    import shutil
    try:
        shutil.rmtree(logs_dir)
    except FileNotFoundError:
        pass # Do nothing

    os.makedirs(logs_dir)

def parse_phrase_bunch(phrases, counter=0):
    clear_logs()
    driver = get_driver()
    driver.get('https://tools.pixelplus.ru/')

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

    handle_login(driver)

    driver.get("https://tools.pixelplus.ru/tools/geo")

    handle_phrases(phrases, driver)


while global_phrases:
    phrases = get_current_phrase_bunch()

    parse_phrase_bunch(phrases)