# mse_plagiarism_search

[![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)](https://forthebadge.com)

[Доска в Trello](https://trello.com/b/1opwXmzy)

## Запуск в docker
1. Склонировать репозиторий  
`git clone git@github.com:moevm/mse_plagiarism_search.git`  
`cd mse_plagiarism_search`  
2. Запустить docker
* `docker-compose up`

Будут запущены:
- Фронтэнд на порту 8080
- pgAdmin 4 на порту 81

## Инструкция по запуску
### Запуск REST API
Пререквизиты:
* [Python](https://www.python.org/) >= 3.6
* [Node.js](https://nodejs.org/en/) >= 12.0
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/) >= 3.5
* bash >= 4.0 (!)

#### Установка:
1. Установить `virtualenv`  
`pip install virtualenv`  
Альтернативный вариант (советую его) - [Miniconda3](https://docs.conda.io/en/latest/miniconda.html).
    * Установить `Miniconda`
    * `conda create --name mse_plagiarism_search`
    * `conda activate mse_plagiarism_search`
    * `conda install python`
    * Опустить шаги 3.2, 3.3 далее
2. Склонировать репозиторий  
`git clone git@github.com:moevm/mse_plagiarism_search.git`  
`cd mse_plagiarism_search`
3. Настрока бэкэнда. В корне репозитория:
	1. `cd backend`  
	2. `python -m virtualenv venv`  
	3. `source venv/bin/activate`  
	4. Установить зависимости Python  
	`pip install -r requirements.txt`  
	В случае проблем с `psycopg2`, ставить как `pip install psycopg2-binary`  
4. Настройка фронтэнда. В корне репозитория:
	* `cd frontend`
	* Установить зависимости Node.js  
	`npm install`

#### Запуск
В корне репозитория:
1. Запуск БД (консоль 1). В корне репозитория:
	1. `docker-compose up`  
	Будет развернута база `PostgresSQL` на порте. 5432 и pgAdmin на порте 81.
2. Запуск бэкэнда (консоль 2):
	1. `cd backend`
	2. `source venv/bin/activate` (или `conda activate mse_plagiarism_search`)
	3. `export FLASK_APP=app.py`
	4. `python -m flask run`
	dev-сервер запустится на порту 5000. При первом запуске в базе будут созданы таблички и будет установлено расширение `fuzzystrmatch`
3. Запуск фронтэнда (консоль 3):
	1. `cd frontend`
	2. `npm run serve`  
	Клиент запустится на порту 8080.

### Выгрузка репозитория с GitHub

#### Выгрузка одиночного репозитория

Будет привязано к основной функциональности, пока в формате отдельного скрипта
1. Повторить п.1,3 инструкции по установке REST API
2. `cd scripts`
3. `python load_repo.py <URI репозитория> <путь>`
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
