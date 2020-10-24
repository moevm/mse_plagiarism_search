from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
from pypikaInit import db
import psycopg2
import os
import traceback
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

class singleConnection:
	def __init__(self):
		self.con = psycopg2.connect(
			database="postgres", 
			user="postgres", 
			password="1234", 
			host="127.0.0.1", 
			port="5432"
		)
	def __new__(self):
		if not hasattr(self, 'instance'):
			self.instance = super(singleConnection, self).__new__(self)
		return self.instance
		
	def __del__(self):
		self.con.close()

con = singleConnection().con

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(Exception)
def internal_error(exception):
	app.logger.error(traceback.format_exc())
	response = {'ok': False, 'message': repr(exception)}
	if os.environ.get('FLASK_ENV') == 'development':
		response['traceback'] = traceback.format_exc()
	return jsonify(response), 500

	
import dbOperations