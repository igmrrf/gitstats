# This file will open a connection to the flask_db database, create a table called books, and populate the table using sample data. Add the following code to it:
import os
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="gitstats",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
)

# Open a cursor to perform database operations
cursor = connection.cursor()

# Execute a command: this creates a new table
cursor.execute("DROP TABLE IF EXISTS insight;")
cursor.execute(
    "CREATE TABLE insight (id serial PRIMARY KEY," "page varchar (150) NOT NULL;"
)

# Insert data into the table
cursor.execute(
    "INSERT INTO insight (page)" "VALUES (%s)",
    ("insight"),
)


cursor.execute(
    "INSERT INTO insight (page)" "VALUES (%s)",
    ("core"),
)

connection.commit()

cursor.close()
connection.close()
# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
