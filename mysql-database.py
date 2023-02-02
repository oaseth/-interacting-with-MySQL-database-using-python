import mysql.connector as mysql
from db_config import config

# The configuration file to be used
config_file = 'mysql_cred.ini'

# Load the MySQL credentials from the configuration file
section = 'mysql'
params = config(config_file, section)


def connect(db_name):
    """ 
    A function to create a connection to MySQL server

    Parameter
    ---------
        db_name: the database name
    """
    try:
        return mysql.connect(
            **params,
            database=db_name)
    except Error as e:
        print(e)


def add_new_project(cursor, project_title, project_description,
                    task_descriptions):
    """ 
    A function to add a new project to the projects database

    Parameter
    ---------
        cursor: the cursor object
        project_title: the title of the project to be added
        project_description: the description of the project
        task_descriptions: the description of the task

    """
    project_data = (project_title, project_description)
    cursor.execute('''INSERT INTO projects(title, description)  
        VALUES (%s, %s)''', project_data)

    project_id = cursor.lastrowid

    tasks_data = []
    for description in task_descriptions:
        task_data = (project_id, description)
        tasks_data.append(task_data)

    cursor.executemany('''INSERT INTO tasks(project_id, description) 
        VALUES (%s, %s)''', tasks_data)


# Main()
if __name__ == '__main__':
    db = connect("projects")
    cursor = db.cursor()

    tasks = ["Clean bathroom", "Clean kitchen", "Clean living room"]
    add_new_project(cursor, "Clean house", "Clean house by room", tasks)

    cursor.execute("SELECT * FROM projects")
    project_records = cursor.fetchall()
    print(project_records)

    cursor.execute("SELECT * FROM tasks")
    tasks_records = cursor.fetchall()
    print(tasks_records)

    db.commit()
    db.close()
