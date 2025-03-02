# -----------------------------------------------------------------------------
# Name: addtask.py
# Description: This module defines the AddTaskModal class, which provides a 
#              modal interface to create and save tasks within the BusyBee 
#              application.
# Programmer: Matthew McManness (2210261)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created (Author: Matthew McManness)
# - October 27, 2024: Updated to include proper comments (Matthew McManness)
# - November 4, 2024: Added connection to database to save tasks (Magaly Camacho)
# - November 10, 2024: Fixed bug where app crashed when there wasn't a due date. Added priority picker functionality (Magaly Camacho)
# - November 18, 2024: Updated default frequency string (Magaly Camacho)
# - November 23, 2024: Updated the save_task function to handle recurrence (Matthew McManness)
# - December 7, 2024: Implemented variables for ease of UI modification (Matthew McManness)
# - December 8, 2024: Theme toggling (Magaly Camacho)
#
# Preconditions:
# - Kivy framework must be installed and configured properly.
# - The `DatePicker` and `RepeatOptionsModal` must be accessible within 
#   screens/usefulwidgets.
#
# Postconditions:
# - This modal saves task data and adds it to the To-Do ListView.
#
# Error Handling:
# - If the task title is missing, the task will not be saved, and an error 
#   message will be printed to the console.
#
# Side Effects:
# - Updates the category list and modifies the To-Do ListView when tasks are added.
# Known Faults:
# - Priority picker needs to be implemented
# -----------------------------------------------------------------------------

# Import necessary Kivy modules and custom widgets
from kivy.uix.modalview import ModalView  # Modal for task creation
from kivy.uix.boxlayout import BoxLayout  # Layout for organizing widgets
from kivy.uix.textinput import TextInput  # Input fields for user text
from kivy.uix.spinner import Spinner  # Dropdown-style component
from kivy.uix.button import Button  # Standard button widget
from screens.usefulwidgets import DatePicker # Date picker
from screens.usefulwidgets import RepeatOptionsModal, PriorityOptionsModal, CategoryModal  # Additional modals
from kivy.uix.label import Label  # Label widget for displaying text
from kivy.app import App  # Ensure App is imported
from Models import Task, Category # Task and Category classes
from Models.databaseEnums import Priority, Frequency # for task priorities and frequency
from database import get_database # to connect to database
from sqlalchemy import select # to query database
from datetime import datetime # for Task.due_date
from Models import Recurrence  # Import the Recurrence model
from kivy.metrics import dp  # Import dp for density-independent pixel values
from kivy.graphics import Color, RoundedRectangle  # For rounded rectangle shape


class UniformButton(Button):
    pass

class UniformSpinner(Spinner):
    pass

db = get_database() # get database

