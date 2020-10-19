import psycopg2
import CRUD as db
import dbOperations as dbOps

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="1234", 
  host="127.0.0.1", 
  port="5432"
)

print("Database opened successfully")

#do anything
#for example:

#dbOps.addOneFile(con, "d:/Code.tar/Code/Code/6303_Dobrokhvalov/lab1/scripts", "tetris.js")
#db.delete(con, "Entry", 29) #удалим то что сделали для тестов

print("It's time to close database")
con.close()