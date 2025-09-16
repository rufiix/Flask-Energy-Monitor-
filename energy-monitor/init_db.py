import sqlite3

with open('init_db.sql', 'r', encoding='utf-8') as f:
    s = f.read()

conn = sqlite3.connect('energy.db')
conn.executescript(s)
conn.commit()
conn.close()

print("Baza energy.db gotowa")
