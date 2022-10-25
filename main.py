def indexOfLast(string, char):
    index = 0
    for i in range(0, len(string)):
        if string[i : i+1] == char:
            index = i
    return index-1

class русКод:
    культурные_слова = {
        'типа': "==",
        'меньше': "<",
        'больше': ">",
        'большеравно': "=>",
        'меньшеравно': "=<",
        'то': ":",
        'делать': ":",
        'если': "if",
        'илиесли': "elif",
        'иначе': "else :",
        'пока': "while",
        'для': "for",
        'глобал': "global",
        'в': "in",
        'правда': "True",
        'ложь': "False",
        'функция': "def",
        'вернуть': "return",
        'сказать': "print",
        'сдохнуть': "exit",
        'это': "=",
        'из': "from",
        'импорт': "import",
        'неравно': "!="
    }


    def __init__(self, режим, табов, файл):
        self.режим = режим
        self.табов = табов
        self.файл = файл

    def транслировать_строку(self, строка):
        культурный_слова = self.культурные_слова
        строка = строка.replace("	", "")
        транслированная_строка = ""
        for слово in строка:
            слово.replace(" ", "")
            if "(" in слово:
                транслированная_строка += self.транслировать_строку(слово[слово.index("(") : indexOfLast(слово, ")")])
            if слово in культурный_слова:
                слово = слово.replace("(", "").replace(")", "")
                транслированная_строка += культурный_слова[слово] + " "
            else:
                транслированная_строка += слово + " "

        return транслированная_строка


    def транслировать(self):
        культурный_слова = self.культурные_слова
        код = open(self.файл, 'r', encoding='utf-8')
        print(f"> код = open(self.файл, 'r', encoding='utf-8')")
        культурный_код = ""
        линия = 0
        print("-"*50)
        for чота in код.readlines():
            линия += 1
            if чота.endswith("\n"):
                чота = чота[0:-1]
            print(f">>{чота}")
            культурный = ""
            if чота.startswith("#"):
                культурный_код += ("    " * self.табов) + чота + "\n"
                continue
            if чота == "":
                культурный_код += ("    " * self.табов) + "\n"
                continue
            for слово in чота.split(" "):
                ориг_слово = слово
                табов = слово.count("	")
                пробелов = слово.count("    ")
                self.табов = max(табов, пробелов)
                #слово = слово.replace("	", "")
                культурный += self.транслировать_строку(слово)
            культурный_код += ("    " * self.табов) + культурный + "\n"
        print(f"{'СОХРАНЕНИЕ ФАЙЛА':-^50}")
        выход = open(self.файл + ".py", 'w', encoding='utf-8')
        выход.write(культурный_код)
        выход.close()
        print(f"> выход = open(self.файл + \".py\", 'w', encoding='utf-8')")
        print(f"> выход.write(транслированный_код)")
        print(f"> выход.close()")

        print(f"{'ГОТОВО':-^50}")


файл = input("Введите имя файла: ")
print(f"{'ЗАГРУЗКА ТРАНСЛЯТОРА':-^50}")
транслятор = русКод("файл", 0, f"./{файл}")
print(f'> транслятор = русКод("файл", 0, "./{файл}")')
print(f"{'ТРАНСЛЯЦИЯ КОДА':-^50}")
print(f'> транслятор.транслировать()')
транслятор.транслировать()

print(транслятор.транслировать_строку("сказать(тест(1+1))"))
