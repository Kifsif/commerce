from itertools import product
import os
from general.general import get_current_dir


PATH_PARTICLE = "../SeoCombinator/"
INIT_PATH_PARTICLE = PATH_PARTICLE + "Init/"

INIT_DIR = os.path.join(get_current_dir(), INIT_PATH_PARTICLE)

file_list = os.listdir(INIT_DIR)


def prepare_lists():
    for f in file_list:
        with open(os.path.join(INIT_DIR, f), encoding='windows-1251') as csvfile:
            import csv
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv = list(csv_reader)

            pass



prepare_lists()
