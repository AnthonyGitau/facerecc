import sqlite3
conn = sqlite3.connect('facedb.db')
c= conn.cursor()

#create table
c.execute('''CREATE TABLE Students(Id INTEGER PRIMARY KEY, Names text)''')
