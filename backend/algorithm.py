from dbOperations import con, db, app, config, ALLOWED_EXTENSIONS, ALLOWED_ARCHIVES, executeQ
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions

def getAllMetaphones():
	metaphones = {}
	q = Query.from_(db.tables["CodeFragment"]).select("fileId", "metaphone").orderby('id', order=Order.asc)
	rows = executeQ(q, True)
	for row in rows:
		metaphones.setdefault(row[0], []).append(row[1])
	return metaphones

def algo(fileId):
	metaphones = getAllMetaphones()

	average = 0
	sumStud1 = 0
	sumStud2 = 0

	for key, val in metaphones.items():
		if key != fileId:
			for lval in val:
				sumStud2+=1
				if lval in metaphones[fileId]:
					sumStud1+=1

	#average = (sumStud1 + sumStud2) // 2
	
	#matches = 0

	#for item in codes[stud1].items():
		#if codes[stud2].get(item[0]):
			#matches += min(item[1], codes[stud2].get(item[0]))
			
	#print("stud", stud1, " vs stud", stud2, ":::::", matches , "/" , average, "/", matches/average*100, "%")
	print(sumStud1, sumStud2)
	print("stud", 1, " vs stud", 2, ":::::", sumStud1/sumStud2*100, "%")
	
algo(3)