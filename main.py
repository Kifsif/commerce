# from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver = Firefox()
driver = Chrome()
driver.implicitly_wait(120)
driver.set_page_load_timeout(120)
driver.get('https://tools.pixelplus.ru/')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
assert "Пиксель Тулс — бесплатные SEO-инструменты, программы и сервисы для SEO-анализа сайта и продвижения" in driver.title, "Заголовок не тот"
login_button = driver.find_element_by_xpath("//a[@href='/user/login']")
login_button.click()
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys

# assert "Вход в сервис — Пиксель Тулс" in driver.title
#sleep(30)

# try:
#     element = WebDriverWait(driver, 70).until(
#         EC.presence_of_element_located((By.ID, "inputEmail"))
#     )
#     pass
# finally:
#     print("inputEmail is absent.")
#     driver.quit()
#     exit()

# sleep(5)
current_cay = datetime.date.today().strftime("%d-%m-%Y")

input_email_field = driver.find_element_by_id("inputEmail")
input_email_field.send_keys("nonverbis13@yandex.ru")

input_email_field = driver.find_element_by_id("inputPassword")
input_email_field.send_keys("goskomstat")

login_button = driver.find_element_by_xpath("//input[@type='submit']")
login_button.click()

driver.get("https://tools.pixelplus.ru/tools/geo")

requests_field = driver.find_element_by_id("requests")
requests_field.send_keys("""статуэтка
статуэтка аист
статуэтка ангел купить
статуэтка ангел с крыльями
статуэтка ангелы пара
статуэтка артемида богиня охоты купить
статуэтка афина паллада купить
статуэтка афины
статуэтка африка
статуэтка африканка
статуэтка африканка полистоун
статуэтка белый медведь
статуэтка богини
статуэтка богини правосудия
статуэтка богиня победы ника
статуэтка богиня правосудия фемида
статуэтка богиня фемида
статуэтка бронза
статуэтка бронза купить
статуэтка бронза лошадь
статуэтка бронза фемида
статуэтка будда большая
статуэтка будда бронза
статуэтка будды
статуэтка будды купить
статуэтка будды цена
статуэтка бык
статуэтка в виде собаки
статуэтка верблюд купить
статуэтка верблюда
статуэтка влюбленная пара купить
статуэтка влюбленные
статуэтка влюбленные фарфор
статуэтка воин
статуэтка гермес
статуэтка голова коня
статуэтка голова лошади
статуэтка голова фараона
статуэтка гусь
статуэтка гусь купить
статуэтка дама
статуэтка два лебедя
статуэтка два лебедя купить
статуэтка девочка
статуэтка девочка гипс
статуэтка девушка
статуэтка девушка с конем
статуэтка девушка с птицей
статуэтка дельфин
статуэтка дети
статуэтка детский сад
статуэтка для украшений
статуэтка дом
статуэтка дракон с жемчужиной
статуэтка дракона
статуэтка дракона из бронзы
статуэтка дракона купить
статуэтка дракона цена
статуэтка жаба
статуэтка жаба с монетой купить
статуэтка жар птица купить
статуэтка женщина
статуэтка жираф
статуэтка журавля купить
статуэтка зевс
статуэтка йорка купить
статуэтка йоркширский терьер
статуэтка кенгуру
статуэтка керамика
статуэтка клоун
статуэтка клоун фарфор
статуэтка колесница
статуэтка конь
статуэтка конь бронза купить
статуэтка конь на дыбах
статуэтка конь цена
статуэтка коня купить
статуэтка кота
статуэтка котик
статуэтка кошка белая
статуэтка кошка лежащая
статуэтка кошка напольная
статуэтка кошка фарфор
статуэтка кошки
статуэтка кошки в доме
статуэтка красного цвета
статуэтка курица
статуэтка лебеди на свадьбу
статуэтка лебедь
статуэтка леопард
статуэтка леопард цена
статуэтка лисичка
статуэтка лошадь
статуэтка лошадь большая
статуэтка лягушка
статуэтка лягушка большая
статуэтка лягушка купить
статуэтка медведь
статуэтка медведь купить
статуэтка медведь цена
статуэтка мудрости""")

# download_results_checkbox = driver.find_element_by_xpath("//span[@text='Получить результаты в виде CSV-файла']")
# download_results_checkbox_ancestor = download_results_checkbox.find_element_by_xpath(".//ancestor::div");
# download_results_checkbox_ancestor.click()

# download_results_checkbox = driver.find_element_by_class_name("jq-checkbox")
# download_results_checkbox = driver.find_element(By.XPATH, '//span[text()="csv"]')
download_results_checkbox = driver.find_element(By.XPATH, '//span[text()="Получить результаты в виде CSV-файла"]')
sleep(1)
download_results_checkbox.click()

# check_button = driver.find_element_by_xpath("//input[@type='submit']")
sleep(1)
check_button =  driver.find_element_by_xpath("//input[@value='Проверить']")
check_button.click()
sleep(180)
pass