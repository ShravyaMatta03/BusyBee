"""
    Name: Database Class
    Description: Database class that serves as an interface to interact with the SQLite database
    Author: Magaly Camacho [3072618]

    Date Created: 10/20/2024
    Revisions: 
        - 11/01/2024 Magaly Camacho
            Added method to get database session
        - 11/04/2024 Magaly Camacho
            Added method default db for testing (Tests/Output/test_db.db)

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
        - Models and Enums must be implemented
    Postconditions: 
        - None
    Errors/Exceptions: 
        - Operational Error if the database cannot be created or accessed
        - SQLAlchemyError for any SQLAlchemy-related errors
    Side Effects: 
        - None
    Invariants: 
        - Base will contain all database metadata (models/tables)
        - The database schema will be consistent with the defined models
    Known Faults: 
        - None
"""


# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Models.base import Base # base class for database models


class Database:
    """
    Class to interact with the SQLite database
    
    Attributes:
        engine (Engine): database engine created from models
    """
    def __init__(self, db_path:str="Tests/Output/test_db.db", debug:bool=False):
        """
        Initialize database from models

        Attributes:
            db_path (str): the path to the database (or where it should be created)
            debug (bool): whether or not to print SQL emitted by connection, False by default
        """
        # engine to create database connections
        self.engine = create_engine(f"sqlite:///{db_path}", echo=debug)
        
        # create database if it doesn't exist already
        Base.metadata.create_all(self.engine) 

    
    def get_session(self) -> Session:
        """Starts and returns a session to manage persistence operations for ORM-mapped objects. Must be used with "with" statement"""
        return Session(self.engine)
    

def get_database(test:bool=False, debug:bool=False):
    """
    Returns database object for busybee
    
    Parameters:
        test (bool): whether to connect to test the database (default in Database)
        debug (bool): whether to print logs or not

    Returns:
        Database: database object
    """
    # debugging, connect to test database
    if test:
        return Database(debug=debug)
    
    # otherwise, connect to actual database
    return Database(db_path="busybee.db", debug=debug)