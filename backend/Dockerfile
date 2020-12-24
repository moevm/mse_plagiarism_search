FROM python:3.8-buster
WORKDIR .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y astyle
EXPOSE 5000
RUN sed 's/127.0.0.1/postgres/g' config.ini -i
CMD ["python","-m","flask","run"]
