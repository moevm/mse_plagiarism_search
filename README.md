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
Альтернативный вариант - [Miniconda3](https://docs.conda.io/en/latest/miniconda.html). В таком случае опустить шаги 4, 5.
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


## Разное
### Запуск [`yapf`](https://github.com/google/yapf)
Поможет сделать код приятнее на вид.
* `pip install yapf`
* В корне репозитория: `yapf -i -r **/*.py`
Рекомендую призязать `yapf` к IDE, обычно возможности для интеграции находятся.

### Семантические коммиты
Договорились использовать [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) для формата коммитов (`scope` будут свои).
