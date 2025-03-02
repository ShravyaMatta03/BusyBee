"""
    Name: Base Model
    Description: Base model class for all database models
    Authors: Magaly Camacho [3072618]

    Date Created: 10/21/2024
    Revisions: 
        - None

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
    Postconditions: 
        - None
    Errors/Exceptions: 
        - None
    Side Effects: 
        - None
    Invariants: 
        - The Base model will always be a sub class of the DeclarativeBase from SQLAlchemy
        - Any classes derived from the Base can be used to create a Database declaratively
    Known Faults: 
        - None
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

