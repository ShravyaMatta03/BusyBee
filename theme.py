# Name: themes.py
# Description: Light mode and dark mode settings
# Programmer: Magaly Camacho (3072618)
# Date Created: December 7, 2024
# Revision History:
# - December 7, 2024: Initial version created (Author: Magaly Camacho)
# - December 8, 2024: Enhanced theme settings (Magaly Camacho)

from enum import Enum
from kivy.utils import get_color_from_hex

class Theme(Enum):
    LIGHT = 0
    DARK = 1
    
    @staticmethod
    def toggle(theme):
        if theme == Theme.LIGHT:
            return Theme.DARK
        
        return Theme.LIGHT
    
    def get_settings(self) -> dict:
        return THEME_SETTINGS[self.value]

WHITE = "#FFFFFF"
GREY_LIGHT = "#BABABA"
GREY_MEDIUM = "#858585"
GREY_DARK = "#5D5D5D"
GREY_DARKER = "#353535"
BLACK = "#000000"

DARK_GREEN = "#106F10"
DARK_ORANGE = "#AB7112"
DARK_RED ="#720B0B"
LIGHT_GREEN = "#1ACF1A"
LIGHT_ORANGE = "#F69F11"
LIGHT_RED ="#D51818"

ALMOST_BLACK_BLUE = "#051016"
DARKER_BLUE = "#0A1F2B"
DARK_BLUE = "#0F2F41"
MED_DARK_BLUE = "#226D98"
BASE_BLUE = "#90C6E6"
LIGHT_BLUE = "#CFE6F4"
ALMOST_WHITE_BLUE = "#F7FBFD"

LIGHT_MODE = {
    "Title_Color": get_color_from_hex(ALMOST_WHITE_BLUE),
    "Title_Background": get_color_from_hex(DARK_BLUE),

    "Subtitle_Color": get_color_from_hex(MED_DARK_BLUE),
    "Background_Color": get_color_from_hex(LIGHT_BLUE), 

    "Text_Color": get_color_from_hex(ALMOST_BLACK_BLUE), 
    "Checkbox_Color": get_color_from_hex(ALMOST_BLACK_BLUE),

    "Button_Color": get_color_from_hex(MED_DARK_BLUE),
    "Button_Text": get_color_from_hex(WHITE),

    "Task_Box": get_color_from_hex(ALMOST_WHITE_BLUE),
    "Event_Box": get_color_from_hex(ALMOST_WHITE_BLUE),
    "Event_Button": get_color_from_hex(BASE_BLUE),
    "Event_Button_Text": get_color_from_hex(WHITE),
    "Event_More_Label": get_color_from_hex(GREY_MEDIUM),
    "Box_Greyed_Out": get_color_from_hex(GREY_LIGHT),
    "Box_Greyed_Out_Text": get_color_from_hex(GREY_DARK),

    "Date_Selected": get_color_from_hex(BASE_BLUE),
    "Date_Selected_Text": get_color_from_hex(ALMOST_WHITE_BLUE),

    "Edit_Button_Color": get_color_from_hex(BASE_BLUE),
    "Edit_Button_Text": get_color_from_hex(WHITE),

    "Weekday_Background": get_color_from_hex(MED_DARK_BLUE), 
    "Weekday_Color": get_color_from_hex(WHITE),

    "Priorities": {
        "Low": get_color_from_hex(DARK_GREEN),
        "Medium": get_color_from_hex(DARK_ORANGE),
        "High": get_color_from_hex(DARK_RED)
    }
}

DARK_MODE = {
    "Title_Color": get_color_from_hex(ALMOST_WHITE_BLUE),
    "Title_Background": get_color_from_hex(MED_DARK_BLUE),

    "Subtitle_Color": get_color_from_hex(BASE_BLUE),
    "Background_Color": get_color_from_hex(ALMOST_BLACK_BLUE), 

    "Text_Color": get_color_from_hex(ALMOST_WHITE_BLUE), 
    "Checkbox_Color": get_color_from_hex(ALMOST_WHITE_BLUE),

    "Button_Color": get_color_from_hex(BASE_BLUE),
    "Button_Text": get_color_from_hex(WHITE),

    "Task_Box": get_color_from_hex(DARK_BLUE), 
    "Event_Box": get_color_from_hex(DARK_BLUE), 
    "Event_Button": get_color_from_hex(LIGHT_BLUE),
    "Event_Button_Text": get_color_from_hex(ALMOST_BLACK_BLUE),
    "Event_More_Label": get_color_from_hex(GREY_LIGHT),
    "Box_Greyed_Out": get_color_from_hex(GREY_DARKER),
    "Box_Greyed_Out_Text": get_color_from_hex(GREY_LIGHT),

    "Date_Selected": get_color_from_hex(LIGHT_BLUE),
    "Date_Selected_Text": get_color_from_hex(ALMOST_BLACK_BLUE),

    "Edit_Button_Color": get_color_from_hex(BASE_BLUE),
    "Edit_Button_Text": get_color_from_hex(WHITE),

    "Weekday_Background": get_color_from_hex(BASE_BLUE), 
    "Weekday_Color": get_color_from_hex(WHITE),

    "Priorities": {
        "Low": get_color_from_hex(LIGHT_GREEN),
        "Medium": get_color_from_hex(LIGHT_ORANGE),
        "High": get_color_from_hex(LIGHT_RED)
    }
}

THEME_SETTINGS = [LIGHT_MODE, DARK_MODE]