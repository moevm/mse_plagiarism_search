import os
import hashlib
from app import * #imported: con, db, app, #ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Загрузка файлов в БД. Работает!
@app.route('/upload', methods=['POST'])#methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file: #and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			addOneFile(app.config['UPLOAD_FOLDER'], filename) #TODO: Удалить файл после всех операций?
			return redirect(url_for('uploaded_file', filename=filename))
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
      # <p><input type=file name=file>
         # <input type=submit value=Upload>
    # </form>
    # '''
	
	
@app.route('/uploads/<filename>') #временная штука для проверок
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#TODO: Осмысленное entryName
#	   Хранить не весь путь для файла, а только от папки загрузок 								   
def addOneFile(dir, fileName, entryName = ""): 

	cwd = os.getcwd()
	
	os.chdir(dir)

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
	
	id = 0
	executeQ(q)
	q = Query.from_(db.tables["Entry"]).select('id').orderby('id', order=Order.desc).limit(1)
	id = getId(executeQ(q, True))

	hash_object = hashlib.sha256(codeInBytes)

	fileId = 0
	q = Query.into(db.tables["File"]).columns("entryId", "path", "hash").insert(id, os.path.join(dir, fileName), hash_object.hexdigest())
	executeQ(q)
	q = Query.from_(db.tables["File"]).select('id').orderby('id', order=Order.desc).limit(1)
	fileId = getId(executeQ(q, True))
		
	for i in range(0, (len(codeInBytes)//255)+1):
		splittedCode.append(bytes.decode(codeInBytes[0+(i*255):min(255*(i+1), len(codeInBytes))], encoding='utf-8'))
		q = Query.into(db.tables["CodeFragment"]).columns("fileId", "order", "text", "metaphone").insert(fileId, i, splittedCode[i], db.func["metaphone"](splittedCode[i], 255))
		executeQ(q)
		
	os.chdir(cwd)


def deleteEntry(id):

	q = Query.from_(db.tables["Entry"]).delete().where(db.tables["Entry"].id == id)
	executeQ(q)

	
def deleteAll():

	q = Query.from_(db.tables["Entry"]).delete()
	executeQ(q)


def getId(rows):
	for row in rows:
		return row[0]

def executeQ(q, isFetchable=False):
	with con:
		with con.cursor() as cur:
			cur.execute(str(q))
			if isFetchable:
				return cur.fetchall()
				
