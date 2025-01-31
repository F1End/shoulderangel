"""
"Do this not, and thus you shall be better... - says the Angel"
Creating an effect that is clearly visible to the user
"""
import tkinter as tk
from tkinter import messagebox

from time import sleep

# Abstracting into class for upcoming alarm types and easier expansion for different systems
class Alarm:
    def __init__(self, cleanup=True):
        self.cleanup = cleanup

    def pop_msg(self, title, msg, move_to_top: bool = False):
        display = tk.Tk()
        display.withdraw()
        messagebox.showinfo(title, msg)
        if move_to_top:
            display.wm_attributes('-topmost', True)
        if self.cleanup:
            display.destroy()

    def nudge(self, program: list, start_time, end_time):
        title = "A nudge from your shoulder :)"
        program_str = ", ".join(program)
        msg = f"""Hey my friend!\nI see you are using {program_str}.""" + \
              f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
              f"""Are you sure this is the best use of your time?"""
        self.pop_msg(title, msg, move_to_top=True)
