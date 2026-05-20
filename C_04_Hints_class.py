from tkinter import *
from functools import partial # To prevent unwanted windows

class StartGame:
    """
    Initial game interface (asks users how many rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """
        self.start_frame = Frame(padx=10, pady=10, bg="#FFDBBB")
        self.start_frame.grid()

        self.play_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#009900", text="Play", width=10,
                                      command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=10, pady=10)

    def check_rounds(self):
        # Retrieve Temperature to be converted.
        round_asked = 5
        self.to_play(round_asked)

    def to_play(self, num_rounds):

        Play(num_rounds)
        root.withdraw()

class Play:
    """
    Interface for playing God's Quiz
    """
    def __init__(self, _amount_):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box, bg="#ffe6cc")
        self.game_frame.grid(padx=10,pady=10)

        self.game_heading_label = Label(self.game_frame, text= f"Round 1 of {_amount_}", font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", 16, "bold"), text="Hints", width=15, fg="#FFFFFF",
                                   bg="#00FFFF", padx=10, pady=10, command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
            """this will display the text for hints functions"""
            DisplayHints(self)

class DisplayHints:
    """
    Displays hints for God's quiz Game
     """

    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_hints, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                    height=200,
                                    bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                            bg=background,
                                            text="Hints",
                                            font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("If you are struggling to find a power that is for the god  you are asked to look for, "
                     "then there a very easy way to find their power."
                     "\n\nFirst off have a look at their name and try to match it with their power. "
                     "\n\n(Eg: Flora's power is Flower)"
                     "\n\n The other way off trying to figure out their power is by looking at their Origin or their"
                     " type. The one with natural powers such as darkness, sky, sea are mostly the god's with Major"
                     " powers, while the one's with  fire, sleep, light are most likely Minor type of God." )

        self.help_text_label = Label(self.help_frame, bg=background,
                                         text=help_text, wraplength=350,
                                         justify="center")
        self.help_text_label.grid(row=1, padx=10)

        self.close_button = Button(self.help_frame,
                                         font=("Arial", 12, "bold"),
                                         text="Close", bg="#CC6600",
                                         fg="#FFFFFF",
                                         command=partial(self.close_hints,partner))
        self.close_button.grid(row=2, padx=10, pady=10)

        # closes help dialogue (used by button and x at top of dialogue)

    def close_hints(self, partner):
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()
# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guess the God")
    StartGame()
    root.mainloop()