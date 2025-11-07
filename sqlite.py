import sqlite3

#connect to sqlite
connection = sqlite3.connect("student.db")

#create cursor object to insert, create records 
cursor = connection.cursor()

#create a table
table_info = """
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);
"""

cursor.execute(table_info)

#Inset some more records

cursor.execute("""Insert into STUDENT values('Krish','Data Science','A',90);""")
cursor.execute("""Insert into STUDENT values('Amit','Data Analytics','B',86);""")
cursor.execute("""Insert into STUDENT values('Pranjay','Machine Learning','B',91);""")
cursor.execute("""Insert into STUDENT values('Arin','Artificial Intelligence','A',56);""")
cursor.execute("""Insert into STUDENT values('Afzal','Business Management','B',32);""")

#Display all records
print("Inserted records are:")

data = cursor.execute("Select * from STUDENT;")
for row in data:
    print(row)

#commit and close the connection

connection.commit()
connection.close()