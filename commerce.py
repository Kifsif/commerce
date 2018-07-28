import os
from selenium.webdriver.common.by import By
from general.drv import get_driver, ATTEMPTS_TO_CHANGE_PROXY, USE_PROXY
from general.general import get_current_dir, get_list, clear_files

global_phrases = []
global_emails = []

PARSING_PATH_PARTICLE = "../CommerceParsing/"
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"

word_list_full_path = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "word_list.txt")
email_list_full_path = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "email_list.txt")

global_phrases =  get_list(word_list_full_path)


global_emails = get_list(email_list_full_path)


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



def handle_login(driver):
    login_button = driver.find_element_by_link_text('Войти')
    login_button.click()

    email = get_current_email()
    print(email)

    input_email_field = driver.find_element_by_id("inputEmail")
    input_email_field.send_keys(email)

    input_email_field = driver.find_element_by_id("inputPassword")
    input_email_field.send_keys("goskomstat")

    login_button = driver.find_element_by_xpath("//input[@type='submit']")
    login_button.click()

def log_out(driver):
    logout_button = driver.find_element_by_xpath("//a[@href='/user/logout']")
    logout_button.click()

def check_limits(driver):
    hourglass_element = driver.find_element_by_class_name("site-icon-hourglass")
    li_tag_with_limits = driver.find_element_by_class_name("site-icon-hourglass").find_element_by_xpath('..')
    li_tag_text = li_tag_with_limits.text

    start_position = li_tag_with_limits.text.find(":") + 1
    end_position = li_tag_with_limits.text.find("/")

    limits_spent_str = li_tag_text[start_position:end_position].strip()

    limits_spent_int = int(limits_spent_str)

    if limits_spent_int != 0:
        raise Exception("Нет лимитов!")


def handle_phrases(phrases, driver):
    check_limits(driver)

    requests_field = driver.find_element_by_id("requests")





    str_phrases = "\n".join(phrases)
    requests_field.send_keys(str_phrases)

    download_results_checkbox = driver.find_element(By.XPATH, '//span[text()="Получить результаты в виде CSV-файла"]')
    download_results_checkbox.click()



    check_button =  driver.find_element_by_xpath("//input[@value='Проверить']")
    check_button.click()
    log_out(driver)
    driver.quit()

def parse_phrase_bunch(phrases):
    logs_dir = os.path.join(get_current_dir(), "log")
    clear_files(logs_dir)

    try:
        driver = get_driver(USE_PROXY)
        driver.get('https://tools.pixelplus.ru/')

    # try:
    #     assert "Пиксель Тулс — бесплатные SEO-инструменты, программы и сервисы для SEO-анализа сайта и продвижения" in driver.title, "Заголовок Пикселя не тот."
    # except AssertionError:
    #     # Что-то пошло не так: парсить не может. Может быть, прокси-сервер не рабочий. Поменяем прокси-сервер и снова
    #     # попробуем. Так несколько раз.
    #     driver.quit()
    #     if counter == ATTEMPTS_TO_CHANGE_PROXY:
    #         exit() # Выполнили много попыток поменять прокси, но парсинг все равно не получается.
    #     counter += 1

        handle_login(driver)

        driver.get("https://tools.pixelplus.ru/tools/geo")

        handle_phrases(phrases, driver)

    except Exception as e:
        print("Проблема ^^^")
        print(e)
        driver.quit()
        parse_phrase_bunch(phrases)


while global_phrases:
    phrases = get_current_phrase_bunch()

    parse_phrase_bunch(phrases)