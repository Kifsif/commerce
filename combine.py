import glob
import os
import codecs
from general.general import clear_files

current_dir = os.path.dirname(os.path.abspath(__file__))
source_files_dir = "/home/michael/Downloads/"
source_files_mask = source_files_dir + "*.csv"

result_file_dir = os.path.join(current_dir, "../CombinedFiles")

clear_files(result_file_dir)

result_file = os.path.join(result_file_dir, 'result.csv')

file_list = glob.glob(source_files_mask)

#read input file
for a_file in file_list:
    with codecs.open(a_file, 'r', encoding = 'windows-1251') as file:
      lines = file.read()

    #write output file
    with codecs.open(result_file, 'a', encoding = 'utf8') as file:
      file.write(lines)