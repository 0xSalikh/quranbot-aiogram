# Quranbot
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Hits-of-Code](https://hitsofcode.com/github/blablatdinov/quranbot-aiogram)](https://hitsofcode.com/github/blablatdinov/quranbot-aiogram/view)
![Custom badge](https://img.shields.io/endpoint?style=flat&url=https%3A%2F%2Fquranbot.ilaletdinov.ru%2Fapi%2Fv1%2Fusers%2Fcount-github-badge%2F)

(Пока находится в тестовом режиме)

[Документация](docs)

Функционал:
 - Каждое утро, вам будут приходить аяты из Священного Корана.
 - При нажатии на кнопку **Подкасты**, вам будут присылаться проповеди с сайта umma.ru.
 - В боте вы можете получать время намаза
 - Доступен поиск по ключевым словам

Также вы можете отправить номер суры, аята (например **4:7**) и получить: аят в оригинале, перевод на русский язык, транслитерацию и аудио

Ссылка на бота: [Quran_365_bot](https://t.me/Quran_365_bot?start=github)

Если хотите поучаствовать в разработке пишите - [telegram](https://t.me/ilaletdinov), [email](mailto:a.ilaletdinov@yandex.ru?subject=[GitHub]%20Quranbot)

## Информация берется с сайтов:

[umma.ru](https://umma.ru/)

[dumrt.ru](http://dumrt.ru/ru/)

## Используемые технологии:

 - aiogram
 - nats
 - postgres
 - pydantic
 - pytest
 - flake8
 - mypy
 - redis

## Смежные проекты:

[django-version](https://github.com/blablatdinov/quranbot) - предыдущая версия бота, сейчас используется для управления миграциями

[API](https://github.com/blablatdinov/quranbot-admin) - для административной панели. Доступен по [ссылке](https://quranbot.ilaletdinov.ru/docs)

[Хранилище схем для событий](https://github.com/blablatdinov/quranbot-schema-registry/)
