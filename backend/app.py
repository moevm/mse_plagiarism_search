import configparser
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
from pypikaInit import db
import psycopg2
import os
import traceback
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sqlQueries

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')
dbConfig = config["databaseConfig"]


def createTablesIfNotExists(con):
    with con:
        with con.cursor() as cur:
            cur.execute(sqlQueries.createSequences)
            con.commit()
            cur.execute(sqlQueries.createEntryTable)
            cur.execute(sqlQueries.createFileTable)
            cur.execute(sqlQueries.createCodeFragmentTable)
            cur.execute(sqlQueries.createSearchResultTable)


class singleConnection:
    def __init__(self):
        self.con = psycopg2.connect(
            database=dbConfig["database"],
            user=dbConfig["user"],
            password=dbConfig["password"],
            host=dbConfig["host"],
            port=dbConfig["port"]
        )
        createTablesIfNotExists(self.con)
        os.makedirs(config['app']['uploadFolder'], exist_ok=True)

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(singleConnection, self).__new__(self)
        return self.instance

    def __del__(self):
        self.con.close()


con = singleConnection().con
app = Flask(__name__)
cors = CORS(
    app, resources={r'/*': {
        'origins': '*'
    }}, supports_credentials=True
)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), config["app"]["uploadFolder"])
ALLOWED_EXTENSIONS = set(config["allowed_extensions"].keys())
ALLOWED_ARCHIVES = set(config["allowed_archives"].keys())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.errorhandler(Exception)
def internal_error(exception):
    app.logger.error(traceback.format_exc())
    response = {'ok': False, 'message': repr(exception)}
    if os.environ.get('FLASK_ENV') == 'development':
        response['traceback'] = traceback.format_exc()
    return jsonify(response), 500


import dbOperations
import algorithm

import sys
sys.path.insert(0, os.path.join(os.getcwd(), "..", "scripts"))
import load_repos_functions
