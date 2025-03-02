# ----------------------------------------------------------------------------- 
# Name: editEvent.py 
# Description: This module defines the EditEventModal class, which provides a
#              modal interface to edit an event within the BusyBee application.
# Programmer: Shravya Matta
# Date Created: November 8, 2024
# Revision History:
# - November 8, 2024: Initial version created for editing events (Author: Shravya Matta)
# - November 10, 2024: Group modified to ensure event button clicks open the edit modal (Author whole group)
# - November 20, 2024: Implemented recurrence and fixed some bugs (Magaly Camacho)
# - December 7, 2024: Implemented variables for ease of UI modification (Matthew McManness)
# - December 8, 2024: Theme toggling (Magaly Camacho)
#
# Preconditions:
# - Kivy framework must be installed and configured properly.
# - The `DatePicker` and `RepeatOptionsModal` must be accessible within screens/usefulwidgets.
#
# Postconditions:
# - This modal allows updating or deleting events and modifies the Event ListView.
#
# Error Handling:
# - If the event title is missing, the event will not be saved, and an error message will be printed.
#
# Side Effects:
# - Updates the event list and modifies the Event ListView when events are saved or deleted.
#
# Known Faults:
# - None
# -----------------------------------------------------------------------------

# Import necessary Kivy modules and custom widgets
from kivy.uix.modalview import ModalView  # Modal for event editing
from kivy.uix.boxlayout import BoxLayout  # Layout for organizing widgets
from kivy.uix.textinput import TextInput  # Input fields for user text
from kivy.uix.button import Button  # Standard button widget
from kivy.uix.label import Label  # Label widget for displaying text
from Models import Event_, Recurrence  # Event class
from Models.databaseEnums import Frequency  # For event frequency
from database import get_database  # To connect to the database
from sqlalchemy import select  # To query the database
from sqlalchemy.orm import Session  # for typing
from datetime import datetime  # For event date and time
from screens.usefulwidgets import DatePicker, RepeatOptionsModal  # Additional modals
from kivy.metrics import dp  # For consistent spacing and sizing
from kivy.app import App  # Access the app instance for global styles
from kivy.graphics import Color, RoundedRectangle  # For rounded rectangle shape


class UniformButton(Button):
    pass

db = get_database(debug=True)  # Get the database connection


