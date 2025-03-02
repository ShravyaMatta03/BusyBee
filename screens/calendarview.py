# Prologue Comments:
# Code Artifact: CalendarView Class Definition
# Brief Description: This code defines the `CalendarView` class for displaying a monthly calendar
# with functionality to navigate months and select days. It also updates the display with the 
# current month and year and populates the calendar dynamically using a grid layout.
# Programmer: Matthew McManness (2210261), Manvir Kaur (3064194), Mariam Oraby (3127776)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of calendar view structure (just a placeholder for navigation) - [Matthew McManness]
#   - November 9, 2024: Added EventBox to add new events to calendar, connection to the database to add all events to the database and show up on the calendar whenever a new event is added or the app is opened. Added widgets to display event info - [Manvir Kaur]
#   - November 9, 2024: Fixed the color, created relative layout for each day cell and added the day button to each cell. Did some debugging - [Manvir Kaur]
#   - November 9, 2024: Updated the populate(), get_cell_widgets(), and populate_calendar() functions - [Mariam Oraby]
#   - November 10, 2024: Updated what Manvir and Mariam added to make it stack events correctly - [Matthew McManness]
#   - November 10, 2024: updated the calendar view so that the week starts on a Sunday - Matthew McManness
#   - November 10, 2024: Group modified to ensure event button clicks open the edit modal - [Whole Group]
#   - November 18, 2024: Implemented recurring events - [Magaly Camacho]
#   - December 5, 2024: Redid the add_event() to truncate names that were too long and added a hover feature to display the full name and time of events [Matthew McManness]
#   - December 6, 2024: changed the populate_calendar() to call open_daily_view() when a day is pressed and created open_daily_view() (to see the details of days when there are more than two events) - [Matthew McManness] 
#   - December 7, 2024: Fixed setting date for dailyview - [Magaly Camacho, Mariam Oraby]
#   - December 7, 2024: Removed EventBox class since it wasn't used - [Magaly Camacho]
#   - December 8, 2024: Theme toggling (Magaly Camacho)
#
# Preconditions:
#   - The `.kv` file must define a `calendar_grid` widget ID to correctly render the calendar grid.
#   - The app must have valid Kivy widgets and dependencies available (e.g., Button, Label, etc.).
# Acceptable Input:
#   - Increment values of 1 or -1 to navigate months.
#   - A day button press to select a specific day.
# Unacceptable Input:
#   - Increment values outside expected range result in incorrect month/year changes.
# Postconditions:
#   - The calendar view updates with the current month and day selection.
#   - Displays a console message when a day is selected.
# Return Values:
#   - None. The methods rely on UI updates and side effects.
# Error and Exception Conditions:
#   - If `calendar_grid` ID is not found, it logs an error message.
# Side Effects:
#   - Updates the calendar dynamically on month changes or day selection.
# Invariants:
#   - The view always displays the current month and updates on navigation.
# Known Faults:
#   - None identified.

# Import necessary modules from Kivy and Python standard libraries.
from kivy.graphics import Color, Rectangle # to control color and size of event background
from kivy.lang import Builder  # Load .kv files for UI definitions.
from kivy.uix.boxlayout import BoxLayout  # Organize widgets horizontally/vertically.
from kivy.uix.modalview import ModalView  # Define modals (pop-up windows).
from kivy.uix.popup import Popup  # Create pop-ups (used for date picker).
from kivy.uix.label import Label  # Display text in the UI.
from kivy.uix.gridlayout import GridLayout  # Arrange widgets in a grid layout.
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen  # Manage screens.
from kivy.uix.textinput import TextInput  # Input field for text entry.
from kivy.uix.button import Button  # Standard button widget.
from kivy.uix.spinner import Spinner  # Dropdown for selecting from options.
from kivy.uix.relativelayout import RelativeLayout  # Layout used in calendar population.
from kivy.metrics import dp  # Use density-independent pixels for UI scaling.
from kivy.properties import StringProperty, ObjectProperty  # Property to update UI reactively.
from kivy.app import App  # Main class to run the Kivy app.
from kivy.clock import Clock  # Schedule functions after a delay.
from calendar import monthcalendar  # Generate calendar layout for a given month.
from datetime import datetime, timedelta  # Work with dates and times.
from database import get_database # to connect to database
from sqlalchemy import select, extract # to query database
from Models import Event_ # task model class
from kivy.uix.anchorlayout import AnchorLayout  # Import for anchoring widgets
from kivy.graphics import Color, Rectangle, RoundedRectangle  # Import for rounded rectangle backgrounds
import calendar  # Import calendar for setting first day of the week
from screens.editEvent import EditEventModal  # Adjust the path if the file is located elsewhere
from kivy.app import App  # Access the app instance for global styles



