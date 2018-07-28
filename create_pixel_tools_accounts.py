from general.drv import get_driver
from general.general import write_phrase_to_log
from general.drv import get_driver, USE_PROXY
from time import sleep
from selenium.webdriver.common.keys import Keys

mail_accounts = """"""

mail_accounts_list = mail_accounts.split("\n")

def get_mail_account():

    global mail_accounts_list

    try:
        current_account = mail_accounts_list.pop()
    except IndexError:
        return None

    return current_account

def create_pixel_plus_account():

    try:
        driver = get_driver(USE_PROXY)
        mail_account = get_mail_account()

        if not mail_account:
            quit()

        driver.get("https://tools.pixelplus.ru/#internal-optimization")
        login_button = driver.find_element_by_link_text('Войти')
        login_button.click()

        register_button = driver.find_element_by_link_text('Зарегистрироваться.')
        register_button.click()

        nick_field = driver.find_element_by_id("input-name")
        nick_field.send_keys(mail_account)

        nick_field = driver.find_element_by_id("input-email")
        nick_field.send_keys(mail_account)

        nick_field = driver.find_element_by_id("input-password")
        nick_field.send_keys("goskomstat")
        sleep(2)
        # nick_field.send_keys(Keys.ENTER)

        # button_element = driver.find_element_by_link_text('Зарегистрироваться')
        # button_element.click()

        pass
        # sleep(20)

    except:
        create_pixel_plus_account()

    write_phrase_to_log(mail_account, "/home/michael/PycharmProjects/PixelPlus/log/used_emails.txt")


def handle():
    while True:
        create_pixel_plus_account()

handle()