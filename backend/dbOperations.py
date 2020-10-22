import os
import hashlib
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
import pypikaInit
import psycopg2

from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = os.getcwd()
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#загрузка файлов. Нужно проверить работоспособность.
@app.route('/upload', methods=['POST'])#methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file: #and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			addOneFile(app.config['UPLOAD_FOLDER'], filename, "testEntry")
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
      # <p><input type=file name=file>
         # <input type=submit value=Upload>
    # </form>
    # '''
	
	
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
							   
def addOneFile(dir, fileName, entryName = ""): 

	con = psycopg2.connect(
		database="postgres", 
		user="postgres", 
		password="1234", 
		host="127.0.0.1", 
		port="5432"
	)
	cur = con.cursor()
	
	db = pypikaInit.DBObjects()

	cwd = os.getcwd()
	
	try:
		os.chdir(dir)
		
	except:
		os.chdir(cwd)
		print("Wrong path")
		return
	if len(entryName) == 0:
		entryName = dir
	code = ""
	splittedCode = []
	with open(os.path.join(dir, fileName), encoding='utf-8') as f:
		code = f.read()
		

	code = code.replace("\n", "")
	code = code.replace("\t", "")
	
	codeInBytes = str.encode(code, encoding='utf-8')
	q = Query.into(db.tables["Entry"]).columns('name', 'createdAt').insert(entryName, functions.CurTimestamp())
	print(str(q))
	cur.execute(str(q))
	con.commit()
	
	###нужна обработка ошибок
	q = Query.from_(db.tables["Entry"]).select('id').orderby('id', order=Order.desc).limit(1)
	print(str(q))
	cur.execute(str(q))
	
	rows = cur.fetchall()
	id = 0
	for row in rows:
		print(row[0])
		id = row[0]
		break
	hash_object = hashlib.sha256(codeInBytes)

	q = Query.into(db.tables["File"]).columns("entryId", "path", "hash").insert(id, os.path.join(dir, fileName), hash_object.hexdigest())
	cur.execute(str(q))
	con.commit()
	
	###нужна обработка ошибок
	q = Query.from_(db.tables["File"]).select('id').orderby('id', order=Order.desc).limit(1)
	cur.execute(str(q))
	
	rows = cur.fetchall()
	fileId = 0
	for row in rows:
		fileId = row[0]
		break
		
		
	for i in range(0, (len(codeInBytes)//255)+1):
		splittedCode.append(bytes.decode(codeInBytes[0+(i*255):min(255*(i+1), len(codeInBytes))], encoding='utf-8'))
		q = Query.into(db.tables["CodeFragment"]).columns("fileId", "order", "text", "metaphone").insert(fileId, i, splittedCode[i], db.func["metaphone"](splittedCode[i], 255))
		cur.execute(str(q))
	con.commit()

	con.close()




def deleteEntry(id):
	con = psycopg2.connect(
		database="postgres", 
		user="postgres", 
		password="1234", 
		host="127.0.0.1", 
		port="5432"
	)
	cur = con.cursor()
	
	db = pypikaInit.DBObjects()
	
	q = Query.from_(db.tables["Entry"]).delete().where(db.tables["Entry"].id == id)
	cur.execute(str(q))
	con.commit()
	
	con.close()
	
def deleteAll():
	con = psycopg2.connect(
		database="postgres", 
		user="postgres", 
		password="1234", 
		host="127.0.0.1", 
		port="5432"
	)
	cur = con.cursor()
	
	db = pypikaInit.DBObjects()
	
	q = Query.from_(db.tables["Entry"]).delete()
	cur.execute(str(q))
	con.commit()
	
	con.close()