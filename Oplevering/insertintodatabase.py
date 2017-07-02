import csv, sqlite3 # modules worden geimporteerd

con = sqlite3.connect("email.db") # er wordt een database verbinding opgezet
con.text_factory = str # hiermee kan je de return waarde controlen
cur = con.cursor() # de cursor zorgt ervoor dat er operaties uitgevoerd kunnen worden
cur.execute("CREATE TABLE Mail (subject VARCHAR, sender VARCHAR, receiver VARCHAR, date datetime, body text);") # deze tabel wordt aangemaakt

with open('./mail/cleaned_mail.csv', 'rb') as fin: # hier wordt het bestand met data geopend
    dr = csv.DictReader(fin) # deze zorgt ervoor dat de eerste rij in het csv bestand als key worden gezien en de rest als value
    to_db = [(i['col1'], i['col2'], i['col3'], i['col4'], i['col5']) for i in dr] # deze variabel wordt gelijk gemaakt aan de waardes van uit het csv bestand

cur.executemany("INSERT INTO Mail(subject, sender, receiver, date, body) VALUES (?, ?, ?, ?, ?);", to_db) # hier wordt de data uit de to_db variabele toegevoegd aan de database in goede orde
con.commit() # de transactie wordt gecommit, anders wordt de uitgevoerde query niet doorgevoerd
con.close() # de database connectie wordt afgesloten
