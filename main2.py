import psycopg2
import time

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
#Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)

cursor.execute('''
    SELECT * FROM COMPANY;
''')
row = cursor.fetchall()
print(row)

cursor.execute('''
    INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE) VALUES (6,'Yeah',24,'Texas',85000.0,'2007-12-13')
''')

conn.commit()
#Closing the connection

time.wait(5)

cursor.execute('''
    SELECT * FROM COMPANY;
''')
row = cursor.fetchall()

print(row)

conn.close()