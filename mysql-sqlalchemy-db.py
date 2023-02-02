from os import environ
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# MySQL URI
mysql_uri = environ.get('MYSQL_URI')

# Name of database to connect
db_name = "household"

# Create the database engine
engine = create_engine(
    mysql_uri + db_name, echo=True)

# Create the base
Base = declarative_base()


class Project(Base):
    """
    A model for the "Project" table
    """
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'household'}

    # The columns of the table
    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    description = Column(String(length=50))

    # String representation
    def __repr__(self):
        return "<Project(title='{0}', description='{1}')>".format(self.title, self.description)


class Task(Base):
    """
    A model for the "Task" table
    """
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'household'}

    # The columns of the table
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('household.projects.project_id'))
    description = Column(String(length=50))

    # The relationship of this model with the Project model
    project = relationship("Project")

    # String representation
    def __repr__(self):
        return f"<Task(description={self.description})>"


# Add models to the engine
Base.metadata.create_all(engine)

# Create a sessionmaker object
session_maker = sessionmaker()
session_maker.configure(bind=engine)
session = session_maker()

# Create a "Project" object
organize_closet_project = Project(
    title='Organize closet', description='Organize closet by color and style')
session.add(organize_closet_project)
session.commit()

# Create a list of "Task" objects
tasks = [Task(project_id=organize_closet_project.project_id,
              description='Decide to what close to donate'),
         Task(project_id=organize_closet_project.project_id,
              description='Organize winter closet'),
         Task(project_id=organize_closet_project.project_id,
              description='Organize summer closet')]

session.bulk_save_objects(tasks)
session.commit()

# Queries
our_project = session.query(Project).filter_by(title='Organize closet').first()
print(our_project)

our_tasks = session.query(Task).all()
print(our_tasks)
