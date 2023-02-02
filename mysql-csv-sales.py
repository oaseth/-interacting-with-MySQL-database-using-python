import mysql.connector as mysql
import csv
from db_config import config

# The configuration file to be used
config_file = 'mysql_cred.ini'

# Load the MySQL credentials from the configuration file
section = 'mysql'
params = config(config_file, section)

# Create a connection to the server
connection = mysql.connect(**params,
                           database='sales',
                           allow_local_infile=True)

# Create a cursor
cursor = connection.cursor()

# Create a query to execute
create_query = '''CREATE TABLE salesperson(
	id INT(255) NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email_address VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	state VARCHAR(255) NOT NULL,
	PRIMARY KEY (id))'''

# Execute queries
cursor.execute("DROP TABLE IF EXISTS salesperson")

cursor.execute(create_query)

# with open('./salespeople.csv', 'r') as f:
# 	csv_data = csv.reader(f)
# 	for row in csv_data:
# 		print(row)
# 		row_tuple = tuple(row)
# 		cursor.execute('INSERT INTO salesperson(first_name, last_name, email_address, city, state) VALUES("%s", "%s", "%s", "%s","%s")', row_tuple)

q = '''LOAD DATA LOCAL INFILE 
'data/salespeople.csv'
 INTO TABLE salesperson FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
 (first_name, last_name, email_address, city, state);'''

cursor.execute(q)

connection.commit()

cursor.execute("SELECT * FROM salesperson LIMIT 10")
print(cursor.fetchall())

connection.close()
