from aes import a
import sqlite3

conn = sqlite3.connect("test.db")

c = conn.cursor()

print(a)
c.execute("""CREATE TABLE employees (
            first TEXT,
            last text,
            pay integer,
            tkey text
        )""")

c.execute("INSERT INTO employees VALUES (\"corey\", \"schafer\", 70000, \"{}\")".format(a))

c.execute("SELECT * FROM employees WHERE last=\"schafer\"")

n = c.fetchall()

print(len(n))
v = n[0][3]
print(type(v))

for element in v:
    print(element)

conn.commit()

conn.close()