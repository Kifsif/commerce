import os

def get_current_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../")

def get_list(full_path_to_file):

    with open(full_path_to_file, "r") as f:
        elements = f.read().splitlines()

    return elements