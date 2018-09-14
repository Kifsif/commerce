from itertools import product
import os
from general.general import get_current_dir, write_phrase_to_log, clear_files
import sys
import re


PATH_PARTICLE = "../SeoCombinator/"
INIT_PATH_DIR = PATH_PARTICLE + "Init/"
RESULT_PATH_DIR = os.path.join(PATH_PARTICLE, "Result")
RESULT_FILE_PATH = os.path.join(RESULT_PATH_DIR,"result.txt")
FILE_ENCODING = 'windows-1251'

INIT_DIR = os.path.join(get_current_dir(), INIT_PATH_DIR)

PLUS_WORDS = []
MINUS_WORDS = []
PHRASES = []
VARIANTS = []
WORDSTAT_LIMIT = 7 # Вордстат парсит только 7 слов.

def handle_csv_with_one_list(csv_list_from_reader):
    # Файлы с общими плюс- и минус-словами содержат только одну строку.
    tmp_list = csv_list_from_reader[0]
    return [*filter(None, tmp_list)]


def delete_empty_values(a_list):
    # Нулевой элемент в списке phrases содержит признак необходимости парсинга лесенкой.
    # На всех других листах кроме листов с плюс- и минус-словами этот столбец должен присутствовать, но быть пустым.
    # Поэтому нулевые элементы в списке не чистим от пустых значений.
    # Есть риск, что на других листах нулевой элемент не заполнен пустым значением, но это не контролируем:
    # это проверяется в экселе, а изменение CSV-файлов по пути до комбинатора - ответственность пользователя.

    return [a_list[0], *filter(None, a_list[1:])]

def delete_empty_values_from_multidimensional_list(a_list):
    tmp_list = [delete_empty_values(current_list) for current_list in a_list]
    return tmp_list



def prepare_variants(variants_file_name):
    global VARIANTS

    with open(os.path.join(INIT_DIR, variants_file_name), encoding=FILE_ENCODING) as csvfile:
        import csv
        csv_reader = csv.reader(csvfile, delimiter=';')
        csv_data = list(csv_reader)
        tmp_csv = delete_empty_values_from_multidimensional_list(csv_data)
        VARIANTS = tmp_csv

def separate_variants_and_others(file_names_list):
    # a_list: список имен файлов, один из которых обязательно в имени файлов содержит "variants".
    # Отделить файл с вариантами от остальных файлов, т.к. варианты нужны для подготовки вариантов плюс-слов.
    # Т.е. варианты нужны первым делом.

    variants_file = ""
    other_files = []

    for file_name in file_names_list:
        if 'variants' in file_name:
            variants_file = file_name
        else:
            assert (("minus" in file_name) or ("plus" in file_name) or ("phrases" in file_name))
            other_files.append(file_name)

    return variants_file, other_files



    return tmp_list[0] # Искключение не ловим, т.к. такой
                       # элемент обязательно должен быть (см. комментарий к параметру a_list).


def prepare_variants(file_name):
    with open(os.path.join(INIT_DIR, file_name), encoding=FILE_ENCODING) as csvfile:
        import csv
        csv_reader = csv.reader(csvfile, delimiter=';')
        csv_data = list(csv_reader)
        global VARIANTS
        tmp_csv = delete_empty_values_from_multidimensional_list(csv_data)
        VARIANTS = tmp_csv


def prepare_lists(file_list):
    variants_file, other_files = separate_variants_and_others(file_list)
    prepare_variants(variants_file)


    for f in file_list:
        with open(os.path.join(INIT_DIR, f), encoding=FILE_ENCODING) as csvfile:
            import csv
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv_data = list(csv_reader)

            if "plus" in f:
                global PLUS_WORDS
                tmp_plus_words = handle_csv_with_one_list(csv_data)
                PLUS_WORDS = get_variants_for_plus_words(tmp_plus_words)
            elif "minus" in f:
                global MINUS_WORDS
                MINUS_WORDS = handle_csv_with_one_list(csv_data)
            elif "phrases" in f:
                global PHRASES
                tmp_csv = delete_empty_values_from_multidimensional_list(csv_data)
                PHRASES = tmp_csv


def get_variants_for_string(a_string):
    for a_list in VARIANTS:
        if a_string.casefold() in (elem.casefold() for elem in a_list):
            return a_list
        assert a_list is not None # Сюда не должны попасть. Обязательно вариант должен присутствовать.

