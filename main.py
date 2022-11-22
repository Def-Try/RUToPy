import argparse
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

parser = argparse.ArgumentParser(description='Переводит русский язык в код питона. Вызовите без аргументов для командной строки.')

parser.add_argument('--rf', type=bool, default=False, help='Реформатировать код после трансляции')
parser.add_argument('-f', type=str, default="", help='Файл для трансляции')

args = parser.parse_args()

def indexoflast(string, char):
    index = 0
    for i in range(0, len(string)):
        if string[i: i + 1] == char:
            index = i
    return index


def makebar(i, maxn, width=10):
    percent = i / maxn * 100
    done = round(percent / 100 * width)
    left = round(width - (percent / 100 * width))
    return "[" + ("=" * (done - 1)) + ">" + ("-" * left) + "]                                            "


class РусВПитон:
    культурные_слова = {
        'равно': "==",
        'меньше': "<",
        'больше': ">",
        'большеравно': "=>",
        'меньшеравно': "=<",
        'то': ":",
        'тогда': ":",
        'делать': ":",
        'если': "if",
        'иначеесли': "elif",
        'иначе': "else :",
        'пока': "while",
        'для': "for",
        'глобал': "global",
        'в': "in",
        'диапазон': "range",
        'правда': "True",
        'ложь': "False",
        'функция': "def",
        'вернуть': "return",
        'сказать': "print",
        'вывести': "print",
        'выйти': "exit",
        'это': "=",
        'из': "from",
        'импорт': "import",
        'неравно': "!=",
        ';': "\n",
        'строка': "str",
        'число': "int",
        'флоут': "float",
        'как': "as",
        'или': "or",
        'и': "and",
        'округлить': "round"
    }

    def __init__(self, табов, файлкода):
        self.табов = табов
        self.имя = файлкода
        self.файл = open(файлкода, 'r', encoding='utf-8') if файлкода != "" else ""

    @staticmethod
    def токенизировать(строка):
        токены = []
        # слова = строка.split(" ")
        позиция = -1
        токен = ""
        while позиция < len(строка):
            токен += строка[позиция: позиция + 1]
            позиция += 1
            if строка[позиция: позиция + 1] == " ":
                токены.append(токен)
                токен = ""
                continue
            if строка[позиция: позиция + 1] in "\"":
                токены.append(токен)
                токен = ""
                while позиция < len(строка):
                    позиция += 1
                    токен += строка[позиция: позиция + 1]
                    if строка[позиция: позиция + 1] in "\"":
                        токены.append("\"" + токен)
                        позиция += 1
                        токен = ""
                        break
            if строка[позиция: позиция + 1] in "(":
                токены.append(токен)
                токен = ""
                while позиция < len(строка):
                    позиция += 1
                    токен += строка[позиция: позиция + 1]
                    if строка[позиция: позиция + 1] in ")":
                        токены.append("(" + токен)
                        позиция += 1
                        токен = ""
                        break
        return токены

    def транслировать_строку(self, строка):
        культурный_слова = self.культурные_слова
        строка = строка.replace("	", "")
        строка = строка.replace("	", "")
        транслированная_строка = ""
        токены = self.токенизировать(строка)
        for слово in токены:
            if слово.startswith("\""):
                транслированная_строка += слово
                continue
            if "(" in слово:
                транслированная_строка += "(" + self.транслировать_строку((слово + " ")[1:-1]) + ""
                continue
            слово = слово.replace(" ", "")
            # if len(слово.split(")")) > 1: слово = слово.split(")")[1]
            if слово in культурный_слова:
                транслированная_строка += культурный_слова[слово] + " "
            else:
                транслированная_строка += слово + " "
        return транслированная_строка

    def транслировать(self):
        культурный_код = ""
        линия = 0
        линии = self.файл.readlines()
        for чота in линии:
            print(
                f"\r{линии.index(чота) / len(линии) * 100}% транслировано... " + makebar(линии.index(чота), len(линии),
                                                                                         30), end='')
            линия += 1
            if чота.endswith("\n"):
                чота = чота[0:-1]
            культурный = ""
            if чота.startswith("#"):
                культурный_код += ("	" * self.табов) + чота + "\n"
                continue
            if чота == "":
                культурный_код += "\n"
                continue
            культурный += self.транслировать_строку(чота)
            культурный_код += ("	" * self.табов) + культурный + "\n"
        print("\r100% транслировано... " + makebar(1, 1, 30), end='')
        return культурный_код


if args.rf == False and args.f == "":
    транслятор = РусВПитон(0, f"")
    while True:
        код = input(">>> ")
        if код.endswith("\\"):
            while код.endswith("\\"):
                код += input("... ")

        with stdoutIO() as s:
            exec(транслятор.транслировать_строку(код.replace("\\", "\n")))
        print(s.getvalue())

if args.rf:
    try:
        from autopep8 import fix_code as reformat
    except ModuleNotFoundError:
        reformat = False
        print("Установите модуль autopep8 для очистки кода после трансляции.")
else:
    reformat = False

файл = args.file
try:
    транслятор = РусВПитон(0, f"./{файл}")
    транслированный = транслятор.транслировать()
    выход = open(транслятор.имя + ".py", 'w', encoding='utf-8')
    if reformat:
        выход.write(reformat(транслированный))
    else:
        выход.write(транслированный)
    выход.close()
    print(f"Сохранено как {транслятор.имя}.py")
except FileNotFoundError:
    print("Файл не найден")
except Exception:
    print("Что-то пошло не так")
exit()
'''
функция факториал(н) то \
    если н равно 0 то вернуть 1 \
    иначе вернуть н * факториал(н-1) \
print(факториал(5))
'''
