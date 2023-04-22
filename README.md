# Поиск вакансий на сайтах HH и SuperJob

Скрипт для поиска вакансий программистов на двух ресурсах: [hh.ru](https://hh.ru/) и [SuperJob.ru](https://www.superjob.ru/).

Результаты поиска отображаются на экране в виде 2 таблиц с данными:

-язык программирования

-количество вакансий

-количество вакансий с заработной платой

-средняя ожидаемая заработная плата
### Запуск

Для работы понадобится Python3 и ряд библиотек из файла requirements.txt.
Для сайта Superjob.ru нужен токен, зарегистрироваться и получить токен можно [здесь](https://api.superjob.ru/).

Токен нужно сохранить в .env файл в директории проекта:

```Python
X-Api-App-Id = # токен для API Superjob
```

Запускаем командную строку, переходим в директорию проекта и устанавливаем зависимости:
```
pip install -r requirements.txt
```
Запускаем проект:

```
python main.py
```

Результат:

![](https://github.com/atskayasatana/Images/blob/cab8f567e77b2cd10ec4035ddcdbaf62c44dfae6/hh_api_res.png)


