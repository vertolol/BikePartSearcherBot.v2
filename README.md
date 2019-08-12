# Бот для Telegram

Бот для поиска запчастей для велосипеда, с сортировкой по цене. 
В процессе поиска можно выбрать сайты по которым будет произведен поиск. Список доступных сайтов [stores.py](https://github.com/vertolol/BikePartSearcherBot.v2/blob/master/static_data/stores.py),
Далее выбирается категория для поиска, и ввод названия детали.
Написан на Python3.7, с использованием библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)


## Подготовка к использованию
Скопируйте свой токен, в переменную TOKEN в файле [TOKEN.py]()

## Описание файлов и директорий
### [main.py](https://github.com/vertolol/BikePartSearcherBot.v2/blob/master/main_t_b.py)
Запускает бота.
Обработка событий:
- */start* — запускает процесс поиска детали;
- */help* — отправляет сообщение с описанием функционала и поддерживаемыми командами. 

При прерывании процесса поиска (напр. пользователь вместо нажатия на кнопку клавиатуры отправляет сообщение), бот отправляет сообщение об ошибке поиска.

### [static_data](https://github.com/vertolol/BikePartSearcherBot.v2/tree/master/static_data)
Включает в себя список сайтов, названия категорий и примеры названий деталей для поиска.

### [service_code](https://github.com/vertolol/BikePartSearcherBot.v2/tree/master/service_code)
Обработчики для извлечения информации о кодах категорий с сайтов.

### [spiders](https://github.com/vertolol/BikePartSearcherBot.v2/tree/master/spiders)
Обработчики для извлечения информации о конкретной детали.

#### [baseSpider.py](https://github.com/vertolol/BikePartSearcherBot.v2/blob/master/spiders/baseSpider.py)
Базовый класс обработчиков, описывает алгоритм поиска информации о детали.
Дочерние классы описывают названия элементов (разметки HTML, либо словари если это json) в которых находится необходимая информация о детали

#### [spiders_launcher.py](https://github.com/vertolol/BikePartSearcherBot.v2/blob/master/spiders/spiders_launcher.py)
Создает и запускает экземпляры обработчиков