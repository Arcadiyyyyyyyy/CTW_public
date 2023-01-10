import sqlite3
import datetime


# SQL initialisation
conn = sqlite3.connect('.\\db.db')
c = conn.cursor()


c.execute('''
          CREATE TABLE IF NOT EXISTS CTW
          ([Date] TEXT, [Vacancies] TEXT)
          ''')


date = datetime.date(2022, 11, 27)


# Enter values from folder to the database
for i in range(0, 39):
    with open("vacancies\\vacancies_" + str(date) + ".txt", "r", encoding="utf-8") as f:
        f1 = f.read()
    c.execute("INSERT INTO CTW (Date, Vacancies) VALUES ('"+str(date)+"', '"+str(f1)+"')")
    date = date + datetime.timedelta(days=1)


conn.commit()
conn.close()
