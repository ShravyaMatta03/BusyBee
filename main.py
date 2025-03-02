# -----------------------------------------------------------------------------
# Name: main.py
# Description: Entry point of the BusyBee application. 
#              This script initializes and runs the Kivy application.
# Programmer: Matthew McManness (2210261)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created. (Author: Matthew McManness)
# - October 27, 2024: Final version completed (including comments)
# 
# Preconditions:
# - The BusyBeeApp class must be correctly defined and imported from busybee.py.
# - Kivy must be installed and accessible via the Python environment.
# 
# Acceptable Input:
# - No direct input is required for this script.
# 
# Unacceptable Input:
# - Attempting to execute without Kivy or without the correct directory setup will result in errors.
#
# Postconditions:
# - If the application initializes successfully, the BusyBee app will run in a window.
#
# Return Values:
# - None. This script executes the BusyBee app and keeps it running until terminated.
#
# Error and Exception Conditions:
# - ImportError: Raised if BusyBeeApp cannot be imported.
# - SystemError: Raised if the Python path is not correctly set.
# 
# Side Effects:
# - Adds the project directory to the system's Python path for module imports.
#
# Invariants:
# - Kivy must remain installed for the application to work properly.
# 
# Known Faults:
# - None identified at the time of writing.
#
# -----------------------------------------------------------------------------

# Import necessary modules
from kivy.app import App  # Kivy's base class for applications
import sys  # System-specific parameters and functions
import os  # Miscellaneous operating system interfaces


# Add the project directory to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busybee import BusyBeeApp  # Import the BusyBeeApp class from busybee.py

# -----------------------------------------------------------------------------
# Main Entry Point:
# This block ensures that the application runs only when the script is executed 
# directly (i.e., not when imported as a module).
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    BusyBeeApp().run()  # Run the BusyBee application
