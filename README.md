# RUToPy
Translator of russian language into python

# Examples
```
функция факториал(число) то
    если число типа 0 то вернуть 1
    иначе вернуть число * факториал(число-1)

вывести(факториал(5))
```
->
```py
def факториал ( число ): 
    if число == 0 : return 1 
    else : return число * факториал ( число-1 )

print ( факториал ( 5 ))
```

```
импорт math как матем
для угол в диапазон(0, 30) делать
    вывести(матем.sin(угол))
```
->
```py
import math as матем
for угол in range(0, 30) :
    print ( матем.sin(угол) )
```
