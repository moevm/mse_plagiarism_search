import os
import hashlib

#Директория, в которой находится файл, должна называться соответственно виду работы. 
#Название будет записано в таблицу Entry
#Или укажи свое название для Entry
#Виндовские слэши в пути библиотека не понимает
def addOneFile(connection, dir, fileName, entryName = ""): 
	
	cur = connection.cursor()
	
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
		
	#print(code)	
		
	code = code.replace("\n", "")
	code = code.replace("\t", "")
	
	codeInBytes = str.encode(code, encoding='utf-8')
	cur.execute(
		"""INSERT INTO Public."Entry" ("name", "createdAt") VALUES (%s, CURRENT_TIMESTAMP) RETURNING id""", (entryName,)
	)
	connection.commit()
	rows = cur.fetchall()
	id = 0
	for row in rows:
		id = row[0]
		break
	hash_object = hashlib.sha256(codeInBytes)
	print(hash_object.hexdigest())
	cur.execute(
		"""INSERT INTO Public."File" ("entryId", "path", "hash") VALUES (%s, %s, %s) RETURNING id""", (id, os.path.join(dir, fileName), hash_object.hexdigest())
	)
	connection.commit()
	
	rows = cur.fetchall()
	fileId = 0
	for row in rows:
		fileId = row[0]
		break
		
		
	for i in range(0, (len(codeInBytes)//255)+1):
		splittedCode.append(bytes.decode(codeInBytes[0+(i*255):min(255*(i+1), len(codeInBytes))], encoding='utf-8'))
		cur.execute(
			"""INSERT INTO Public."CodeFragment" ("fileId", "order", "text", "metaphone") VALUES (%s, %s, %s, metaphone(%s, 255))""", (fileId, i, splittedCode[i], splittedCode[i])
		)
	connection.commit()