class AddTaskModal(ModalView):
    """
    A modal for adding a new task to the To-Do List.

    Attributes:
        categories (list): List of predefined task categories.
        selected_categories (list): List of user-selected categories for the task.
    """

    def __init__(self, refresh_callback=None, **kwargs):
        """
        Initialize the AddTaskModal with layout components.

        Args:
            refresh_callback (function, optional): A callback function to refresh the ToDoListView.
            **kwargs: Additional arguments passed to the superclass.

        Preconditions:
            - The `refresh_callback` should be a callable function or None.
        """
        super().__init__(**kwargs)
        self.refresh_callback = refresh_callback  # Store the refresh callback
        self.size_hint = (0.99, 0.9)  # Set modal size
        self.auto_dismiss = False  # Prevent accidental dismissal

        self.recurrence = None  # Initialize recurrence as None
        # Access app-wide styles
        app = App.get_running_app()

        # Initialize categories and the selected category list
        with db.get_session() as session, session.begin():
            stmt = select(Category).where(True) # sql statement
            results = session.scalars(stmt).all() # query the database for all categories
            self.categories = [result.name for result in results] # save the names of all categories in the database
            self.categories_ids = [result.id for result in results] # cache ids
        self.selected_categories = [] # initially none

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add a custom background color with rounded corners
        with layout.canvas.before:
            Color(rgba=app.Background_Color)  # Use the app's background color
            self.bg_rect = RoundedRectangle(
                pos=layout.pos,
                size=layout.size,
                radius=[dp(20)]
            )

        # Bind the position and size of the layout to update the background rectangle dynamically
        layout.bind(pos=self.update_background, size=self.update_background)

        # Input field for the task title
        self.title_input = TextInput(hint_text="Task Title")
        layout.add_widget(self.title_input)

        # Deadline section with a label and date picker button
        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(
            text="Pick a deadline",
            color=app.Text_Color,  # RGBA format for black color
            font_size=app.button_font_size,
            size_hint_x=0.8
        )
        deadline_layout.add_widget(self.deadline_label)
        pick_date_button = UniformButton(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(pick_date_button)
        layout.add_widget(deadline_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = UniformButton(text=Frequency.frequency_options()[0], on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)
        
        # Button to open the Priority Options modal
        self.priority_button = UniformButton(text="Pick Priority", on_release=self.open_priority_window)
        layout.add_widget(self.priority_button)

        # Input field for additional task notes
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner for category selection
        category_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.category_spinner = UniformSpinner(
            text="Select Category",
            values=self.categories + ["Add New Category"],
            size_hint=(0.7, None),
            height=44
        )
        self.category_spinner.bind(text=self.on_category_selected)
        category_layout.add_widget(self.category_spinner)
        layout.add_widget(category_layout)

        # Display selected categories dynamically
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons for canceling or saving the task
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(UniformButton(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(UniformButton(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add the layout to the modal

    def open_date_picker(self, instance):
        """Open the DatePicker modal to select a deadline."""
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        RepeatOptionsModal(self).open()

    def open_priority_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        PriorityOptionsModal(self).open()

    def on_category_selected(self, spinner, text):
        """
        Handle category selection from the spinner.

        Args:
            spinner (Spinner): The spinner instance.
            text (str): The selected text from the spinner.
        """
        if text == "Add New Category":
            CategoryModal(self).open()  # Open modal to add a new category
        elif text not in self.selected_categories:
            self.selected_categories.append(text)  # Add the selected category
            self.update_applied_categories()  # Refresh the display

    def update_applied_categories(self):
        """Update the layout displaying selected categories."""
        self.applied_categories_layout.clear_widgets()  # Clear previous widgets
        for category in self.selected_categories:
            label = Label(text=category)
            self.applied_categories_layout.add_widget(label)

    def update_category_spinner(self):
        """Update the category spinner with the latest categories."""
        self.category_spinner.values = self.categories + ["Add New Category"]

    def save_task(self, *args):
        """
        Save the new task to the database.

        Args:
            *args: Additional arguments passed by the event handler.

        Postconditions:
            - A new task is created and added to the database.
            - Additional tasks are created based on the recurrence if specified.
            - Refreshes the to-do list view after saving the task.
        """
        if not self.title_input.text:
            print("Task Title is required.")  # Error message for missing title
            return

        # Collect data
        name = self.title_input.text
        notes = self.notes_input.text
        due_date = self.deadline_label.text.split(" ", 1)[1] if "Deadline" in self.deadline_label.text else None

        # Ensure a valid due_date is provided if recurrence is specified
        if self.recurrence and not due_date:
            print("Due date is required for recurring tasks.")  # Debugging message
            return

        # Convert due_date to a datetime object
        due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M") if due_date else None
        priority = Priority.str2enum(self.priority_button.text) if "Pick Priority" != self.priority_button.text else None

        # Ensure self.recurrence is None if "Does not Repeat" is selected or untouched
        if self.recurrence is None or self.repeat_button.text == Frequency.frequency_options()[0]:
            self.recurrence = None

        # Retrieve category instances
        selected_categories_ids = [cat_id for cat_id, cat in zip(self.categories_ids, self.categories) if cat in self.selected_categories]

        with db.get_session() as session:
            # Create the main task
            task = Task(
                name=name,
                notes=notes,
                due_date=due_date,
                priority=priority
            )
            task.categories = session.query(Category).filter(Category.id.in_(selected_categories_ids)).all()
            session.add(task)
            session.flush()  # Get task ID immediately

            # Add recurrence if specified
            if self.recurrence:
                recurrence = Recurrence(
                    frequency=self.recurrence["frequency"],
                    times=self.recurrence["times"]
                )
                session.add(recurrence)
                session.flush()
                task.recurrence_id = recurrence.id

                # Create repeated tasks based on recurrence
                next_date = due_date
                for _ in range(self.recurrence["times"] - 1):  # Subtract 1 because the first task is already created
                    next_date = recurrence.frequency.get_next_date(next_date, due_date)
                    if not next_date:  # Debugging check for invalid dates
                        print("Error: next_date calculation returned None.")
                        break
                    repeated_task = Task(
                        name=name,
                        notes=notes,
                        due_date=next_date,
                        priority=priority,
                        recurrence_id=recurrence.id
                    )
                    repeated_task.categories = task.categories
                    session.add(repeated_task)

             # Capture the task ID before the session is closed
            task_id = task.id

            # Commit all changes
            session.commit()

        # Refresh the to-do list view if a callback is provided
        if self.refresh_callback:
            self.refresh_callback()

        print(f"Task saved with ID: {task_id}")
        self.dismiss()

    def update_background(self, *args):
        """Update the size and position of the background rectangle."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
