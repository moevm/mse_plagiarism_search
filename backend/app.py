import configparser
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
from pypikaInit import db
import psycopg2
import os
import traceback
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

config = configparser.ConfigParser()
config.read("config.ini")
dbConfig = config["databaseConfig"]


class singleConnection:
	def __init__(self):
		self.con = psycopg2.connect(
			database=dbConfig["database"], 
			user=dbConfig["user"], 
			password=dbConfig["password"], 
			host=dbConfig["host"], 
			port=dbConfig["port"]
		)
	def __new__(self):
		if not hasattr(self, 'instance'):
			self.instance = super(singleConnection, self).__new__(self)
		return self.instance
		
	def __del__(self):
		self.con.close()

con = singleConnection().con
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), config["app"]["uploadFolder"])
ALLOWED_EXTENSIONS = set(config["allowed_extensions"].keys())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(Exception)
def internal_error(exception):
	app.logger.error(traceback.format_exc())
	response = {'ok': False, 'message': repr(exception)}
	if os.environ.get('FLASK_ENV') == 'development':
		response['traceback'] = traceback.format_exc()
	return jsonify(response), 500

	
import dbOperations