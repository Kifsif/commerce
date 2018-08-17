from itertools import product
import os
from general.general import get_current_dir, write_phrase_to_log, clear_files

PATH_PARTICLE = "../SeoCombinator/"
INIT_PATH_DIR = PATH_PARTICLE + "Init/"
RESULT_PATH_DIR = os.path.join(PATH_PARTICLE, "Result")
RESULT_FILE_PATH = os.path.join(RESULT_PATH_DIR,"result.txt")
FILE_ENCODING = 'windows-1251'

INIT_DIR = os.path.join(get_current_dir(), INIT_PATH_DIR)

file_list = os.listdir(INIT_DIR)

PLUS_WORDS = []
MINUS_WORDS = []
PHRASES = []
VARIANTS = []

def handle_csv_with_one_list(csv_list_from_reader):
    # Файлы с общими плюс- и минус-словами содержат только одну строку.
    tmp_list = csv_list_from_reader[0]
    tmp_list = delete_empty_values(tmp_list)
    return tmp_list

def delete_empty_values(a_list):
    # Нулевой элемент в списке phrases содержит признак необходимости парсинга лесенкой.
    # Поэтому нулевые элементы в списке не чистим от пустых значений.
    # Есть риск, что на других листах нулевой элемент незаполнен, но это не контролируем:
    # это проверяется в экселе, а изменение CSV-файлов по пути до комбинатора - ответственность пользователя.

    return [a_list[0], *filter(None, a_list[1:])]

def delete_empty_values_from_multidimensional_list(a_list):
    tmp_list = [delete_empty_values(current_list) for current_list in a_list]
    return tmp_list

def prepare_lists():
    for f in file_list:
        with open(os.path.join(INIT_DIR, f), encoding=FILE_ENCODING) as csvfile:
            import csv
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv_data = list(csv_reader)

            if "plus" in f:
                global PLUS_WORDS
                PLUS_WORDS = handle_csv_with_one_list(csv_data)
            elif "minus" in f:
                global MINUS_WORDS
                MINUS_WORDS = handle_csv_with_one_list(csv_data)
            elif "phrases" in f:
                global PHRASES
                tmp_csv = delete_empty_values_from_multidimensional_list(csv_data)
                PHRASES = tmp_csv
            else:
                assert "variants" in f
                global VARIANTS
                tmp_csv = delete_empty_values_from_multidimensional_list(csv_data)
                VARIANTS = tmp_csv

def get_variants(a_string):
    for a_list in VARIANTS:
        if a_string.casefold() in (elem.casefold() for elem in a_list):
            return a_list
            pass # Отладка
        assert a_list is not None

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

def write_upstairs(a_string):
    # Записать в результирующий файл однословники лесенкой.

    all_variants = get_variants(a_string)
    phrases, minus_words = separate_phrases_and_minus_words(all_variants)

    minus_words_str = " ".join(minus_words)

    for phrase in phrases:
        for i in range(2, 8): # Однословники не нужны, поэтому стартуем с 2. Wordstat принимает не более 7 слов. Поэтому с 2 до 8.
            tmp_result = (phrase + " ") * i # Образуется лишний технический пробел в конце.
            tmp_result = '{symb}{phr}{symb} {minus}'.format(symb='"',
                                                            phr=tmp_result[:-1], # Не включаем технический пробел.
                                                            minus=minus_words_str)
            write_phrase_to_log(phrase=tmp_result,
                                write_mode='a',
                                enc=FILE_ENCODING,
                                full_path_to_file=RESULT_FILE_PATH)

def combine_phrases_and_minus_words(phrases, minus_words_list):
    result_list = []
    for phrase in phrases:
        result_list.append(list(phrase) + minus_words_list)
    return result_list

def write_list_to_file(result_phrases_list):
    for phrase in result_phrases_list:
        tmp_str = " ".join(phrase)
        write_phrase_to_log(phrase=tmp_str, write_mode="a", enc=FILE_ENCODING, full_path_to_file=RESULT_FILE_PATH)

def combine_variants(phrase):
    result_phrases_list = []
    result_minus_list = []
    upstairs_flag = phrase[0] # Получим флаг необходимости парсинга лесенкой. Он всегда в нулевом элементе.

    phrase_without_upstairs_flag = phrase[1:] # Нулевой элемент не берем, т.к. он содержит флаг парсинга лесенкой.

    for current_key in phrase_without_upstairs_flag:
        dirty_variants = get_variants(current_key)
        variants, minus_words = separate_phrases_and_minus_words(dirty_variants)

        if upstairs_flag:
            write_upstairs(current_key)

        result_phrases_list.append(variants)
        result_minus_list += minus_words

    cartesian_production = list(product(*result_phrases_list))
    result_phrases_list = combine_phrases_and_minus_words(phrases=cartesian_production, minus_words_list=result_minus_list)
    write_list_to_file(result_phrases_list)

clear_files(RESULT_PATH_DIR)
prepare_lists()
for phrase in PHRASES:
    combine_variants(phrase)

