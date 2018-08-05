# words = """клапан
# летающ
# достоин
# дрянь
# выглядит
# мусульман
# нагрудн
# одноразов
# палех
# гжел
# пластик"""

words = """потол
светоди
зажиг
ссср
советск
лфз
ленинград
императ"""

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