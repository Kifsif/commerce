from general.general import get_list, get_current_dir
from general.drv import get_driver
from general.drv import USE_PROXY
import os

full_path_to_proxy_list = os.path.join(get_current_dir(), "../CommerceParsing/Init/proxy_list.txt")

init_proxy_list = get_list(full_path_to_proxy_list)

def test_proxies():
    for i in range( len(init_proxy_list)):
        driver = get_driver(USE_PROXY)
        driver.get("http://ip-api.com/")

        element = driver.find_element_by_id("qr")
        element_text = element.text
        ip = element_text.split(",")

        region = driver.find_element_by_xpath('//th[text()="Country"]/following-sibling::td').text
        print("{}, {}".format(ip, region))

test_proxies()