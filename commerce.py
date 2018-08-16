import os
from selenium.webdriver.common.by import By
from general.drv import get_driver, USE_PROXY
from general.general import get_current_dir, get_list, clear_files, write_phrase_to_log

global_phrases = []
global_emails = []

PARSING_PATH_PARTICLE = "../CommerceParsing/"
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"

PHRASE_BUNCH_SIZE = 300

word_list_full_path = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "word_list.txt")
email_list_full_path = os.path.join(get_current_dir(), INIT_PATH_PARTICLE, "email_list.txt")

INDEX_LOG_FILE = "index_log.txt"

global_phrases =  get_list(word_list_full_path)


global_emails = get_list(email_list_full_path)

def get_log_path(log):
    log_path = os.path.join(get_current_dir(), PARSING_PATH_PARTICLE, "log", log)
    return log_path

def get_phrase_counter_val():
    index_log_file = get_log_path(INDEX_LOG_FILE)
    try:
        with open(index_log_file, 'r') as f:
            line = f.readline()
            if line:
                phrase_counter = int(line)
            else:
                phrase_counter = 0
    except FileNotFoundError:
        phrase_counter = 0

    return phrase_counter

phrase_counter = get_phrase_counter_val()

def get_current_phrase_bunch():
    global global_phrases
    # current_phrase_bunch = global_phrases[:100]
    # global_phrases = global_phrases[100:]
    # phrase_counter += 100

    start = phrase_counter
    end = start + PHRASE_BUNCH_SIZE

    current_phrase_bunch = global_phrases[start:end]

    return current_phrase_bunch



def get_last_used_email():
    email_log = get_log_path("email_log.txt")

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

def get_current_email(infinite_loop=True):
    global global_emails
    last_email = get_last_used_email()

    first_free_email = 0

    if last_email:
        last_email_position = global_emails.index(last_email)
        first_free_email = last_email_position + 1

        try:
            current_email = global_emails[first_free_email]
        except IndexError:
            if infinite_loop:
                global_emails = get_list(email_list_full_path)
                current_email = get_current_email()
                return current_email
            else:
                print("Емейлов не осталось.")
                exit()
    else:
        current_email = global_emails[0]

    email_excluded = is_excluded(current_email)

    if email_excluded:
        while email_excluded:
            first_free_email += 1
            current_email = global_emails[first_free_email]
            email_excluded = is_excluded(current_email)

    # email_log = get_email_log_path()

    # with open(email_log, "w") as f:
    #     f.write("%s\n" % current_email)

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

    return email

def log_out(driver):
    logout_button = driver.find_element_by_xpath("//a[@href='/user/logout']")
    logout_button.click()

def check_limits(driver):
    hourglass_element = driver.find_element_by_class_name("site-icon-hourglass")
    li_tag_with_limits = hourglass_element.find_element_by_xpath('..')
    li_tag_text = li_tag_with_limits.text

    start_position = li_tag_with_limits.text.find(":") + 1
    end_position = li_tag_with_limits.text.find("/")

    limits_spent_str = li_tag_text[start_position:end_position].strip()

    limits_spent_int = int(limits_spent_str)

    if limits_spent_int >= 1200:
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
    global phrase_counter

    logs_dir = os.path.join(get_current_dir(), "log")
    # clear_files(logs_dir)

    try:
        driver = get_driver(USE_PROXY)
        driver.get('https://tools.pixelplus.ru/')

        used_email = handle_login(driver)

        driver.get("https://tools.pixelplus.ru/tools/geo")

        email_log = get_log_path("email_log.txt")
        write_phrase_to_log(used_email, email_log)

        handle_phrases(phrases, driver)

        index_log = get_log_path("index_log.txt")
        write_phrase_to_log(phrase_counter, index_log)
        phrase_counter += PHRASE_BUNCH_SIZE

    except Exception as e:
        print("Проблема ^^^")
        print(e)
        driver.quit()
        parse_phrase_bunch(phrases)


while global_phrases:
    phrases = get_current_phrase_bunch()

    parse_phrase_bunch(phrases)