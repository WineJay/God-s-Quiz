from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random
from tabulate import tabulate
from datetime import date


def get_powers():
    """
    Retrieves the powers name from the CSV file and returns to us with a list of power where each item has a power name
    linked
    to a god.
    """
    # retrieve the CSV file

    file = open("gods_name_power_lists.csv", "r")
    all_gods = list(csv.reader(file, delimiter=","))
    file.close()

    return all_gods


def get_round_power():
    """
    Choose four different power from the list
    """
    all_gods_list = get_powers()

    round_power = []
    gods_name = []
    origin = []
    type = []
    # loop until we have 4 different gods
    while len(round_power) < min(4, len(all_gods_list)):
        potential_power = random.choice(all_gods_list)

        # check if the power is for the correct god
        if potential_power not in gods_name:
            round_power.append(potential_power)
            gods_name.append(potential_power[2])
            origin.append(potential_power[0])
            type.append(potential_power[1])

    print("round power", round_power)
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
            [choose_string, ("Arial", 12, "bold"), "#474747"]
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

        # enters the number of rounds the user will play
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"), width=10, )
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button...

        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#006600", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=10, pady=10)

    def check_rounds(self):
    # checks the amount of rounds the user is going to play so that we won't play a random number of rounds or infinite.
        round_asked = self.num_rounds_entry.get()

        # reset label and entry box ( for when user comes back to home screen)
        self.choose_label.config(fg="#006600", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config(bg="#90EE90")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            round_asked = int(round_asked)
            if round_asked > 0:
                Play(round_asked)
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
        # retrieves the number of rounds the user had asked for
        self.round_asked = IntVar(value=_amount_)
        # finds the number of rounds the user played
        self.round_played = IntVar()
        self.round_played.set(0)
        # calculates the number of rounds the user has won while playing the rounds
        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # finds the list where the real god and power is
        self.all_real_gods_list = []

        # these for the play class or the quiz page
        self.round_power_list = ()
        self.target_god = ()
        self.target_power= ()
        self.origin=()
        self.type = ()
        self.rounds_requested = IntVar()
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box, bg="#ffe6cc")
        self.game_frame.grid(padx=10, pady=10)

        #this is for the quiz page where the game starts from 1 and continues to the round the user has asked for
        self.game_heading_label = Label(self.game_frame, text=f"Round 1 of {_amount_}", font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        # body font for the labels
        body_font = ("Arial", 12)
        # List of label details (text|font|bg|row)
        play_label_list = [

            ["", ("Arial", 16, "bold"), "#ffe6cc", 1],
            ["", ("Arial", 16, "bold"), "#ffe6cc", 2],
            ["", ("Arial", 16, "bold"), "#ffe6cc", 3],
            ["Choose a power below", body_font, "#D5E8D4", 4],
            ["You chose , result", body_font, "#ffe6cc", 6]
        ]

        # this is where the Labels are referenced and sorted into their rows through their order.
        play_label_ref = []
        for item in play_label_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10, sticky="w")

            play_label_ref.append(self.make_label)

        # retrieving the labels
        self.name_label = play_label_ref[0]
        self.gods_origin = play_label_ref[1]
        self.type_of_god = play_label_ref[2]
        self.chosen_label = play_label_ref[3]
        self.results_label = play_label_ref[4]

        # powers for the buttons
        self.power_frame = Frame(self.game_frame, bg="#ffe6cc")
        self.power_frame.grid(row=5)

        # set up the power buttons
        self.power_button_ref = []
        self.power_button_list = []

        # create 4 buttons in a 2 x 2 grid to choose the powers
        for item in range(0, 4):
            self.power_button = Button(self.power_frame, font=("Arial", 12), text="Power",width=15,wraplength=140,
                                       bg="#008cff", command=partial(self.round_result, item))
            self.power_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.power_button_ref.append(self.power_button)

            # retrieve next round button
        self.next_round_button = Button(self.game_frame, text= "Next Round", font=("Arial", 16, "bold"),
                                        fg="#ffffff", bg="#0057D8",width=21, command=self.next_round)
        self.next_round_button.grid(row=7, pady=5)
        # the stats Button
        self.stats_button = Button(self.game_frame, text="Progress", font=("Arial", 16, "bold"),
                                   fg="#ffffff", bg="#FCE27E", width=21, command=self.to_stats)
        self.stats_button.grid(row=8, pady=5)
        # the Hints button
        self.hints_button = Button(self.game_frame, font=("Arial", 16, "bold"), text="Hints", width=21, fg="#FFFFFF",
                                   bg="#005C5C", command=self.to_hints)
        self.hints_button.grid(row=9, pady=5)
        # the End game button
        self.end_game_button = Button(self.game_frame, text="End Game", font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#990000", width=21, command=self.close_play)

        self.end_game_button.grid(row=10, pady=5)

        # continues when there is more rounds and there a history to add at the stats function where the correct and incorrect is shown
        self.next_round()
        self.round_history_list = []
    def next_round(self):
        """
        chooses another 4 lists where a different god along with 4 different powers are retrieved. (some power may seem
        the same because there are many duplicates but there is no more than 2 duplicates, and sometimes they are not the
        right answer)
        """
        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.round_played.get()
        rounds_requested = self.round_asked.get()

        self.round_power_list = get_round_power()
        # picks a god from the 4 sets it retreives and then picks a random 1 out of 4
        real_god = random.choice(self.round_power_list)
        print("random string out of the 4", real_god)
        gods_origin = real_god[0]
        print("gods origin", gods_origin)
        type_of_god = real_god[1]
        print("gods type", type_of_god)

        # since my gods name is in index 2 and power in 3
        self.target_god = real_god[2]
        self.target_power = real_god[3]

        self.game_heading_label.config(text=f"Round {rounds_played +1} of {rounds_requested} ")
        self.name_label.config(text=f"Name of God: {self.target_god}")
        self.gods_origin.config(text=f"Origin: {gods_origin}")
        self.type_of_god.config(text=f"Type: {type_of_god}")
        self.results_label.config(text="", bg="#ffe6cc", justify="center")

        self.button_lookup = {}

        for count, item in enumerate(self.power_button_ref):
            print("button text?", self.round_power_list[count][3])
            pwr_button_text = self.round_power_list[count][3]
            item.config(text=pwr_button_text, state=NORMAL, bg="#008cff")
            self.button_lookup[pwr_button_text] = item
        self.next_round_button.config(state=DISABLED)


    def close_play(self):
        # shows the root and end current
        root.deiconify()
        # allows new game to start
        self.play_box.destroy()


    def round_result(self, user_choice):
        """
        retrieves which power button was pressed
        """
        # finds the real answer to the quiz for user's choice
        real_god = self.target_god
        real_power = self.target_power

        # find the number of rounds the user asked for and the rounds user had won.
        rounds_requested = self.round_asked.get()
        rounds_won = self.rounds_won.get()

        # alternate way to get button name. good for buttons have been scrambled
        power_name = self.power_button_ref[user_choice].cget('text')

        # checks if the user pressed on the correct answer for the quiz or not

        if  real_power == power_name :
            pass
            result_text = f"Success! {power_name} was the answer for {real_god}"
            result_bg = "#82B366"
            self.all_real_gods_list.append(1)
            # if the answer was correct it shows to the stats function where it is stored as correct
            self.round_history_list.append([real_god, power_name, "Correct"])

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
        else:
            result_text = f"Oops {power_name} is not the power of {real_god}."
            result_bg = "#F8CECC"
            self.all_real_gods_list.append(0)
            # if the result is incorrect it shows the stats function where it shows the answer was incorrect
            self.round_history_list.append([real_god, power_name, "Incorrect"])
        # changes the results label so that it matches the answer instead of staying as default all time.
        self.results_label.config(text=result_text, bg=result_bg, wraplength=200)

        # for the buttons to go red for incorrcect and green for correct
        for button in self.power_button_ref:
            button.config(state=DISABLED, disabledforeground="#000000")

        self.button_lookup[real_power].config(bg = "#82B366")

        if power_name != real_power:
            self.power_button_ref[user_choice].config(bg="#F8CECC")

        # enables stats & next button, disable power buttons
        self.next_round_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # # checks to see if game is over

        rounds_played = self.round_played.get()
        rounds_played += 1
        self.round_played.set(rounds_played)
        print("played rounds", rounds_played)
        #rounds_wanted = self.rounds_requested.get()

        # code for when the rounds end
        if rounds_played == rounds_requested:
            # CONFIGURE 'END GAME' labels / buttons
            self.game_heading_label.config(text="Game Over")
            self.chosen_label.config(text="Please click the stats button for more info.")
            self.next_round_button.config(state=DISABLED, text="Game Over")
            self.stats_button.config(bg="#990000")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.power_button_ref:
            item.config(state=DISABLED)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics"""

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_real_gods_list, self.round_history_list]

        Stats(self, stats_bundle)

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
                                         justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.close_button = Button(self.help_frame,
                                         font=("Arial", 12, "bold"),
                                         text="Close", bg="#CC6600",
                                         fg="#FFFFFF",
                                         command=partial(self.close_hints,partner))
        self.close_button.grid(row=3, padx=10, pady=10)

        # closes help dialogue (used by button and x at top of dialogue)

    def close_hints(self, partner):
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()

class Stats:

    """
    Displays stats for Colour Quest Game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        rounds_won = all_stats_info[0]
        user_played = all_stats_info[1]
        # for tabulate to show
        round_history = all_stats_info[2]

        self.round_history = round_history

        # sort user real_gods to find high real_god...
        user_played.sort()
        self.stats_box = Toplevel()
        self.stats_box.title("Guess the God's Power")

        # disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))


        self.stats_frame = Frame(self.stats_box, width=350, bg="#ffe6cc", pady=20, padx=25)
        self.stats_frame.grid()

        # Math to populate Stats dialogue...
        rounds_played = len(user_played)
        rounds_requested = partner.rounds_requested.get()
        success_rate = (rounds_won / rounds_played * 100) if rounds_played > 0  else 0
        total_real_god = rounds_won

        # Strings for Stats labels...

        self.stats_title = Label(self.stats_frame, text="Your Progress along the way",
                                 bg="#ffffff", fg="#000000", justify="center", anchor="w")
        self.stats_title.grid(row=0, pady=(0,15))

        success_string = (f"Success Rate: {rounds_won} / {rounds_played} ({success_rate:.0f}%)")

        total_real_god_string =(f"You have got right {total_real_god} answers right!")


        all_stats_string = [
            success_string,
            total_real_god_string
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_string):
            self.stats_label = Label(self.stats_frame, text=item, font=("Arial", 16), wraplength=300,
                                     anchor="w", justify="left",padx=30, pady=5, bg="#ffe6cc")
            self.stats_label.grid(row=count +1, sticky="W", padx=10)
            stats_label_ref_list.append(self.stats_label)
        # folowing codes for the tabulate table
        headers = ["God", "User Choice", "Correct / incorrect"]
        # format for tabulate's grid
        table_string = tabulate(round_history, headers, tablefmt="fancy_grid", maxcolwidths=[15,15,12])

        self.table_label = Label(self.stats_frame, text=table_string, font=("Consolas" , 10), justify="left", anchor="w",
                                 bg="#ffffff", fg="#000000", bd=1, padx=10, pady=10)
        self.table_label.grid(row=3)


        if success_rate <59:
            self.stats_statement = Label(self.stats_frame, text="You didn't win 😥 Please try again!",
                                         font=("Arial", 12, "bold"), bg="#D91A1A", fg="#ffffff", justify="center",
                                            width=32, pady=10)
            self.stats_statement.grid(row=4, sticky="EW" ,padx=5, pady=5)


        else:
            self.stats_statement = Label(self.stats_frame, text="You did it! 😊", font=("Arial", 12, "bold"), bg="#82B366",)
            self.stats_statement.grid(row=4, sticky="EW", padx=5, pady=5)


        self.export_button = Button(self.stats_frame, font=("Arial", 16, "bold"), text="Export",
                                    bg="#004C99", fg="#ffffff", width=20, command=partial(self.export_results))
        self.export_button.grid(row=5, padx=5, pady=5)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=6, padx=10, pady=10)

        # closes help dialogue (used by button and x at top of dialogue)

    def export_results(self):
        # **** Get current date for heading and filename ***
        today = date.today()

        # get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"Gods_quiz_{year}_{month}_{day}"

        headers = ["God's Name", "User Choice", "Correct / Incorrect"]
        table_string = tabulate(self.round_history, headers=headers, tablefmt="fancy_grid", maxcolwidths=[15,15,12])

        with open(file_name, "w", encoding="utf-8") as text_file:
            text_file.write("***** Guess the God's Power *****\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")

            text_file.write("Here is the results of each rounds you played...\n")
            text_file.write(table_string)
            text_file.write("\n\nThanks for playing this rounds!")

        success_string = f"Export was Successful! File Name: {file_name}"
        self.stats_statement.config(text=success_string, bg="#009900", fg="#ffffff", width=32, wraplength=300)
        self.export_button.config(state=DISABLED,text="Exported!")

    def close_stats(self, partner):
        # Put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()
# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Guess the God")
    StartGame()
    root.mainloop()