def get_variants_for_plus_words(a_list):
    # Получить общий список вариантов плюс-слов (все варианты всех плюс-слов в общую кучу - в один список).

    tmp_result = []

    for element in a_list:
        variants = get_variants_for_string(element)
        tmp_result += variants

    return tmp_result


def separate_phrases_and_minus_words(a_list):
    phrases = []
    minus_words = []
    for element in a_list:
        if element[0] == "-":
            minus_words.append(element)
        else:
            assert element[0] != "-"
            phrases.append(element)
    return phrases, minus_words

def create_list_with_one_element(phrase_list):
    tmp_list = [element for element in phrase_list]
    tmp_list = " ".join(tmp_list)
    tmp_list = tmp_list.split()
    return tmp_list[:WORDSTAT_LIMIT]


def cut_words_to_limit(phrase_list):
    # Проверить, сколько слов во фразе.
    # Если семь или более, вернуть только 7 слов. Лишние слова просто обрезаются.
    number_of_words = count_words_phrases_list(phrase_list)
    if number_of_words > WORDSTAT_LIMIT:
        new_phrase_list = create_list_with_one_element(phrase_list)
        return True, new_phrase_list
    return False, phrase_list

def count_words_phrases_list(phrases_list):
    # Получен список фраз. Например, "["федеративная республика германии", "экономика германии"].
    # Посчитать, сколько всего слов во всех фразах. В данном примере - 5 слов.

    sum = 0
    for phrase in phrases_list:
        tmp_list = phrase.split()
        sum += len(tmp_list)

    return sum

def write_upstairs(a_string):
    # Записать в результирующий файл фразы лесенкой.


    all_variants = get_variants_for_string(a_string)
    phrases, minus_words = separate_phrases_and_minus_words(all_variants)

    minus_words_str = " ".join(minus_words)

    for phrase in phrases:
        for i in range(1, 8): #  Wordstat принимает не более 7 слов.
            tmp_list = [phrase for _ in range(i)]

            if len(tmp_list) == 1: # Однословники не нужны.
                continue

            break_loop, tmp_list = cut_words_to_limit(tmp_list)
            phrase_for_writing = " ".join(tmp_list)
            tmp_result = '{symb}{phr}{symb} {minus}'.format(symb='"',
                                                            phr=phrase_for_writing,
                                                            minus=minus_words_str)

            write_phrase_to_log(phrase=tmp_result,
                                write_mode='a',
                                enc=FILE_ENCODING,
                                full_path_to_file=RESULT_FILE_PATH)

            if break_loop:
                break


def combine_phrases_and_minus_words(phrases, minus_words_list):
    result_list = []
    for phrase in phrases:
        result_list.append(list(phrase) + minus_words_list)
    return result_list

def write_list_to_file(result_phrases_list):
    for phrase in result_phrases_list:
        tmp_str = " ".join(phrase)
        write_phrase_to_log(phrase=tmp_str, write_mode="a", enc=FILE_ENCODING, full_path_to_file=RESULT_FILE_PATH)


def get_plus_words_variants():
    tmp_result = []

    for element in PLUS_WORDS:
        variants = get_variants_for_string(element)
        tmp_result += variants

    return tmp_result


def combine_variants(phrase, parse_plus_words=False):
    # Сначала запишем комбинацию вариантов без плюс-слов, затем рекурсивно вызовем функцию и запишем комбинацию вариантов
    # с плюс-словами.
    result_phrases_list = []

    if parse_plus_words:
        result_phrases_list.append(PLUS_WORDS)

    result_minus_list = []
    upstairs_flag = phrase[0] # Получим флаг необходимости парсинга лесенкой. Он всегда в нулевом элементе.

    phrase_without_upstairs_flag = phrase[1:] # Нулевой элемент не берем, т.к. он содержит флаг парсинга лесенкой.

    for current_key in phrase_without_upstairs_flag:
        dirty_variants = get_variants_for_string(current_key)
        variants, minus_words = separate_phrases_and_minus_words(dirty_variants)

        if upstairs_flag == '1':
            write_upstairs(current_key)

        result_phrases_list.append(variants)
        result_minus_list += minus_words

    cartesian_production = list(product(*result_phrases_list))
    result_phrases_list = combine_phrases_and_minus_words(phrases=cartesian_production, minus_words_list=result_minus_list)
    write_list_to_file(result_phrases_list)

    if not parse_plus_words:
        combine_variants(phrase, parse_plus_words=True)

clear_files(RESULT_PATH_DIR)
prepare_lists(os.listdir(INIT_DIR))
for phrase in PHRASES:
    combine_variants(phrase)

