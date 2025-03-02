"""
    Name: Item-Category Association Model
    Description: Item-Category association model to represent records in ItemCategory table of the database
    Author: Magaly Camacho [3072618]

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
        - Base class will have the association as a part of its metadata
    Invariants: 
        - Records will reference records in Item and Category tables
    Known Faults: 
        - None
"""


# Imports
from .base import Base # base model
from sqlalchemy import Column, Table, ForeignKey


item_category_association = Table(
    "Item_Category", # Table name
    Base.metadata, # link to base, for engine/database creation

    # attribute item_id
    Column("item_id", 
        ForeignKey("Item.id"), 
        primary_key=True
    ), 

    # attribute category_id
    Column("category_id", 
        ForeignKey("Category.id"), 
        primary_key=True
    )
)