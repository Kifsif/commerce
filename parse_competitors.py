from general.general import get_current_dir, clear_files
from general.drv import send_proxy_to_black_set
import os
from bs4 import BeautifulSoup
from general.drv import get_proxy
import requests
from requests.exceptions import ProxyError
from general.general import write_phrase_to_log

LINK_COL = 1 # В какой колонке в csv-файле находится ссылка. Начинть с 0.



PARSING_PATH_PARTICLE = os.path.join(get_current_dir(), "../ParseCompetitors/")
INIT_PATH_PARTICLE = PARSING_PATH_PARTICLE + "Init/"
INIT_DIR = os.path.join(get_current_dir(), INIT_PATH_PARTICLE)
RESULT_DIR = os.path.join(PARSING_PATH_PARTICLE, "Log")
RESULT_FILE = os.path.join(RESULT_DIR, "result.csv")
READ_FILE_ENCODING = 'utf-8'
WRITE_FILE_ENCODING = 'windows-1251'


def prepare_link_list(file_list):

    for f in file_list:
        with open(os.path.join(INIT_DIR, f), encoding=READ_FILE_ENCODING) as csvfile:
            import csv
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv_data = list(csv_reader)
    return csv_data

def get_files(dir):
    file_list = os.listdir(INIT_DIR)
    return file_list

def get_meta_content(a_list):
    tmp_list = [element.attrs.get("content").strip() for element in a_list]
    tmp_str = "||".join(tmp_list)
    return tmp_str

def get_tags(a_list):
    tmp_list = [element.text.strip() for element in a_list]
    tmp_str = "||".join(tmp_list)
    return tmp_str

def get_alts(a_list):
    pass
    return ""

def get_data_from_competitor(a_link):
    html = get_html(a_link)
    if not html: # Не смогли ничего спарсить у этого конкурента.
        return None
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.title.text

    keywords_set = soup.findAll("meta",  attrs={"name":"keywords"})
    keywords = get_meta_content(keywords_set)

    description_set = soup.findAll("meta",  attrs={"name":"description"})
    descriptions = get_meta_content(description_set)

    h1_list = soup.findAll("h1")
    h1_s = get_tags(h1_list)

    h2_list = soup.findAll("h2")
    h2_s = get_tags(h2_list)

    h3_list = soup.findAll("h3")
    h3_s = get_tags(h3_list)

    h4_list = soup.findAll("h4")
    h4_s = get_tags(h4_list)

    alt_list = soup.findAll("img", alt=True)
    alts = get_alts(alt_list)

    return title, keywords, descriptions, h1_s, h2_s, h3_s, h4_s, alts



def get_html(a_url, counter=0):
    current_proxy = get_proxy()
    proxies = {'http': 'http://{}'.format(current_proxy)}

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }

    max_number_of_attempts = 10

    if counter == max_number_of_attempts:
        return None

    try:
        response = requests.get(a_url, headers=headers, proxies=proxies)
    except ProxyError as e:
        print("Bad proxy: {}".format(proxies))
        print(e)
        send_proxy_to_black_set(current_proxy)
        get_html(a_url)
    except requests.exceptions.RequestException as e:
        print("{}: {}: {}".format(a_url, current_proxy, e))
        counter += 1
        get_html(a_url, counter)

    if response.status_code != 200:
        print("{}: {}".format(a_url, response.status_code))
        counter += 1
        get_html(a_url, counter)

    html = response.text

    return html

def convert_list_into_csv_line(a_list):
    tmp_str = ";".join(a_list)
    return tmp_str

def handle_link_list(link_list):
    for a_line in link_list:
        current_link = a_line[LINK_COL]

        try:
            title, keywords, descriptions, h1_s, h2_s, h3_s, h4_s, alts \
                = get_data_from_competitor(current_link)
        except Exception as e: # Не смогли спарсить у этого конкурента.
            print(e)
            continue

        for element in [title, keywords, descriptions, h1_s, h2_s, h3_s, h4_s, alts]:
            a_line.append(element)

        csv_line = convert_list_into_csv_line(a_line)
        write_phrase_to_log(phrase=csv_line,
                            write_mode='a',
                            enc=WRITE_FILE_ENCODING,
                            full_path_to_file=RESULT_FILE)
        pass

def create_csv_titles():
    csv_line = "Query;Url;title;keywords;descriptions;h1_s;h2_s;h3_s;h4_s;alts"
    write_phrase_to_log(phrase=csv_line,
                        write_mode='a',
                        enc=WRITE_FILE_ENCODING,
                        full_path_to_file=RESULT_FILE)

def parse_competitors(dir):
    clear_files(RESULT_DIR)
    create_csv_titles()
    file_list = get_files(dir)
    link_list = prepare_link_list(file_list)
    handle_link_list(link_list)

parse_competitors(INIT_DIR)
