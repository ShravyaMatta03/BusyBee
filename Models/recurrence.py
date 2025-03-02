"""
    Name: Recurrence Model
    Description: Recurrence model class to represent records in Recurrence table of the database
    Author: Magaly Camacho [3072618]

    Date Created: 10/26/2024
    Revisions:
        - 11/01/2024 Magaly Camacho
            Added __repr__() method
        - 11/18/2024 Magaly Camacho
            Removed relation to events, added relation to items

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
    Postconditions: 
        - None
    Errors/Exceptions: 
        - Validation errors if the attribute constraints (e.g. type, string length, etc.) are not met 
    Side Effects: 
        - Base class will have Recurrence as a part of its metadata
    Invariants: 
        - The class will always be a sub class of the declarative_base from SQLAlchemy
        - The id attribute will always be unique and automatically generated
        - ItemType Enum, Frequency Enum, and Event model are implemented
        - One-to-Many Relationship With Event_
    Known Faults: 
        - None
"""


# Imports
import datetime
from .base import Base # base model
from .item import Item # Event model
from .databaseEnums import Frequency # Enum for frequency attribute
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Recurrence(Base):
    """
    Recurrence Model for records in the Recurrence Table

    Attributes:
        __tablename__ (str): the name of the table
        id (int): recurrence id (primary key, automatically generated by database)
        times (int): how many times to repeat, including original item
        frequency (Models.databaseEnums.Frequency): how often to repeat (daily, weekly, monthly, yearly)
        r_created (datetime): date and time recurrence was created
        r_last_updated (datetime): date and time recurrence was last updated
        items (list[Item]): items associated with this recurrence
    """
    __tablename__ = "Recurrence"


    # Attributes, all are NOT NULL (required)
    id: Mapped[int] = mapped_column(
        primary_key=True # primary key, automatically generated by database
    ) 

    times: Mapped[int]

    frequency: Mapped[Frequency] # daily, weekly, monthly, yearly

    r_created: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now # defaults to inserted date and time
    )

    r_last_updated: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, # defaults to inserted date and time
        onupdate=datetime.datetime.now # auto update this attribute, when record is updated
    )

    # One-to-Many Relationship With Items
    items: Mapped[Optional[List[Item]]] = relationship(
        back_populates="recurrence", # attribute
        cascade="all, delete-orphan" # delete recurrence if all of it's events are deleted
    )


    def __repr__(self):
        """String representation of recurrence instance"""
        string = "\nRecurrence("
        string += f"\n\tid={self.id}"
        string += f"\n\ttimes={self.times}"
        string += f"\n\tfrequency={self.frequency}"
        string += "\n)\n"

        return string