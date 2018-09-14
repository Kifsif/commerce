import os
import shutil
import datetime
from pathlib import Path

INSTRUMENTS_DIR = os.path.join(Path.home(), 'Documents/Parsing/')

def get_current_date():
    current_date = datetime.date.today().strftime("%Y%m%d")
    return current_date

def get_current_date_time():
    current_date_time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    return current_date_time


def clear_files(logs_dir):
    try:
        shutil.rmtree(logs_dir)
    except FileNotFoundError:
        pass # Do nothing

    os.makedirs(logs_dir)

def get_current_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../")

def get_list(full_path_to_file, encoding):

    try:
        with open(full_path_to_file, "r", encoding=encoding) as f:
            elements = f.read().splitlines()
    except FileNotFoundError:
        return []

    return elements

def write_list_to_file(link_list, enc, full_path_to_file):
    # if os.path.exists(full_path_to_file):
    #     os.remove(full_path_to_file) # Удалили старый файл.

    with open(full_path_to_file, "a", encoding=enc) as f:
        last_elem = len(link_list)
        for i in range(last_elem):
            if i != (last_elem-1):
                f.write("{}\n".format(link_list[i]))
            else:
                f.write("{}".format(link_list[i]))

def write_phrase_to_log(phrase, write_mode, enc, full_path_to_file):
    with open(full_path_to_file, write_mode, encoding=enc) as f:
        try:
            f.write("{}\n".format(phrase))
        except UnicodeEncodeError:
            return # Проблема с кодировкой.

def add_phrase_in_log(phrase, full_path_to_file):
    with open(full_path_to_file, "a") as f:
        f.write("{}\n".format(phrase))