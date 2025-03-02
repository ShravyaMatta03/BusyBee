# Prologue Comments:
# Code Artifact: ToDoListView Class Definition
# Brief Description: This code defines the `ToDoListView` class, a screen used to display and manage  tasks in a to-do list. It provides a method to add tasks dynamically based on input data.
# Programmer: Matthew McManness (2210261), Manvir Kaur (3064194), and Magaly Camacho (3072618)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of ToDoListView structure  (placeholder for navigation) - [Matthew McManness]
#   - October 27, 2024: Created init, sort_tasks, add_task, and save_task function structure with initialization for what they will include to ToDoListView(Screen) and added in dummy task to display how tasks will look like - [Manvir Kaur]
#   - November 4, 2024: Updated add_task to connect to database, and added a method populate() that adds all tasks in the database - [Magaly Camacho]
#   - November 10, 2024: Added def on_task_click(self, task_id), refresh_tasks(self), toggle_complete(self, checkbox, task_id, task_box), grey_out_task(self, task_box), reset_task_appearance(self, task_box)  - [Matthew McManness]
#   - November 10, 2024: Fixed bug that crashed app when there's no due date. Added priority picker functionality - [Magaly Camacho]
#   - November 23, 2024: updated the populate function to handle recurrence - [Matthew McManness]
#   - November 23, 2024: tasks are displayed sorted by due date automatically - [Manvir Kaur]
#   - November 23, 2024: choosing a sorting option prints it to terminal instead of crashing - [Manvir Kaur]
#   - November 23, 2024: updating populate function to correctly sort all tasks according to the option selected - [Manvir Kaur]
#   - November 24, 2024: Implemented the filter_tasks fuction - [Matthew McManness]
#   - November 27, 2024: Drag-and-drop almost working as intended but you have to right-click to get a red dot to appear which you can the drag to drag and drop the task - [Manvir Kaur]
#   - December 06, 2024: Added an edit button for all tasks instead of just clicking the task so drag-and-drop can work without edit screen popping up - [Manvir Kaur]
#   - December 06, 2024: Fixed the drag-and-drop functionality to work perfectly! - [Manvir Kaur]
#   - December 07, 2024: Implemented variables for ease of UI modification - [Matthew McManness]
#   - December 08, 2024: Removed update_task_order since we do not need that based on our requirements - [Manvir Kaur]
#   - December 08, 2024: Theme toggling (Magaly Camacho)
#  - [Insert Further Revisions]: [Brief description of changes] - [Your Name]
# Preconditions:
#   - This class should be part of a ScreenManager in the Kivy application to function correctly.
# Acceptable Input:
#   - Valid task data must be passed to the `add_task` method in dictionary format.
# Unacceptable Input:
#   - Passing `None` or invalid data types to `add_task` will result in incorrect behavior.
# Postconditions:
#   - A new task is added and a message is logged to the console.
# Return Values:
#   - None. The task addition relies on side effects such as console logging.
# Error and Exception Conditions:
#   - If the `task_id` isn't valid, the method will not function correctly.
# Side Effects:
#   - Logs task addition messages to the console for debugging.
# Invariants:
#   - The `ToDoListView` must be part of the screen management system for correct rendering.
# Known Faults:
#   - When a new task is added, it's always added at the bottom instead of sorted in

# Imports
from kivy.uix.screenmanager import Screen  # to manage screen
from kivy.uix.boxlayout import BoxLayout  # base class for a task's box
from kivy.uix.checkbox import CheckBox  # checkbox widget (to mark complete/incomplete)
from kivy.uix.label import Label  # label widget to display text
from kivy.graphics import Color, Rectangle  # to control color and size of task background
from kivy.properties import ObjectProperty
from database import get_database  # to connect to database
from sqlalchemy import select  # to query database
from Models import Task  # task model class
from Models.databaseEnums import Priority  # for Task.priority
from kivy.app import App
from kivy.uix.dropdown import DropDown
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from Models import Category  # Ensure the Category model is imported
from sqlalchemy.sql import case
from kivy.uix.button import Button

db = get_database()  # get database

