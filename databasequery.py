import sqlite3

conn = sqlite3.connect('email.db')
curs = conn.cursor()

curs.execute('SELECT * from Mail')
iets = curs.fetchall()

#for row in curs:
 #   print (row)




conn.close()