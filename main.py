import os
from selenium.webdriver.common.by import By
from general.drv import get_driver
from general.general import get_current_dir, PARSING_PATH_PARTICLE, INIT_PATH_PARTICLE, get_list

USE_PROXY = True
ATTEMPTS_TO_CHANGE_PROXY = 10

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