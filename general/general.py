import os
import shutil
import datetime

def get_current_date():
    current_date = datetime.date.today().strftime("%Y%m%d")
    return current_date

def clear_files(logs_dir):
    try:
        shutil.rmtree(logs_dir)
    except FileNotFoundError:
        pass # Do nothing

    os.makedirs(logs_dir)

def get_current_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../")

def get_list(full_path_to_file):

    with open(full_path_to_file, "r") as f:
        elements = f.read().splitlines()

    return elements

def write_list_to_file(link_list, enc, full_path_to_file):
    with open(full_path_to_file, "a", encoding=enc) as f:
        for link in link_list:
            f.write("{}\n".format(link))

def write_phrase_to_log(phrase, write_mode, enc, full_path_to_file):
    with open(full_path_to_file, write_mode, encoding=enc) as f:
        try:
            f.write("{}\n".format(phrase))
        except UnicodeEncodeError:
            return # Проблема с кодировкой.

def add_phrase_in_log(phrase, full_path_to_file):
    with open(full_path_to_file, "a") as f:
        f.write("{}\n".format(phrase))