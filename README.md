# Multiplication bot
Телеграм - бот, который помогает выучить таблицу умножения.

Можно запускать и останавливать бота. Когда он работает, то предлагает перемножить два числа от 1 до 9.

Если пользователь ввел правильный ответ, то предлагает новый пример, если нет - предлагает попробовать ввести ответ еще раз, до тех пор, пока не будет получен правильный ответ.

В качестве ответа принимает только числа, если введен ответ другого формата, то он обязательно сообщит об этом.

## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)

## Запуск проекта

Клонировать репозиторий и перейти в папку с проектом:

```
git clone https://github.com/jullitka/multiplication_bot.git
cd multiplication_bot
```
Cоздать и активировать виртуальное окружение:

```
python -m venv env
```
Для Linux
    ```
    source venv/bin/activate
    ```
    
Для Windows
    ```
    source venv/Scripts/activate
    ```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Зарегистрировать чат-бота в Телеграм

Запустить проект:
```
python multiplication_bot.py
```
## Авторы
[Юлия Пашкова](https://github.com/Jullitka)
