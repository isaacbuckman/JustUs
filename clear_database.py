# sqlite3 commands
# DROP TABLE reports
# CREATE TABLE reports(who TEXT, location TEXT, what BLOB)
# SELECT who, location, what FROM reports
# DELETE FROM reports
# INSERT INTO reports(who, location, what) VALUES(?,?,?)

import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''DELETE FROM reports''')
con.commit()