class UniformButton(Button):
    pass
class EditButton(UniformButton):
    pass

class TaskBox(BoxLayout):
    """A BoxLayout to hold task details"""
    task_id = ObjectProperty(None)
    categories = ObjectProperty(None)

    def __init__(self, on_click_callback, edit_callback, **kwargs):
        """Initialize the TaskBox with a callback for clicks."""
        super().__init__(**kwargs)
        self.on_click_callback = on_click_callback  # Set the callback attribute
        self.check_box = None  # Placeholder for checkbox reference
        self.edit_callback = edit_callback  # Callback for editing task

        # Attributes for drag-and-drop
        self.is_dragging = False
        self.initial_touch_pos = None
        
        # Initialize the size and background color of the TaskBox
        with self.canvas.before:
            app = App.get_running_app()
            Color(*app.Task_Box)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Update the rectangle size and position when TaskBox is resized
        self.bind(size=self.update_rect, pos=self.update_rect)

    def add_checkbox(self, callback):
        """Add a checkbox to the task box and bind it to a callback."""
        self.check_box = CheckBox(size_hint_x=0.1, color=App.get_running_app().Checkbox_Color)
        self.check_box.bind(on_release=callback)
        self.add_widget(self.check_box)

    def add_edit_button(self):
        """Adds an edit button for opening the edit modal."""
        edit_button = EditButton(
            text="Edit", 
            on_release=lambda instance: self.edit_callback(self.task_id)
        )
        self.add_widget(edit_button)
        self.edit_button = edit_button

    def update_rect(self, *args):
        """Update rectangle to match the size and position of the TaskBox."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        """Detect if the TaskBox was clicked but ignore if the checkbox was clicked."""
        if self.edit_button.collide_point(*touch.pos):
            return super().on_touch_down(touch)
            
        if self.check_box and self.check_box.collide_point(*touch.pos):
            # If clicking on the checkbox, do not trigger the task click callback
            return super().on_touch_down(touch)
            
        # Otherwise, proceed with the task box click event
        if self.collide_point(*touch.pos):
            if self.on_click_callback:
                self.on_click_callback(self.task_id)
                self.is_dragging = True
                self.initial_touch_pos = touch.y
            return True
        return super().on_touch_down(touch)
   
    def on_touch_move(self, touch):
        if self.is_dragging:
            self.y += touch.dy  # Move the task box with the touch
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.is_dragging:
            self.is_dragging = False

            # Check where the task was dropped
            task_list = self.parent
            siblings = [child for child in task_list.children if isinstance(child, TaskBox)]

            # Find the new position based on Y coordinates
            siblings.sort(key=lambda child: child.center_y, reverse=True)

            # Reorder the tasks in the UI
            task_list.clear_widgets()
            for sibling in siblings:
                task_list.add_widget(sibling)

            return True
        return super().on_touch_up(touch)
        
            
class ToDoListView(Screen):
    """A screen for displaying the To-Do List."""

    def __init__(self, **kwargs):
        """Initialize the ToDoListView screen."""
        super().__init__(**kwargs)  # Initialize the superclass with provided arguments.
        self.sort_by_dropdown = DropDown()
        self.current_sort = "Due Date"  # Default sorting criterion


    def add_task(self, task_id, name, priority=None, due_date=None, categories=None, complete=False):
        """Add a new task to the to-do list."""
        app = App.get_running_app()
        # Create a TaskBox and pass `on_task_click` as the click callback
        task_box = TaskBox(on_click_callback=self.on_task_click, edit_callback=self.on_edit_task_click, padding="15dp", spacing="5dp", size_hint_y=None, height="60dp", size_hint_x=1)
        task_box.task_id = task_id

        # Add checkbox for Task.complete and bind it to toggle_complete
        task_box.add_checkbox(lambda instance: self.toggle_complete(instance, task_id, task_box))
        task_box.check_box.active = complete  # Set initial checkbox state

        # Check/update info to display None if needed
        if due_date is None:
            due_date = "-" 
        if categories is None:
            categories = "-" 
        if priority is None:
            priority = "-"
            priority_color = app.Text_Color

        # Get priority text and color
        else:
            priority, priority_color = Priority.get_str_and_color(priority)
            priority_color = app.Priority_Colors[priority]

        priority_label = Label(text=priority, size_hint_x=0.1, color=priority_color)
        priority_label.id = "priority"

        # Add widgets to display task info
        task_box.add_widget(Label(text=name, size_hint_x=0.5, color=app.Text_Color))
        task_box.add_widget(Label(text=due_date, size_hint_x=0.3, color=app.Text_Color))
        task_box.add_widget(priority_label)
        task_box.add_widget(Label(text=categories, size_hint_x=0.5, color=app.Text_Color))
        
        task_box.add_edit_button()

        # Grey out task if already complete
        if complete:
            self.grey_out_task(task_box)

        # Add task box to task list layout
        self.ids.task_list.add_widget(task_box)

        print(f"Added task: {task_id}")  # Log the task addition

    def populate(self):
        """
        Populate the ToDoListView with tasks from the database, sorted based on the current_sort attribute.
        
        Postconditions:
            - Retrieves all tasks, including those created through recurrence.
            - Tasks are displayed in the to-do list, ordered by due date.
        """
        with db.get_session() as session:
            stmt = None  # Initialize stmt to avoid UnboundLocalError

            # Determine sorting order based on the selected option
            if self.current_sort == "Priority":
                # Define custom priority order: High (1), Medium (2), Low (3), None (-) as 4
                priority_order = case(
                    (Task.priority == 'HIGH', 1),
                    (Task.priority == 'MEDIUM', 2),
                    (Task.priority == 'LOW', 3),
                    else_=4  # For tasks without a priority, assign the lowest order
                )
                stmt = select(Task).order_by(priority_order)
            elif self.current_sort == "Due Date":
                stmt = select(Task).order_by(Task.due_date.asc())
            elif self.current_sort == "Category":
                # Sort by the name of the first associated category
                stmt = (
                    select(Task)
                    .outerjoin(Task.categories)  # Join tasks with categories
                    .order_by(func.coalesce(Category.name, "").asc())  # Order by category name, null-safe
                )
            else:
                # Default to sorting by Due Date
                stmt = select(Task).order_by(Task.due_date.asc())

            # Fetch tasks from the database
            tasks = session.scalars(stmt).all()

            # Debugging: Print fetched tasks and their sort order
            print(f"Sorting by: {self.current_sort}")
            for task in tasks:
                category_names = [cat.name for cat in task.categories] if task.categories else "-"
                print(f"Task: {task.name}, Priority: {task.priority}, Due Date: {task.due_date}, Categories: {category_names}")

            # Clear the current task list
            self.ids.task_list.clear_widgets()

            # Add each task to the list view
            for task in tasks:
                # Format due date as a string, or set to "-" if None
                due_date = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "-"

                # Format categories as a comma-separated string, or set to "-" if none exist
                categories = ", ".join([cat.name for cat in task.categories]) if task.categories else "-"

                # Add the task to the view
                self.add_task(task.id, task.name, task.priority, due_date, categories, complete=task.complete)

    def on_task_click(self, task_id):
        """Open the EditTaskModal for the clicked task."""
        print(f"Clicked task with ID: {task_id}")  # Debugging output
        app = App.get_running_app()
        #app.open_edit_task_modal(task_id)
    
    def refresh_tasks(self):
        """Refresh the list of tasks by reloading from the database."""
        self.ids.task_list.clear_widgets()  # Clear the current list
        self.populate()  # Re-populate with updated data from the database

    def toggle_complete(self, checkbox, task_id, task_box):
        """Toggle the completion status of a task."""
        complete = checkbox.active  # True if checked, False if unchecked

        # Update the task in the database
        with db.get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.complete = complete  # Assume `complete` is a field in the Task model
                session.commit()

        # Update the visual appearance of the task
        if complete:
            # Set text and background color to greyed-out
            self.grey_out_task(task_box)
        else:
            # Set text and background color back to normal
            self.reset_task_appearance(task_box)

    def grey_out_task(self, task_box):
        """Grey out the task's appearance."""
        app = App.get_running_app() # for theme settings
        # Change text color to grey
        for widget in task_box.children:
            if isinstance(widget, EditButton):
                continue

            if isinstance(widget, Label):
                widget.color = app.Box_Greyed_Out_Text #(0.5, 0.5, 0.5, 1)  # Grey color

        # Change background color to a lighter grey
        with task_box.canvas.before:
            Color(*app.Box_Greyed_Out)
            task_box.rect = Rectangle(size=task_box.size, pos=task_box.pos)

        # Bind update_rect on task_box to keep the grey background consistent
        task_box.bind(size=task_box.update_rect, pos=task_box.update_rect)


    def reset_task_appearance(self, task_box):
        """Reset the task's appearance to its original color."""
        app = App.get_running_app() # get app for theme config

        # Reset text color 
        for widget in task_box.children:
            if isinstance(widget, EditButton):
                continue

            if isinstance(widget, Label):
                if hasattr(widget, "id") and widget.id == "priority":
                    widget.color = app.Priority_Colors[widget.text]
                else:
                    widget.color = app.Text_Color  # Original black color

        # Reset background color
        with task_box.canvas.before:
            Color(*app.Task_Box)
            task_box.rect = Rectangle(size=task_box.size, pos=task_box.pos)

        # Bind update_rect on task_box to maintain the white background
        task_box.bind(size=task_box.update_rect, pos=task_box.update_rect)

    def sort_tasks(self, sort_option):
        """
        Updates the sorting criteria based on the selected sort option and repopulates the list.

        Args:
            sort_option (str): The selected sorting option (e.g., "Priority", "Due Date", "Name").
        """
        print(f"Sorting by: {sort_option}")
        self.current_sort = sort_option  # Update the current sorting option
        self.refresh_tasks()  # Refresh the list to apply the new sorting

    def filter_tasks(self, priority_filter):
        """
        Filter tasks based on the selected priority level.

        Args:
            priority_filter (str): The selected priority filter (e.g., "High", "Medium", "Low", "-", "All").
        """
        if priority_filter == "All":
            print("Displaying all tasks.")
            self.populate()  # Reset and show all tasks
            return

        # Handle the "-" option to display tasks with no priority
        if priority_filter == "-":
            print("Displaying tasks with no priority.")
            with db.get_session() as session:
                tasks = session.query(Task).filter(Task.priority == None).all()  # Fetch tasks with NULL priority

                # Debugging: Log tasks with no priority
                print(f"Tasks with no priority:")
                for task in tasks:
                    print(f"Task: {task.name}, Priority: {task.priority}")

                # Clear the current task list and add filtered tasks
                self.ids.task_list.clear_widgets()
                for task in tasks:
                    due_date = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "-"
                    categories = ", ".join([cat.name for cat in task.categories]) if task.categories else "-"
                    self.add_task(task.id, task.name, task.priority, due_date, categories, complete=task.complete)

            return  # Exit the method after handling "-"

        try:
            # Convert the priority filter to the appropriate enum
            priority_enum = Priority.str2enum(priority_filter)
        except ValueError:
            print(f"Invalid Priority value: {priority_filter}")
            return

        # Query tasks filtered by the selected priority
        with db.get_session() as session:
            tasks = session.query(Task).filter_by(priority=priority_enum).all()

            # Debugging: Log tasks for the selected priority
            print(f"Filtering tasks by priority: {priority_filter}")
            for task in tasks:
                print(f"Task: {task.name}, Priority: {task.priority}")

            # Clear the current task list and add filtered tasks
            self.ids.task_list.clear_widgets()
            for task in tasks:
                due_date = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "-"
                categories = ", ".join([cat.name for cat in task.categories]) if task.categories else "-"
                self.add_task(task.id, task.name, task.priority, due_date, categories, complete=task.complete)

    def on_edit_task_click(self, task_id):
        """Opens the edit modal when the edit button is clicked."""
        print(f"Edit button clicked for task with ID: {task_id}")
        app = App.get_running_app()
        app.open_edit_task_modal(task_id)
