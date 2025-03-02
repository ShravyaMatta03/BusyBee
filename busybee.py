# -----------------------------------------------------------------------------
# Name: busybee.py
# Description: This module contains the main application logic for the BusyBee 
#              app. It manages the screens and provides functionality to open 
#              task/event modals.
# Programmer: Matthew McManness (2210261), Magaly Camacho (3072618), Manvir Kaur (3064194)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created. (Author: Matthew McManness)
# - October 27, 2024: Current version created (added comments). (Updated by: Matthew McManness)
# - November 4, 2024: Added call to To Do list view so that tasks already in the database are populated (Updated by: Magaly Camacho)
# - November 11, 2024: Added open_edit_task_modal(self, task_id) (Updated by: Matthew McManness)
# - November 24, 2024: Added switch_to_daily_view_today to facilitate seeing the daily view (Matthew McManness)
# - November 24,2024: Resolved conflicts to merch testing-1 branch with main (Magaly Camacho)
# - December 6, 2024: Implemented variables for ease of UI modification (Matthew McManness)
# - December 7, 2024: Added theme toggling functionality (Magaly Camacho)
# - December 8, 2024: Theme toggling improved (Magaly Camacho)
#
# Preconditions:
# - Kivy must be installed and properly configured in the Python environment.
# - The `screens` directory must contain the required screen classes 
#   (CalendarView, ToDoListView, AddEventModal, AddTaskModal).
#
# Acceptable Input:
# - Screen names such as "calendar" and "todo" for switching screens.
#
# Unacceptable Input:
# - Inputting an invalid screen name will raise an error in screen switching.
#
# Postconditions:
# - If all modules are loaded properly, the application will open the main window 
#   with a screen manager to switch between screens.
#
# Return Values:
# - None. This class initializes and runs the Kivy application.
#
# Error and Exception Conditions:
# - ImportError: Raised if the screen classes or modals are not found.
# - RuntimeError: Raised if the Kivy environment is not properly initialized.
#
# Side Effects:
# - Adds multiple screens to the screen manager.
#
# Invariants:
# - ScreenManager should always contain at least two screens: CalendarView and 
#   ToDoListView.
#
# Known Faults:
# - None identified at the time of writing.
# -----------------------------------------------------------------------------

# Import necessary modules
from kivy.app import App  # Main class for running Kivy applications
from kivy.uix.screenmanager import ScreenManager, NoTransition  # Manage screens and transitions

# Import screen classes from the screens directory
from screens.calendarview import CalendarView # Import the Calendar View class
from screens.todolistview import ToDoListView # Import the TodoListView class
from screens.addevent import AddEventModal # Import the add event modal
from screens.addtask import AddTaskModal # Import the add task modal
from screens.edittask import EditTaskModal  # Import the edit modal
from screens.editEvent import EditEventModal # Import the edit event modal
from kivy.uix.screenmanager import ScreenManager
from screens.dailyview import DailyView # Import the daily view class
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from theme import Theme


