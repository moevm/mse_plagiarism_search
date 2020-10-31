# mse_plagiarism_search

[Доска в Trello](https://trello.com/b/1opwXmzy)

## Инструкция по запуску
### Запуск REST API
Пререквизиты:
* [Python](https://www.python.org/) >= 3.6
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/) >= 3.5
* bash >= 4.0 (!)

Инструкция:
1. Установить `virtualenv`  
`pip install virtualenv`  
Альтернативный вариант (советую его) - [Miniconda3](https://docs.conda.io/en/latest/miniconda.html).
    * Установить `Miniconda`
    * `conda create --name mse_plagiarism_search`
    * `conda activate mse_plagiarism_search`
    * `conda install python`
    * Опустить шаги 4, 5 далее
2. Склонировать репозиторий  
`git clone git@github.com:moevm/mse_plagiarism_search.git`
3. `cd mse_plagiarism_search/backend`
4. `python -m virtualenv venv`
5. `source venv/bin/activate`
6. Установить зависимости Python  
`pip install -r requirements.txt`
7. Открыть ещё одну консоль с корнем репозитория, запустить там `docker-compose up`.  
Будет развернута база `PostgresSQL` на порте. 5432 и pgAdmin на порте 81.
8. (в первой консоли) `python -m flask run`  
dev-сервер запустится на порту 5000. При первом запуске в базе будут созданы таблички.

### Выгрузка репозитория с GitHub
Будет привязано к основной функциональности, пока в формате отдельного скрипта
1. Повторить п.1,2 инструкции по запуску REST API
2. `cd scripts`
3. `python delete_files.py <URI репозитория> <путь>`
4. В папке `<путь>` будут полученные файлы с исходным кодом

### Парсинг датасета StackOverflow
Будет привязано к основной функциональности, пока в формате отдельного скрипта

1. Повторить п.1,2 инструкции по запуску REST API
2. `cd parsing`
3. После запуска программы(python pars.py) ввести путь до файла, который необходимо парсить
4. В консоль будут выведены теги языков из обработанного кода
5. В файлы с соответствующими названиями будут добавлены фрагменты кода разделенные по языкам
6. В файл o.txt будут сохранены все фрагменты кода

## Разное
### Запуск [`yapf`](https://github.com/google/yapf)
Поможет сделать код приятнее на вид.
* `pip install yapf`
* В корне репозитория: `yapf -i -r **/*.py`
Рекомендую призязать `yapf` к IDE, обычно возможности для интеграции находятся.

### Семантические коммиты
Договорились использовать [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) для формата коммитов (`scope` будут свои).
