import csv,sqlite3

con = sqlite3.connect("email.db")
con.text_factory = str
cur = con.cursor()
cur.execute("CREATE TABLE Mail (subject VARCHAR, sender VARCHAR, receiver VARCHAR, date datetime, body text);")

with open('cleaned_mail.csv', 'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['col1'], i['col2'], i['col3'], i['col4'], i['col5']) for i in dr]

cur.executemany("INSERT INTO Mail(subject, sender, receiver, date, body) VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

