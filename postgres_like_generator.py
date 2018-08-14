words = """ставит
кирпич
нижегород
отлив
ифз
виком
подержан
мерцающ
создан
медово
берц
мера
нефрит
чернеет
треск
масса
иеромон
методика
подним
неман
правосл
сломал
стандарт
венге
pavone
рису
"""


words_list = words.strip() # Убрать переносы строк после последнего значимого слова.
words_list = words_list.split('\n')

start_part = "from phrases where title ilike any (array["
end_part = "]);"

middle_part = ""

for word in words_list:
    middle_part += "'%{}%',".format(word)

middle_part = middle_part[:-1]

print("select * {}{}{}".format(start_part, middle_part, end_part))
print("delete {}{}{}".format(start_part, middle_part, end_part))
pass