class EditEventModal(ModalView):
    def __init__(self, event_id=None, refresh_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.event_id = event_id  # Store the event ID for loading
        self.size_hint = (0.95, 0.5)
        self.auto_dismiss = False
        self.refresh_callback = refresh_callback  # Store the refresh callback

        # Access app-wide styles
        app = App.get_running_app()

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

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


        # Title input for event name
        self.title_input = TextInput(
            hint_text="Event Title",
            multiline=False,
            font_size=app.button_font_size,
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(5)]
        )
        layout.add_widget(self.title_input)

        # Date and time section
        date_layout = BoxLayout(orientation='horizontal', spacing=dp(10))
        self.event_date_label = Label(
            text="Pick Event Date & Time",
            font_size=app.button_font_size,
            color=app.Text_Color,
        )
        date_layout.add_widget(self.event_date_label)
        pick_date_button = UniformButton(
            text="Pick Date & Time",
            on_release=self.open_date_picker
        )
        date_layout.add_widget(pick_date_button)
        layout.add_widget(date_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = UniformButton(
            text=Frequency.frequency_options()[0],
            on_release=self.open_repeat_window
        )
        layout.add_widget(self.repeat_button)

        # Notes input for event description
        self.notes_input = TextInput(
            hint_text="Notes",
            multiline=True,
            font_size=app.button_font_size,
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(5)]
        )
        layout.add_widget(self.notes_input)

        # Action buttons (Save, Delete, Cancel)
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        cancel_button = UniformButton(
            text="CANCEL",
            on_release=self.cancel_and_close
        )
        delete_button = UniformButton(
            text="DELETE",
            on_release=self.delete_event
        )
        save_button = UniformButton(
            text="SAVE",
            on_release=self.save_event
        )
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(delete_button)
        button_layout.add_widget(save_button)
        layout.add_widget(button_layout)

        self.add_widget(layout)

        if event_id:
            self.load_event(event_id)

    def load_event(self, event_id):
        """Load event data into fields for editing."""
        with db.get_session() as session, session.begin():
            event = session.query(Event_).filter_by(id=event_id).first()
            if event:
                # Populate the title and notes fields
                self.title_input.text = event.name
                self.notes_input.text = event.notes
                # Format and display the event start time
                self.event_date_label.text = f"Event Date: {event.start_time.strftime('%Y-%m-%d %H:%M')}" if event.start_time else "Pick a date & time"

                # Get recurrence info
                if event.recurrence_id:
                    recurrence: Recurrence = event.recurrence
                    self.repeat_button.text = Frequency.enum2str(recurrence.frequency)

                    if not Frequency.is_no_repeat(recurrence.frequency):
                        self.repeat_button.text += f" ({recurrence.times} times)"
    def save_event(self, *args):
        """Save the event, updating if it exists or creating a new one."""
        if not self.title_input.text:
            print("Event Title is required.")
            return

        # Collect data from the modal
        name = self.title_input.text
        notes = self.notes_input.text
        start_time = (" ").join(self.event_date_label.text.split(" ")[2:]) if "Event Date:" in self.event_date_label.text else None # remove "Event Date:"
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M") if start_time else None
        repeat_info = self.repeat_button.text.split(" ")
        frequency = None if len(repeat_info) == 2 else Frequency.str2enum(repeat_info[1]) # None if "Doesn't Repeat"
        times = None if len(repeat_info) == 2 else int(repeat_info[2]) # None if "Doesn't repeat"

        with db.get_session() as session, session.begin():
            if self.event_id:
                event = session.scalar(select(Event_).where(Event_.id == self.event_id)) # get event from database
                # Update existing event
                if event:
                    event.name = name
                    event.notes = notes
                    event.start_time = start_time

                    make_new_recurrence = False # assume new recurrence isn't needed

                    # New recurrence might be needed if times and frequency was given
                    if times and frequency:
                        # if event has recurrence, new recurrence is need if it doesn't match existing one
                        if event.recurrence_id: 
                            recurrence = event.recurrence
                            if times != recurrence.times or frequency != recurrence.frequency:
                                make_new_recurrence = True
                    
                        else: # if event doesn't have recurrence and recurrence info was given, make new recurrence
                            make_new_recurrence = True
                    
                    # Make new recurrence if needed
                    if make_new_recurrence:
                        new_recurrence_id = self.save_recurrence(frequency, times, session=session)
                        event.recurrence_id = new_recurrence_id

                        # create other events
                        current_date = start_time
                        for _ in range(times - 1):
                            new_date = frequency.get_next_date(current_date, start_time)

                            # create event with same info as edited event
                            event_i = Event_(
                                name=name,
                                notes=notes,
                                start_time=new_date,
                                recurrence_id=new_recurrence_id
                            )
                            print(event_i)

                            current_date = new_date # save date to calculate next one
                            session.add(event_i)

                else:
                    print(f"No event found with ID {self.event_id}.")
            else:
                # Create a new event only if no event_id was provided
                event = Event_(name=name, notes=notes, start_time=start_time)
                session.add(event)
                session.commit()

        # Refresh the calendar after saving if callback is provided
        if self.refresh_callback:
            print("Refreshing")
            self.refresh_callback()

        self.cancel_and_close()

    def delete_event(self, *args):
        """Delete the event from the database."""
        if self.event_id:
            with db.get_session() as session, session.begin():
                event = session.query(Event_).filter_by(id=self.event_id).first()
                if event:
                    session.delete(event)
            print(f"Event with ID {self.event_id} deleted.")

            # Call the refresh callback to update the event list after deletion
            if self.refresh_callback:
                self.refresh_callback()

            self.cancel_and_close()

    def open_date_picker(self, instance):
        """Open the DatePicker modal to select a date and time."""
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        RepeatOptionsModal(self).open()

    def save_recurrence(self, frequency:Frequency, times:int, session:Session) -> int:
        """
        Adds the given recurrence to the given session and returns its id
        
        Parameters:
            frequency (Frequency): the frequency of the recurrence (daily, weekly, monthly, yearly)
            times (int): the number of times to repeat the event 
            session (Session): the session to add the recurrence to

        Returns:
            int: the id of the new recurrence
        """
        recurrence = Recurrence(times=times, frequency=frequency)
        session.add(recurrence) 
        session.flush() # assigns id without needing to commiting (in case of a rollback)
        
        return recurrence.id
    
    def update_background(self, *args):
        """Update the size and position of the background rectangle."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def cancel_and_close(self, *args):
        """Close the modal and reset the modal_open flag in CalendarView."""

        # Dismiss the modal
        self.dismiss()