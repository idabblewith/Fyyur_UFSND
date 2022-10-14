import psycopg2

connection = psycopg2.connect("dbname=test user=postgres password=1")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS table2;")

cursor.execute(
    """
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
"""
)

SQL = "INSERT INTO table2 (id, completed)" + " VALUES(%(id)s, %(completed)s);"
data = {
    "id": 2,
    "completed": True,
}
cursor.execute(SQL, data)


connection.commit()
connection.close()
cursor.close()
