from UserInterface.ConsoleUI import UserInterface
from UserInterface.GUI import *

def get_settings_user_interface_value():
    file_settings = open("settings.properties", "r")
    lines = file_settings.readlines()
    first_line = lines[0].strip(' ').split()
    value = first_line[2].strip('"')
    return value

if get_settings_user_interface_value() == "UI":
    program = UserInterface()
    program.run_game()

elif get_settings_user_interface_value() == "GUI":
    program = GraphicalUI()
    program.run_menu()