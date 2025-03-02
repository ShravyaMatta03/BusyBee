"""
    Name: Event Model
    Description: Event model class to represent records in Event table of the database
    Author: Magaly Camacho [3072618]

    Date Created: 10/24/2024
    Revisions: 
        - 11/01/2024 Magaly Camacho
            Added __repr__() method, and added superclass attributes to docstring
        - 11/18/2024 Magaly Camacho
            Removed relation to recurrence (moved up to Item model)

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
    Postconditions: 
        - None
    Errors/Exceptions: 
        - Validation errors if the attribute constraints (e.g. type, string length, etc.) are not met 
    Side Effects: 
        - Base class will have Event_ as a part of its metadata
    Invariants: 
        - The class will always be a sub class of the declarative_base from SQLAlchemy
        - The id attribute will always be an id of an Item
        - ItemType Enum is implemented
        - Many-to-One Relationship with Recurrence
    Known Faults: 
        - None
"""


# Imports
from datetime import datetime
from .item import Item # Superclass model
from .databaseEnums import ItemType # enum for types of item
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship


class Event_(Item):
    """
    Event Model for records in the Event Table

    Attributes:
        __tablename__ (str): the name of the table
        id (int): event id (foreign key to Item.id)
        name (str): name of event (from Item superclass)
        notes (str): notes about the event, max 255 chars (optional, from Item superclass)
        place (str): place of event, max 100 chars
        start_time (datetime): start date and time of event
        e_created (datetime): date and time event was created
        e_last_updated (datetime): date and time event was last updated
    """
    __tablename__ = "Event_"


    # Attributes, all are NOT NULL (required) except place
    id: Mapped[int] = mapped_column(
        ForeignKey("Item.id"),  # Foreign Key: Item(id)
        primary_key=True # foreign key is primary key
    )

    place: Mapped[Optional[str]] = mapped_column(String(100))
    
    start_time: Mapped[datetime] = mapped_column(
        default=datetime.now # defaults to inserted date and time
    )
    
    e_created: Mapped[datetime] = mapped_column(
        default=datetime.now # defaults to inserted date and time
    )
    
    e_last_updated: Mapped[datetime] = mapped_column(
        default=datetime.now, # defaults to inserted date and time
        onupdate=datetime.now # auto update this attribute, when record is updated
    )


    # Discriminator, for inheritance: Item(type)
    __mapper_args__ = {
        "polymorphic_identity": ItemType.EVENT
    }


    def __repr__(self):
        """String representation of event instance"""
        string = "\nEvent("
        string += f"\n\tid={self.id}"
        string += f"\n\tname={self.name}"
        string += f"\n\tnotes={self.notes}"
        string += f"\n\tplace={self.place}"
        string += f"\n\tstart_time={self.start_time}"
        string += "\n)\n"

        return string