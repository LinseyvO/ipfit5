import sqlite3

#er wordt een verbinding opgezet met de database
conn = sqlite3.connect('email.db')
curs = conn.cursor()

#er wordt een query uitgevoerd
curs.execute('SELECT * from Mail')

#hier wordt de opgevraagde query uitgeprint in de terminal
for row in curs:
    print (row)




conn.close() # de connectie wordt afgesloten
