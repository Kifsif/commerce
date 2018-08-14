import glob
import os
import codecs
from general.general import clear_files

current_dir = os.path.dirname(os.path.abspath(__file__))
source_files_dir = "/home/michael/Downloads/"
source_files_mask = source_files_dir + "*.csv"


# 'utf-8', 'windows-1251'
READ_ENCODING = 'utf-8'
WRITE_ENCODING = 'windows-1251'

result_file_dir = os.path.join(current_dir, "../CombinedFiles")

clear_files(result_file_dir)

result_file = os.path.join(result_file_dir, 'result.csv')

file_list = glob.glob(source_files_mask)

#read input file

def combine(first_column_only = False):
    if first_column_only:
        counter = 1
        for a_file in file_list:
            with codecs.open(a_file, 'r', encoding=READ_ENCODING) as r_file:
                while True:
                    try:
                        line = r_file.readline()
                    except UnicodeDecodeError:
                        continue # Встретилась строка не в кодировке utf. Например, Букварикс может поместить такие строки в конце.
                    if (not line):
                        break
                    try:
                        start_pos = line.index('"')
                        end_pos = line.index('"', start_pos + 1)
                    except ValueError:
                        continue # Кавычка не найдена.


                    with codecs.open(result_file, 'a', encoding=WRITE_ENCODING) as w_file:
                        phrase = line[start_pos+1:end_pos]
                        w_file.write("{}\n".format(phrase))
                        print("{}:{}".format(counter, phrase))
                        counter += 1

    else:

        for a_file in file_list:
            with codecs.open(a_file, 'r', encoding = READ_ENCODING) as file:
                try:
                    lines = file.read()
                except UnicodeDecodeError:
                    continue

            with codecs.open(result_file, 'a', encoding = WRITE_ENCODING) as file:
                try:
                    file.write(lines)
                except UnicodeEncodeError:
                    pass # Поставить точку останова и смотреть в каждом конкретном случае.


combine(first_column_only = False)