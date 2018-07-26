import urllib
from general.general import get_list, get_current_date, add_phrase_in_log
from time import sleep
from general.drv import get_driver

import random
import os

BUKVARIX_DIR = "/home/michael/PycharmProjects/Bukvarix/"

current_date = get_current_date()

phrase_list = get_list(os.path.join(BUKVARIX_DIR, "Init/word_list.txt"))
log_file = os.path.join(BUKVARIX_DIR, "Log/{}.txt".format(current_date))

BUNCH_SIZE = 100

import requests

def pop_bunch():
    global phrase_list
    counter = 0

    phrase_bunch = ""

    while phrase_list and counter < 100:
        current_phrase = "{}\n".format(phrase_list.pop(0))
        phrase_bunch += current_phrase
        counter +=1

    return phrase_bunch


def get_minus_words():
    minus_words = """авито
метро
м видео
эльдорадо
детский мир
магнит
ситилинк
avito
озон
юлмарт
aliexpress
wildberries
мвидео
биглион
хофф
экзист
максидом
ebay
бутик
metro
технопарк
ozon
mvideo
али экспресс
амазон
утконос
медиамаркт
выгода
таобао
citilink
техпорт
олди
technopoint
eldorado
топ шоп
купикупон
oldi
taobao
ulmart
васко
детмир
onlinetrade
е5
купинатао
майшоп
holodilnik
e96
mediamarkt
молоток ру
младенец ру
utkonos
тао бао
вайлберис
алиэкспрес
вкусный
molotok
ебэй
купи на тао
медиамарт
самостоятельно
самостоятельный
сам
своими руками
своими силами
собственными силами
собственными руками
индивидуально
индивидуальный
персонально
персональный
лично
личный
в домашних условиях
дома
на дому
сделай сам
как сделать
как изготовить
как приготовить
научись делать
научись готовить
научитесь делать
научитесь готовить
обучайтесь делать
обучайся делать
обучайтесь готовить
обучайся готовить
как готовить
технология
техника
мастер класс
видео урок
видео
урок
тренинг
инструкция
рекомендация
руководство
мануал
рецепт"""

    return minus_words

def parse(phrase_bunch):

    while True:
        try: # Транзакция. Если хоть что-нибудь пошло не так, начинаем все сначала.
            driver = get_driver()

            driver.get("https://www.bukvarix.com/mkeywords/")

            phrases_field = driver.find_element_by_id("win_in_focus")
            phrases_field.send_keys(phrase_bunch)

            minus_words = get_minus_words()
            minus_words_field = driver.find_element_by_class_name("minus-words")
            minus_words_field.send_keys(minus_words)

            submit_button = driver.find_element_by_xpath("//input[@type='submit']")
            submit_button.click()

            download_button = driver.find_element_by_class_name("report-download-button")
            download_button.click()
            sleep(50)
            driver.quit()
            add_phrase_in_log(phrase_bunch, os.path.join(BUKVARIX_DIR, "Log/log.txt"))
            break
        except:
            parse(phrase_bunch)



def parse_bukvarix():

    while phrase_list:
        phrase_bunch = pop_bunch()
        parse(phrase_bunch)

parse_bukvarix()