class UniformButton(Button):
    pass

class EventButton(UniformButton):
    pass


# Set the first day of the week to Sunday
calendar.setfirstweekday(calendar.SUNDAY)

db = get_database()  # Get database
        
class CalendarView(Screen):
    """Displays a monthly calendar with navigational buttons and day selection."""

    month_year_text = StringProperty()  # Reactive property for month and year text.
    modal_open = False

    def __init__(self, **kwargs):
        """Initialize the calendar with the current month and year."""
        super().__init__(**kwargs)  # Initialize the superclass.
        now = datetime.now()  # Get the current date and time.
        self.current_year = now.year  # Store the current year.
        self.current_month = now.month  # Store the current month.
        self.update_month_year_text()  # Update the month-year text display.

    def on_kv_post(self, base_widget):
        """Populate the calendar after the KV file has loaded."""
        if 'calendar_grid' in self.ids:  # Check if the grid is defined in the KV file.
            # Use the Clock to schedule the population to ensure the UI is fully loaded.
            Clock.schedule_once(lambda dt: self.populate_calendar())
        else:
            print("Error: 'calendar_grid' not found in ids.")  # Log error if grid not found.

    def update_month_year_text(self):
        """Update the label to show the current month and year."""
        self.month_year_text = datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def change_month(self, increment):
        """Change the month based on the given increment and repopulate the calendar."""
        self.current_month += increment  # Adjust the month.
        # Handle year change when month goes out of bounds.
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_month_year_text()  # Update the month-year text.
        self.populate_calendar()  # Repopulate the calendar grid.

    def populate_calendar(self):
        """Generate the calendar grid with day buttons."""
        grid = self.ids['calendar_grid']  # Get the calendar grid from the KV file.
        grid.clear_widgets()  # Clear any existing widgets from the grid.

        # Get the calendar layout for the current month.
        cal = monthcalendar(self.current_year, self.current_month)

        # Populate the grid with days of the month.
        for week in cal:
            for day in week:
                if day == 0:
                    # Add an empty label for non-days (blank spaces).
                    grid.add_widget(Label())
                else:
                    # Create a relative layout for each day cell.
                    cell = BoxLayout(orientation='vertical', spacing=-20)
                    container = RelativeLayout(size_hint=(1, None), height=dp(60))

                    # Create a label to display the day number.
                    day_label = Label(
                        text=str(day),
                        size_hint=(None, None),
                        size=(dp(20), dp(20)),
                        pos_hint={'right': 1, 'top': 1},
                        color= App.get_running_app().Text_Color  
                    )

                    # Create a button for the day, which responds to clicks.
                    day_button = Button(
                        background_normal="",
                        background_color=App.get_running_app().Event_Box, 
                        on_press=lambda instance, day=day: self.open_daily_view(day),  # Open DailyView on press.
                        size_hint=(1, 1),  # Make the button fill the cell.
                        text=""  # No text on the button itself.
                    )

                    # Add the button and label to the cell.
                    container.add_widget(day_button)
                    cell.add_widget(day_label)
                    container.add_widget(cell)

                    # Add the cell to the calendar grid.
                    grid.add_widget(container)
        self.populate()

    def add_event(self, event_id, name, start_time, frequency=None, times=None, place=None):
        """
        Add a new event to the calendar.
        """
        # Define a character limit for truncation
        char_limit = 9  # Adjust this value as needed

        # Truncate the event name if it exceeds the character limit
        display_name = name if len(name) <= char_limit else f"{name[:char_limit]}..."

        # Ensure start_time is a datetime object
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')

        # Create the event button
        event_button = EventButton(
            text=display_name,
            size_hint_y=None,
            height=dp(15),
            background_normal="",
            on_press=lambda instance, event_id=event_id: self.open_edit_event_modal(event_id)  # Pass event ID to the method
        )

        # Set font_size explicitly after creation
        event_button.font_size = dp(12)
        event_button.height = dp(15)

        # event box to separate event buttons
        event_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(18), padding=(0, 3))
        event_box.add_widget(event_button)

        # Retrieve the cell widget for the event's start date
        cell = self.get_cell_widget(start_time)
        if cell:
            # Ensure AnchorLayout for events exists
            if not cell.children or not isinstance(cell.children[0], AnchorLayout):
                anchor_layout = AnchorLayout(anchor_y='top', size_hint_y=None, height=dp(60))
                events_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=(5, 5))
                events_layout.bind(minimum_height=events_layout.setter('height'))
                anchor_layout.add_widget(events_layout)
                cell.add_widget(anchor_layout)
            else:
                events_layout = cell.children[0].children[0]

            # Add the event button only if fewer than 2 events are currently displayed
            displayed_events = [child for child in events_layout.children if isinstance(child, BoxLayout)]
            if len(displayed_events) < 2:
                events_layout.add_widget(event_box)

            # Add "More..." label if there are more than 2 events
            if len(displayed_events) == 2:
                # Ensure the "More..." label exists only once
                more_label_layout = next(
                    (child for child in events_layout.children if isinstance(child, AnchorLayout) and child.anchor_y == "bottom"),
                    None
                )
                if not more_label_layout:
                    more_label_layout = AnchorLayout(anchor_y="bottom", size_hint_y=None, height=dp(15), padding=(0,0))
                    more_label = Label(
                        text="More...",
                        font_size=dp(12),
                        size_hint=(None, None),
                        height=dp(15),
                        color=App.get_running_app().Event_More_Label  # Grey color for the "More..." label
                    )
                    more_label_layout.add_widget(more_label)
                    events_layout.add_widget(more_label_layout)

            print(f"Added event: {event_id} - {display_name} on {start_time}")

    def get_cell_widget(self, date_obj):
        """Retrieve the widget for the specified date."""
        # Parse the date string into a datetime object
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M')

        target_day = date_obj.day
        target_month = date_obj.month
        target_year = date_obj.year

        # Check if the date is in the current calendar view
        if target_month != self.current_month or target_year != self.current_year:
            print("Error: The specified date is not in the current month or year.")
            return None

        # Get the calendar layout for the current month
        cal = monthcalendar(self.current_year, self.current_month)

        # Locate the widget for the target day in calendar_grid
        grid = self.ids['calendar_grid']
        widget_index = 0
        for week in cal:
            for day in week:
                if day == target_day:
                    # Found the target day; retrieve the widget
                    return grid.children[len(grid.children) - widget_index - 1]
                widget_index += 1

        print("Error: Day widget not found.")
        return None
    
    def refresh_calendar(self):
        grid = self.ids['calendar_grid']  # Get the calendar grid from the KV file.
        grid.clear_widgets()  # Clear any existing widgets from the grid.
        self.populate_calendar()

    def populate(self):
        """Retrieve and display events for the current month."""
        session = db.get_session()
        try:
            stmt = select(Event_).where(
                extract("year", Event_.start_time) == self.current_year,
                extract("month", Event_.start_time) == self.current_month
            )
            events = session.scalars(stmt).all()
            events.sort(key=lambda event: event.start_time)  # Sort events by start time

            for event in events:
                start_time = event.start_time if isinstance(event.start_time, datetime) else datetime.strptime(event.start_time, "%Y-%m-%d %H:%M")
                self.add_event(event.id, event.name, start_time, event.place)
        finally:
            session.close()

    def open_edit_event_modal(self, event_id):
        """Open the Edit Event modal for a specific event ID and refresh calendar upon save."""
        self.modal_open = True
        edit_event_modal = EditEventModal(event_id=event_id, refresh_callback=self.refresh_calendar)

        # Reset modal_open when the modal is dismissed
        def reset_modal_open(*args):
            self.modal_open = False

        edit_event_modal.bind(on_dismiss=reset_modal_open)
        edit_event_modal.open()

    def open_daily_view(self, day):
        """Open the DailyView for the selected day."""
        selected_date = datetime(self.current_year, self.current_month, day)
        daily_view = self.manager.get_screen('daily')  # Access the DailyView screen.
        daily_view.current_date = selected_date  # Pass the selected date.
        daily_view.selected_date = selected_date  # Pass the selected date.
        daily_view.set_date()  # Display correct date label and add events
        self.manager.transition.direction = 'left'  # Slide transition.
        self.manager.current = 'daily'  # Switch to the DailyView screen.

