"""
"Do this not, and thus you shall be better... - says the Angel"
Creating an effect that is clearly visible to the user
"""
import ctypes


# Abstracting into class for upcoming alarm types and easier expansion for different systems
class Alarm:
    def __init__(self):
        pass

    @staticmethod
    def nudge(program: list, start_time, end_time):
        title = "A nudge from your shoulder :)"
        program_str = ", ".join(program)
        msg = f"""Hey my friend!\nI see you are using {program_str}.""" + \
              f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
              f"""Are you sure this is the best use of your time?"""
        ctypes.windll.user32.MessageBoxW(0, msg, title, 0)
