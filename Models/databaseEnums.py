"""
    Name: Database Enumerations
    Description: Enumerations for database models, item types, as well as database attributes Task(Priority) and Recurrence(Frequency)
    Authors: Magaly Camacho [3072618]

    Date Created: 10/20/2024
    Revisions: 
        - 11/04/2024 Magaly Camacho
            Added a static method to Priority to get string and color associated with a given priority
        - 11/18/2024 Magaly Camacho
            Added helpful methods to Frequency enum

    Preconditions: 
        - None
    Postconditions: 
        - None
    Errors/Exceptions: 
        - None
    Side Effects: 
        - None
    Invariants: 
        - The classes will be subclasses of Enum
    Known Faults: 
        - None
"""


from enum import Enum
from datetime import datetime, timedelta


class ItemType(Enum):
    """Enumeration for types of items"""
    EVENT = 0
    TASK = 1


class Priority(Enum):
    """Enumeration for Task.Priority"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2


    @classmethod
    def get_str_and_color(cls, priority) -> tuple[str, tuple[float, float, float, float]]:
        """
        Returns string and color associated with a given priority

        Parameters:
            priority (Priority): a given priority (LOW, MEDIUM, or HIGH)

        Returns:
            tuple[str, tuple[float, float, float, float]: the string and color associated with the priority (string, color)
        """
        str_list = cls.priority_options()
        colors = [
            (16, 111, 16, 1), # green, low
            (171, 113, 18, 1), # orange, medium
            (114, 11, 11, 1) # red, high
        ]

        if priority in Priority:
            val = priority.value
            return str_list[val], tuple(c / 255 if i != 3 else c for i, c in enumerate(colors[val]))
        
        raise ValueError("Invalid Priority value")
    
    @classmethod
    def str2enum(cls, priority:str):
        """
        Converts string representation of priority to corresponding enum

        Parameters:
            priority (str): the string representation of the priority ("Low", "Medium", or "High")

        Returns:
            Priority: the corresponding Priority enum value

        Raises:
            ValueError: If the provided priority string is not valid
        """
        str_list = cls.priority_options()

        # check to make sure its a valid priority
        if priority not in str_list:
            raise ValueError("Invalid Priority value")
        
        # return valid enum
        return Priority(str_list.index(priority))

    @staticmethod
    def priority_options():
        """Returns a list of stringified priority options"""
        return ["Low", "Medium", "High"]
    

class Frequency(Enum):
    """Enumeration for Recurrence.Frequency"""
    NO_REPEAT = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


    @staticmethod
    def frequency_options():
        """Returns a list of stringified priority options"""
        return ["Never Repeats", "Daily", "Weekly", "Monthly", "Yearly"]
    

    @staticmethod
    def is_no_repeat(frequency:"Frequency"):
        """Returns whether or not the frequency is NO_REPEAT"""
        return frequency.value == 0
    

    @classmethod
    def enum2str(cls, frequency:"Frequency") -> str:
        """Returns string representation of enum"""
        return cls.frequency_options()[frequency.value]
    

    @classmethod
    def str2enum(cls, frequency:str) -> "Frequency":
        """Returns enum based on input string"""
        str_list = cls.frequency_options()

        # check to make sure its a valid frequency
        if frequency not in str_list:
            raise ValueError("Invalid Frequency value")
        
        # return valid enum
        return Frequency(str_list.index(frequency))
    

    def get_next_date(self, current_date:datetime, original_date:datetime) -> datetime:
        """
        Returns time delta for the given frequency
        
        Parameters:
            current_date (datetime): the base date
            original_date (datetime): for MONTHLY, to force the day (after exception on previous date)
        """
        if self == Frequency.DAILY:
            return current_date + timedelta(days=1)
        
        elif self == Frequency.WEEKLY:
            return current_date + timedelta(weeks=1)
        
        elif self == Frequency.MONTHLY:
            # adjust month and year 
            adjusted_year = current_date.year + current_date.month // 12
            next_month = current_date.month % 12 + 1

            try:
                return current_date.replace(year=adjusted_year, month=next_month, day=original_date.day)
            
            # if next month has less days than current month, return last valid day
            except ValueError:
                next_next_month = next_month % 12 + 1 
                next_next_month_year = adjusted_year + next_month // 12
                next_next_first_day = current_date.replace(year=next_next_month_year, month=next_next_month, day=1)
                return next_next_first_day - timedelta(days=1)
        
        elif self == Frequency.YEARLY:
            next_year = current_date.year + 1

            # Handle leap years
            if current_date.month == 2 and current_date.day == 29:
                return current_date.replace(year=next_year, month=2, day=28)
            
            # Normal
            return current_date.replace(year=next_year)
        
    
