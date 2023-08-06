# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrsub']

package_data = \
{'': ['*']}

install_requires = \
['jtran>=0.2.13,<0.3.0', 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'jrsub',
    'version': '0.1.10',
    'description': 'Python package for working with Warodai and Yarxi dictionaries',
    'long_description': '# JRSub\n[![PyPI](https://img.shields.io/pypi/v/jrsub.svg)](https://pypi.python.org/pypi/jrsub)\n[![Build Status](https://travis-ci.com/kateabr/jrsub.svg?branch=master)](https://travis-ci.com/kateabr/jrsub)\n\n## Установка\n\n`pip install jrsub`\n\n## Использование\n\n### Загрузка ранее сгенерированной словарной базы\n\n#### ЯРКСИ\n```\nyl = YarxiLoader() // экземпляр загрузчика\nyd = yl.load() // словарь\n```\n#### Warodai\n```\nwl = WarodaiLoader() // экземпляр загрузчика\nwd = wl.load() // словарь\n```\n\n### Поиск в словарях\n\n`yd.lookup(lexeme: str[, reading: str, search_mode: SearchMode])` → `[SearchResult]`\n* возвращает список `SearchResult`, включающих в себя поля `lexeme`, `reading` и `translation` из подходящих записей;\n* все три поля являются списками строк.\n\n`yd.lookup_translations_only(lexeme: str[, reading: str, search_mode: SearchMode])`→ `[str]`\n* возвращает значения полей "перевод" из подходящих записей в виде одномерного списка строк.\n\nПараметр | Допустимые значения | Обязательный параметр\n------------ | ------------- | ------------\n`lexeme` | хирагана, катакана, кандзи | ✔️\n`reading` | хирагана | ❌\n`search_mode` | `SearchMode.consecutive`, `SearchMode.deep_only`, `SearchMode.shallow_only` | ❌\n\n* `SearchMode.shallow_only`: поиск осуществляется только по исходным формам, дословно приведенным в словаре. Малейшие изменения в слове (например, лишние символы окуриганы или их отсутствие) приведут к пустой выдаче словаря.\n\n* `SearchMode.deep_only`: задает "глубокий" режим поиска: при поиске в первую очередь учитываются входящие в слово иероглифы. Этот режим работает медленнее, чем `SearchMode.shallow_only`, но при этом он гораздо надежнее.\n\n* `SearchMode.consecutive` (_задан по умолчанию_): вначале запускается "поверхностный поиск", а затем, если он не дал результатов, -- "глубокий". Это оптимальный из всех трех вариантов, лучше его не изменять.\n\n---\n### Пересборка словарных баз\n\n#### Методы загрузчиков\n\nДействие  | Метод | Аргументы | Начальное значение\n----------|-------|-----------|------------------------\nВключение/откючение транслитерации примеров в переводах | `.enable_transliteration` | mode: `bool` | `True` (включено)\nИзменение префикса к переводам, свойственным иероглифам в составе сложных слов _(только для ЯРКСИ)_ | `.set_compounds_pref` | pref: `str` | `\'〈в сочет.〉\'`\nИзменение способа выделения некоторых частей перевода | `.set_highlighting` | left: `str`; right: `str` | `\'《\'`; `\'》\'`\nЗапуск перестройки словарной базы | `.rescan` | path: `str`; show_progress: `bool` | папка `dictionaries/source` в каталоге установки пакета; `True`\n\n* Для отображения в браузере можно при помощи `set_highlighting` заменить кавычки-елочки на HTML-теги: `yl.set_highlighting(\'<i>\', \'</i>\')`;\n* Перестройка одной базы занимает около восьми минут: полосы прогресса позволяют отследить, на какой стадии база находится в данный момент.\n* При перестройке рекомендую использовать отредактированные мной варианты исходников, доступные в репозитории в каталоге [`dictionaries/source`](https://github.com/kateabr/jrsub/tree/master/dictionaries/source) (список изменений в [`Яркси`](https://docs.google.com/spreadsheets/d/1oUPO1zTyYWZdhC4T_DKzlWpR9B4NBnw16mv5vycp4TM/edit?usp=sharing) | [`Вародае`](https://docs.google.com/spreadsheets/d/1sU5ihleVZlBVRimYV_NM5TWq0lH_n68cEJx60iRdjTM/edit?usp=sharing); в основном изменения касаются форматирования, но также было найдено и исправлено несколько опечаток).\n\n#### Методы полученных после сборки словарных баз\n\nДействие  | Метод | Аргументы | Значение по умолчанию\n----------|-------|-----------|------------------------\nСохранение перестроенной базы | `.save` | path: `str` | папка `dictionaries` в каталоге установки пакета\n\n* Если оставить значение пути по умолчанию, база будет сохраняться в установочный каталог пакета, и при следующем запуске к ней можно будет получить доступ методом загрузчика `.load()` без параметров.\n\n---\n### Примеры работы со словарями ([`demo`](https://github.com/kateabr/jrsub/tree/master/demo))\n* `cli.py` -- самый простой пример взаимодействия через командную строку;\n* `app.py` -- веб-интерфейс для работы через браузер;\n* `flask.Dockerfile` -- docker-контейнер с приложением из файла `app.py`.',
    'author': 'Ekaterina Biryukova',
    'author_email': 'kateabr@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kateabr/jrsub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
