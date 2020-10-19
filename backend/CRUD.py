def create(connection, table, **args): 
	#Аргументы: Поле1 = "Значение1", Поле2 = "Значение2"
	#если нужна постгресовская функция, то передавать нужно исключительно ее параметр, а дальше я тут разберусь
	#если без параметра, то вообще ничего не передавать
	
	cur = connection.cursor()

	query = """INSERT INTO Public."{table}" (""".format(table = table)
	values = ""
	listForTuple = []
	
	for key, val in args.items():
		query += '"'+key+'",'
		if table == "CodeFragment" and key == "metaphone":
			values += "metaphone(%s, 255)"
		else:
			values += "%s,"
		listForTuple.append(val)
	if table == "Entry":
		query += '"createdAt",'
		values += "CURRENT_TIMESTAMP,"

		
	query = query[0:-1]
	values = values[0:-1]
	query += ") VALUES ({values}) RETURNING id".format(values = values)
	
	cur.execute(query, tuple(listForTuple))
	connection.commit()
	
	rows = cur.fetchall()
	id = 0
	for row in rows:
		id = row[0]
		break
	return id
	
	
def read(connection, table, id=0):

	cur = connection.cursor()
	
	query = """SELECT * FROM Public."{table}" """.format(table = table)
	condition = 'WHERE "id" = ' + str(id)
	
	if (id != 0):
		query += condition
		
	cur.execute(query)
	rows = cur.fetchall()

	return rows
	

def update(connection, table, setString, whereString, tupleOfArgs = None):
	#Тут слишком много возможностей использовать какую-то специфичную postgresql функцию, поэтому я просто немного упрощу синтаксис
	#setString вида " "field1" = newValue1, "field2" = newValue2", лучше использовать " "field1" = %s, "field2" = %s" и все аргументы передавать кортежем
	#whereString вида "field1 = condition1, "field2" = condition2" так же лучше все строки через кортеж передавать
	
	cur = connection.cursor()
	
	query = """UPDATE Public."{table}" SET """ + setString + " WHERE " + whereString
	if tupleOfArgs is None:
		cur.execute(query)
	else:
		cur.execute(query, tupleOfArgs)
		
	connection.commit()
	
def delete(connection, table, id=0):
	
	cur = connection.cursor()
	
	query = """DELETE FROM Public."{table}" """.format(table = table)
	condition = 'WHERE "id" = ' + str(id)
	
	if (id != 0):
		query += condition
	cur.execute(query)
	connection.commit()
