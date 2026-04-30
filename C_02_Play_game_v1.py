from sysconfig import get_path_names
from tkinter import *
from functools import partial # To prevent unwanted windows
import random
import csv

def get_powers():
    """
    Retrieves the powers name from the CSV file and returns to us with a list of power where each item has a power name
    linked
    to a god.
    """
    # retrieve the CSV file
    file = open("gods(Data).csv" ,"r")
    all_power_names = list(csv.reader(file, delimiter=","))
    file.close()

    all_power_names.pop(0)

    return all_power_names

def get_rounds_power():
    """
    Choose four different power from the list
    """
    all_power_names_list = get_powers()

    round_power = []
    gods_name = []
    #loop until we have 4 different gods
    while len(round_power) < 4:
        potential_power = random.choice(all_power_names_list)

        # check if the power is for the correct god
        if potential_power[1] not in gods_name:
            round_power.append(potential_power)

    return round_power

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

        # strings for labels
        intro_string = ("In each round you will be invited to choose a power. Your goal is "
                        "to beat the success-rate of 60% out of a 100%")

        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Guess the God", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#FFFFFF"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=[1],
                               fg=item[2], wraplength=350, justify="left", pady=10, padx=20, bg="#FFDBBB")
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed into an error message when necessary.
        self.choose_label = start_label_ref[2]

        # frame so that entry box and bottom can be in same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"), width=10, )
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button...

        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#009900", text="Play", width=10,
                                      command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=10, pady=10)

    def check_rounds(self):
        # Retrieve Temperature to be converted.
        rounds_asked = self.num_rounds_entry.get()

        #reset label and entry box ( for when user comes back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config()

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        #checks that amount to be converted is a number above absolute zero
        try:
            rounds_asked = int(rounds_asked)
            if rounds_asked > 0:
                Play(rounds_asked)

                root.withdraw()


            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", 10, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


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

        # body font for the labels
        body_font = ("Arial", 12)
        # List of label details (text|font|bg|row)
        play_label_list = [

            ["Name of the God: #", ("Arial", 16, "bold"), "#ffe6cc", 1],
            ["Choose a power below", body_font, "#D5E8D4", 2],
            ["You chose , result", body_font, "#D5E8D4", 4]
        ]


        self.end_game_button = Button(self.game_frame, text="End Game", font=("Arial", 16, "bold"),
                                        fg="#FFFFFF", bg= "#990000", width=10, command=self.close_play)
        self.end_game_button.grid(row=5)
    def close_play(self):
        # shows the root and end current
        root.deiconify()
        # allows new game to start
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guess the God")
    StartGame()
    root.mainloop()