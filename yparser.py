import os
from selenium.webdriver.common.keys import Keys
from general.general import get_current_dir, get_list, clear_files, write_list_to_file, write_phrase_to_log
from general.drv import get_driver, USE_PROXY
from time import sleep

SELECTED_REGION = 1 # https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/
PROJECT_DIR = get_current_dir()
PAGES_TO_PARSE = 3
LOGS_DIR = os.path.join(get_current_dir(), "../YandexParsing/log")
ENCODING = 'utf-8'
RESULT_FILE = os.path.join(LOGS_DIR, "{}_result.csv".format(SELECTED_REGION))
PARSE_RELATED_WORDS = False

def get_region():
    # https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/
    regions = {225:"Россия",
               1: "Москва"}
    return regions.get(SELECTED_REGION)


def get_phrases():
    yandex_parsing_init_dir = os.path.join(PROJECT_DIR, "../YandexParsing/init/phrases.txt")
    yandex_parsing_init_file = os.path.join(yandex_parsing_init_dir)
    phrases = get_list(yandex_parsing_init_file)
    return phrases

phrases = get_phrases()


def get_phrase():
    global phrases
    phrase = phrases[0]
    phrases = phrases[1:]
    return phrase

def change_city(driver):
    city_input = driver.find_element_by_id("city__front-input")
    city_input.clear()
    city_input.send_keys(get_region())
    city_input.send_keys(Keys.PAGE_DOWN)
    sleep(2)
    city_input.send_keys(Keys.ENTER)

def send_phrase_to_search(driver, phrase):
    text_input_field = driver.find_element_by_xpath("//input[@name='text']")
    text_input_field.clear()
    text_input_field.send_keys(phrase)
    text_input_field.send_keys((Keys.ENTER))

def remove_garbage(parsed_links):
    parsed_links = [element for element in parsed_links if ("yabs" not in element)
                    and ("market.yandex.ru" not in element)
                    and ("yandex.ru/video/" not in element)
                    and ("yandex.ru/images/" not in element)
                    and ("www.youtube") not in element]
    return parsed_links



YANDEX_PARSING_LOG_PARTICLE = "../YandexParsing/log/"



def collect_links(driver):
    parsed_webdriver_links = driver.find_elements_by_xpath("//a[contains(@class, 'organic__url')]")

    parsed_links = [element.get_attribute("href") for element in parsed_webdriver_links]

    parsed_links = remove_garbage(parsed_links)

    return parsed_links

def go_to_next_page(driver):
    sleep(3)
    next_page_link = driver.find_element_by_xpath('//a[text()="дальше"]')
    next_page_link.click()


def collect_related_items(driver):
    sleep(2)
    related_items = driver.find_elements_by_class_name("related__item")

    related_item_list = [element.text for element in related_items]

    return related_item_list

def prepare_csv(phrase, a_list):
    # Мы спарсили данные и создали из них списк. Но каждый элемент этого списка должен
    # быть связан с фразой, которую вводили в поиск. Поэтому делаем csv.

    result_list = ['"{}";"{}"'.format(phrase, element) for element in a_list]

    return result_list

def get_highlighted_words(driver):
    bold_elements = driver.find_elements_by_tag_name("b")
    bold_elemen_list = [element.text for element in bold_elements if
                        element.text
                        and (element.find_element_by_xpath("..").tag_name != "a")
                        and element.text.strip() != "..."]
    return bold_elemen_list

def handle_phrase(phrase):

    while True:
        try: # Транзакция.
            driver = get_driver()
            driver.get("https://yandex.ru/tune/geo/?retpath=https%3A%2F%2Fwww.yandex.ru%2F%3Fdomredir%3D1%26text%3D%25D0%25BA%25D1%2583%25D0%25BF%25D0%25B8%25D1%2582%25D1%258C%2520%25D0%25BA%25D0%25BE%25D0%25BC%25D0%25BF%25D1%258C%25D1%258E%25D1%2582%25D0%25B5%25D1%2580%26lr%3D213%26domredir%3D1&nosync=1")
            change_city(driver)

            for i in range(PAGES_TO_PARSE):
                if i == 0:
                    send_phrase_to_search(driver, phrase)

                sleep(3)
                parsed_links_tmp = collect_links(driver)

                print("parsed_links")
                # link_log_file = "{}.csv".format(SELECTED_REGION)
                parsed_links = prepare_csv(phrase, parsed_links_tmp)

                write_list_to_file(parsed_links, ENCODING, RESULT_FILE)

                print("highlited_words")
                highlited_words_log_file = "{}_highlighted.csv".format(SELECTED_REGION)
                highlited_words_tmp = get_highlighted_words(driver)
                highlited_words = prepare_csv(phrase, highlited_words_tmp)
                full_path_to_highlited_words_file = os.path.join(LOGS_DIR, highlited_words_log_file)

                write_list_to_file(highlited_words, ENCODING, full_path_to_highlited_words_file)

                if PARSE_RELATED_WORDS:
                    print("tmp_related_item")
                    tmp_related_item_list = collect_related_items(driver)
                    related_item_list = prepare_csv(phrase, tmp_related_item_list)

                    print("related_items")
                    related_items_log_file = "{}_related_items.csv".format(SELECTED_REGION)
                    full_path_to_log_file = os.path.join(LOGS_DIR, related_items_log_file)
                    write_list_to_file(related_item_list, ENCODING, full_path_to_log_file)

                print("go_to_next_page")
                go_to_next_page(driver)

            log_file = os.path.join(LOGS_DIR, "{}_last_phrase.txt".format(SELECTED_REGION))
            write_phrase_to_log(phrase=phrase, write_mode='a', enc=ENCODING, full_path_to_file=log_file)
            driver.quit()
            break
        except Exception as e:
            print(e)
            driver.quit()
            handle_phrase(phrase)

def parse_yandex(counter=0):
    clear_files(LOGS_DIR)

    while phrases:
        phrase = get_phrase()
        handle_phrase(phrase)

parse_yandex()





