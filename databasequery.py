import sqlite3

conn = sqlite3.connect('email.db')
curs = conn.cursor()

#curs.execute('SELECT * from Mail order by date ASC')
curs.execute('Select * from Users')
iets = curs.fetchall()

for row in iets:
    print (row)




conn.close()