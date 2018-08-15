from itertools import product
import os
from general.general import get_current_dir


PATH_PARTICLE = "../SeoCombinator/"
INIT_PATH_PARTICLE = PATH_PARTICLE + "Init/"

INIT_DIR = os.path.join(get_current_dir(), INIT_PATH_PARTICLE)

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
    return [a_list[0], *filter(None, a_list[1:])]

def delete_empty_values_from_multidimensional_list(a_list):
    tmp_list = [delete_empty_values(current_list) for current_list in a_list]
    return tmp_list

def prepare_lists():
    for f in file_list:
        with open(os.path.join(INIT_DIR, f), encoding='windows-1251') as csvfile:
            import csv
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv = list(csv_reader)

            if "plus" in f:
                global PLUS_WORDS
                PLUS_WORDS = handle_csv_with_one_list(csv)
            elif "minus" in f:
                global MINUS_WORDS
                MINUS_WORDS = handle_csv_with_one_list(csv)
            elif "phrases" in f:
                global PHRASES
                tmp_csv = delete_empty_values_from_multidimensional_list(csv)
                PHRASES = tmp_csv
            else:
                assert "variants" in f
                global VARIANTS
                tmp_csv = delete_empty_values_from_multidimensional_list(csv)
                VARIANTS = tmp_csv


prepare_lists()
pass