# -----------------------------------------------------------------------------
# Main Application Class: BusyBeeApp
# This class manages the screens and provides functionality to open modals.
# -----------------------------------------------------------------------------
class BusyBeeApp(App):
    """Main app class to manage screens and modals."""

    #Variables:

    #Sizes
    button_font_size = NumericProperty((Window.width + Window.height) * 0.018)
    title_font_size = NumericProperty((Window.width + Window.height) * 0.03)
    label_font_size = NumericProperty((Window.width + Window.height) * 0.015)
    button_size = NumericProperty((Window.width + Window.height) * 0.025)

    # Colors - Initialize to Light Mode
    current_theme = Theme.LIGHT
    theme_settings = current_theme.get_settings()

    Title_Color = theme_settings["Title_Color"]
    Title_Background = theme_settings["Title_Background"]

    Subtitle_Color = theme_settings["Subtitle_Color"]
    Background_Color = theme_settings["Background_Color"]

    Text_Color = theme_settings["Text_Color"]
    Checkbox_Color = theme_settings["Checkbox_Color"]

    Button_Color = theme_settings["Button_Color"]
    Button_Text = theme_settings["Button_Text"]

    Event_Button = theme_settings["Event_Button"]
    Event_Button_Text = theme_settings["Event_Button_Text"]
    
    Task_Box = theme_settings["Task_Box"]
    Event_Box = theme_settings["Event_Box"]
    Event_More_Label = theme_settings["Event_More_Label"]
    Box_Greyed_Out = theme_settings["Box_Greyed_Out"]
    Box_Greyed_Out_Text = theme_settings["Box_Greyed_Out_Text"]

    Date_Selected = theme_settings["Date_Selected"]
    Date_Selected_Text = theme_settings["Date_Selected_Text"]

    Edit_Button_Color = theme_settings["Edit_Button_Color"]
    Edit_Button_Text = theme_settings["Edit_Button_Text"]

    Weekday_Background = theme_settings["Weekday_Background"]
    Weekday_Color = theme_settings["Weekday_Color"]

    Priority_Colors = theme_settings["Priorities"]

    def build(self):
        """
        Initialize the screen manager and add the CalendarView and ToDoListView screens.

        Preconditions:
        - ScreenManager must be correctly initialized.

        Postconditions:
        - CalendarView and ToDoListView screens are added to the screen manager.

        Return:
        - Returns the initialized ScreenManager instance.
        """
        self.screen_manager = ScreenManager(transition=NoTransition())  # Initialize ScreenManager


        # Initialize To Do list view
        todo = ToDoListView(name="todo")
        todo.populate() # add existing tasks 

        # Add the CalendarView and ToDoListView screens to the manager
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(todo)
        self.screen_manager.add_widget(DailyView(name="daily"))

        return self.screen_manager  # Return the configured ScreenManager

    def open_add_task_modal(self):
        """
        Open the AddTaskModal for creating a new task.

        Preconditions:
        - The ToDoListView screen must be accessible from the ScreenManager.

        Postconditions:
        - Displays the AddTaskModal for user input.
        - Passes the refresh_tasks callback from ToDoListView to the AddTaskModal.
        """
        # Use the correct screen name ('todo' as defined in build)
        todo_list_view = self.root.get_screen('todo')

        if hasattr(todo_list_view, 'refresh_tasks'):  # Ensure the callback exists
            # Pass refresh_tasks to the AddTaskModal
            add_task_modal = AddTaskModal(refresh_callback=todo_list_view.refresh_tasks)
            add_task_modal.open()
        else:
            print("Error: ToDoListView does not have a refresh_tasks method.")

    def open_add_event_modal(self):
        """
        Open the Add Event modal.

        Preconditions:
        - AddEventModal must be properly imported.

        Postconditions:
        - The Add Event modal will open.

        Side Effects:
        - Opens the Add Event modal view.

        Errors:
        - ImportError: If AddEventModal is not found.

        Return:
        - None.
        """
        add_event_modal = AddEventModal()  # Create an instance of AddEventModal
        add_event_modal.open()  # Open the modal

    def switch_to_screen(self, screen_name):
        """
        Switch between Calendar and To-Do List screens.

        Preconditions:
        - `screen_name` must be a valid screen name (either "calendar" or "todo").

        Postconditions:
        - The specified screen will become active.

        Side Effects:
        - Changes the active screen.

        Errors:
        - ValueError: If the provided screen name is not valid.

        Parameters:
        - screen_name (str): The name of the screen to switch to.

        Return:
        - None.
        """
        self.screen_manager.current = screen_name  # Change the active screen

    def open_edit_task_modal(self, task_id):
        """
        Open the Edit Task modal for a specific task.

        Args:
        - task_id (int): ID of the task to edit.

        Postconditions:
        - The Edit Task modal will open with the task data preloaded.
        """
        """Open the Edit Task modal for a specific task."""
        # Get the ToDoListView instance to access its refresh_tasks method
        todo_screen = self.screen_manager.get_screen("todo")
        
        # Create the EditTaskModal and pass the task ID and refresh callback
        edit_task_modal = EditTaskModal(task_id=task_id, refresh_callback=todo_screen.refresh_tasks)
        edit_task_modal.open()

    def switch_to_daily_view_today(self):
        """Switch to the DailyView screen and set it to the current day."""
        daily_view = self.screen_manager.get_screen("daily")  # Get the Daily View screen
        daily_view.current_date = datetime.now()  # Set to today's date
        daily_view.update_date_label()  # Update the date label
        daily_view.populate_events()  # Populate today's events
        self.screen_manager.current = "daily"  # Switch to the Daily View screen

    def toggle_theme(self):
        """Toggle theme between light and dark mode"""
        # get new theme and save
        self.current_theme = Theme.toggle(self.current_theme)
        theme_settings = self.current_theme.get_settings()
        self.set_theme_settings(theme_settings)

        # reload screens
        screens = [self.screen_manager.get_screen(screen_name) for screen_name in ["daily", "calendar", "todo"]]
        for screen in screens:
            screen.__init__()

        # re-add tasks
        self.root.get_screen('todo').populate()

    def set_theme_settings(self, theme_settings:dict):
        """Set color variables based on theme settings"""
        self.Title_Color = theme_settings["Title_Color"]
        self.Title_Background = theme_settings["Title_Background"]

        self.Subtitle_Color = theme_settings["Subtitle_Color"]
        self.Background_Color = theme_settings["Background_Color"]

        self.Text_Color = theme_settings["Text_Color"]
        self.Checkbox_Color = theme_settings["Checkbox_Color"]

        self.Button_Color = theme_settings["Button_Color"]
        self.Button_Text = theme_settings["Button_Text"]

        self.Event_Button = theme_settings["Event_Button"]
        self.Event_Button_Text = theme_settings["Event_Button_Text"]
        
        self.Task_Box = theme_settings["Task_Box"]
        self.Event_Box = theme_settings["Event_Box"]
        self.Event_More_Label = theme_settings["Event_More_Label"]
        self.Box_Greyed_Out = theme_settings["Box_Greyed_Out"]
        self.Box_Greyed_Out_Text = theme_settings["Box_Greyed_Out_Text"]

        self.Date_Selected = theme_settings["Date_Selected"]
        self.Date_Selected_Text = theme_settings["Date_Selected_Text"]

        self.Edit_Button_Color = theme_settings["Edit_Button_Color"]
        self.Edit_Button_Text = theme_settings["Edit_Button_Text"]

        self.Weekday_Background = theme_settings["Weekday_Background"]
        self.Weekday_Color = theme_settings["Weekday_Color"]

        self.Priority_Colors = theme_settings["Priorities"]
        


def open_edit_event_modal(self, event_id):
    edit_event_modal = EditEventModal(event_id=event_id, refresh_callback=self.populate)
    edit_event_modal.open()
