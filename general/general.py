import os

PARSING_PATH_PARTICLE = "../CommerceParsing/"
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"

def get_current_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../")

def get_list(current_list):
    source_file = get_current_dir() + INIT_PATH_PARTICLE + current_list

    with open(source_file, "r") as f:
        elements = f.read().splitlines()

    return elements