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

result_file_dir = os.path.join(current_dir, "../ConvertedFiles")

clear_files(result_file_dir)

result_file = os.path.join(result_file_dir, 'result.csv')

file_list = glob.glob(source_files_mask)

def convert():
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

                with codecs.open(result_file, 'a', encoding=WRITE_ENCODING) as w_file:
                    try:
                        w_file.write(line)
                    except UnicodeEncodeError:
                        pass # Поставить точку останова. Анализировать причину в каждом конкретном случае.
                        continue
                    print("{}:{}".format(counter, line))
                    counter += 1

convert()