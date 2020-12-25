FROM python:3.8-buster
WORKDIR .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y astyle
COPY ./backend ./backend
COPY ./prettier ./prettier
COPY ./scripts ./scripts
WORKDIR ./backend
EXPOSE 5000
RUN sed 's/127.0.0.1/postgres/g' config.ini -i
CMD ["python","-m","flask","run"]
