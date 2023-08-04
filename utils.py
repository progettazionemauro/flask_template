from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app import app, UserRegistration


# Create an engine for the core database
core_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
CoreSession = sessionmaker(bind=core_engine)
core_session = CoreSession()

# Create an engine for the user registration database
users_engine = create_engine(app.config['SQLALCHEMY_BINDS']['users'])
UsersSession = sessionmaker(bind=users_engine)
users_session = UsersSession()

# Inspect databases and tables
def inspect_databases():
    core_inspector = inspect(core_engine)
    users_inspector = inspect(users_engine)

    print("Core Database Tables:")
    print(core_inspector.get_table_names())

    print("User Registration Database Tables:")
    print(users_inspector.get_table_names())

# Perform queries
def perform_queries():
    # Query from core database
   # core_user = core_session.query(OtherModel).filter_by(some_column='value').first()
   # print("User from Core Database:", core_user)

    # Query from user registration database
    user = users_session.query(UserRegistration).filter_by(username='mauro').first()
    print("User from User Registration Database:", user)

if __name__ == "__main__":
    inspect_databases()
    perform_queries()
