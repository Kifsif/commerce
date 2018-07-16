from selenium import webdriver
import os
from selenium.webdriver import Chrome
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


USE_PROXY = True
WAIT_PERIOD = 360 # seconds


chrome_options = webdriver.ChromeOptions()
copied_proxy_list = []


from copy import deepcopy

def get_current_dir():
    return os.path.dirname(os.path.abspath(__file__)) + "/"

def get_list(current_list):
    source_file = get_current_dir() + "initial_data/" + current_list

    with open(source_file, "r") as f:
        elements = f.read().splitlines()

    return elements

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

init_proxy_list = get_list("proxy_list.txt")


# # from selenium.webdriver import Firefox

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# # driver = Firefox()
# driver = Chrome()

# #sleep(30)
#
# # try:
# #     element = WebDriverWait(driver, 70).until(
# #         EC.presence_of_element_located((By.ID, "inputEmail"))
# #     )
# #     pass
# # finally:
# #     print("inputEmail is absent.")
# #     driver.quit()
# #     exit()
#
# # sleep(5)
# current_day = datetime.date.today().strftime("%d-%m-%Y")
#

#

#
# driver.get("https://tools.pixelplus.ru/tools/geo")
#
#
#

#


global_phrases = []
global_emails = []



def get_current_phrase_bunch():
    global global_phrases
    current_phrase_bunch = global_phrases[:100]
    global_phrases = global_phrases[100:]

    phrase_log = get_current_dir() + "log/phrase_log.txt"

    with open(phrase_log, "a") as f:
        for phrase in current_phrase_bunch:
            f.write("%s\n" % phrase)

    return current_phrase_bunch

def get_current_email():
    global global_emails
    current_email = global_emails.pop(0)

    email_log = get_current_dir() + "log/email_log.txt"

    with open(email_log, "a") as f:
        f.write("%s\n" % current_email)

    return current_email


get_current_dir()
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

    # login_button = driver.find_element_by_xpath("//a[@href='/user/login']")
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



def parse_phrase_bunch(phrases):
    clear_logs()
    driver = get_driver()
    driver.get('https://tools.pixelplus.ru/')

    assert "Пиксель Тулс — бесплатные SEO-инструменты, программы и сервисы для SEO-анализа сайта и продвижения" in driver.title, "Заголовок Пикселя не тот."

    handle_login(driver)

    driver.get("https://tools.pixelplus.ru/tools/geo")

    handle_phrases(phrases, driver)


while global_phrases:
    phrases = get_current_phrase_bunch()

    parse_phrase_bunch(phrases)

    pass

a = 0
pass
from selenium.webdriver.common.proxy import *



#
# def get_phrase_bunch():
#
#     return ""
#
#
# requests_field.send_keys("""статуэтка
# статуэтка аист
# статуэтка ангел купить
# статуэтка ангел с крыльями
# статуэтка ангелы пара
# статуэтка артемида богиня охоты купить
# статуэтка афина паллада купить
# статуэтка афины
# статуэтка африка
# статуэтка африканка
# статуэтка африканка полистоун
# статуэтка белый медведь
# статуэтка богини
# статуэтка богини правосудия
# статуэтка богиня победы ника
# статуэтка богиня правосудия фемида
# статуэтка богиня фемида
# статуэтка бронза
# статуэтка бронза купить
# статуэтка бронза лошадь
# статуэтка бронза фемида
# статуэтка будда большая
# статуэтка будда бронза
# статуэтка будды
# статуэтка будды купить
# статуэтка будды цена
# статуэтка бык
# статуэтка в виде собаки
# статуэтка верблюд купить
# статуэтка верблюда
# статуэтка влюбленная пара купить
# статуэтка влюбленные
# статуэтка влюбленные фарфор
# статуэтка воин
# статуэтка гермес
# статуэтка голова коня
# статуэтка голова лошади
# статуэтка голова фараона
# статуэтка гусь
# статуэтка гусь купить
# статуэтка дама
# статуэтка два лебедя
# статуэтка два лебедя купить
# статуэтка девочка
# статуэтка девочка гипс
# статуэтка девушка
# статуэтка девушка с конем
# статуэтка девушка с птицей
# статуэтка дельфин
# статуэтка дети
# статуэтка детский сад
# статуэтка для украшений
# статуэтка дом
# статуэтка дракон с жемчужиной
# статуэтка дракона
# статуэтка дракона из бронзы
# статуэтка дракона купить
# статуэтка дракона цена
# статуэтка жаба
# статуэтка жаба с монетой купить
# статуэтка жар птица купить
# статуэтка женщина
# статуэтка жираф
# статуэтка журавля купить
# статуэтка зевс
# статуэтка йорка купить
# статуэтка йоркширский терьер
# статуэтка кенгуру
# статуэтка керамика
# статуэтка клоун
# статуэтка клоун фарфор
# статуэтка колесница
# статуэтка конь
# статуэтка конь бронза купить
# статуэтка конь на дыбах
# статуэтка конь цена
# статуэтка коня купить
# статуэтка кота
# статуэтка котик
# статуэтка кошка белая
# статуэтка кошка лежащая
# статуэтка кошка напольная
# статуэтка кошка фарфор
# статуэтка кошки
# статуэтка кошки в доме
# статуэтка красного цвета
# статуэтка курица
# статуэтка лебеди на свадьбу
# статуэтка лебедь
# статуэтка леопард
# статуэтка леопард цена
# статуэтка лисичка
# статуэтка лошадь
# статуэтка лошадь большая
# статуэтка лягушка
# статуэтка лягушка большая
# статуэтка лягушка купить
# статуэтка медведь
# статуэтка медведь купить
# статуэтка медведь цена
# статуэтка мудрости""")
#
# # download_results_checkbox = driver.find_element_by_xpath("//span[@text='Получить результаты в виде CSV-файла']")
# # download_results_checkbox_ancestor = download_results_checkbox.find_element_by_xpath(".//ancestor::div");
# # download_results_checkbox_ancestor.click()
#
# # download_results_checkbox = driver.find_element_by_class_name("jq-checkbox")
# # download_results_checkbox = driver.find_element(By.XPATH, '//span[text()="csv"]')

#
# # check_button = driver.find_element_by_xpath("//input[@type='submit']")
# sleep(1)
# check_button =  driver.find_element_by_xpath("//input[@value='Проверить']")
# check_button.click()
# sleep(180)
# pass