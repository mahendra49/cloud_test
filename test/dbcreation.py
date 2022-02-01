import sqlite3
conn=sqlite3.connect('users.db')
c = conn.cursor()
c.execute("""DROP TABLE IF EXISTS user_details""")

c.execute('''CREATE TABLE user_details
             (first_name varchar(20), last_name varchar(20), email varchar(50),user_name varchar(20), password varchar(20), filename varchar(50))''')

c.execute("INSERT INTO user_details VALUES ('divya','devanaboina','divya@gmail.com','devanadh','devanadh','')")


conn.commit()


conn.close()
