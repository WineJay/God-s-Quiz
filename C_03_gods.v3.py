from tkinter import *
from functools import partial # To prevent unwanted windows
import csv
import random

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

    #loop until we have 4 different gods
    while len(round_power) < 4:
        potential_power = random.choice(all_gods_list)

        # check if the power is for the correct god
        if potential_power[3] not in gods_name :
            round_power.append(potential_power)

    print("round power", round_power)

    return round_power, gods_name

def get_gods_name():
    all_gods_list = get_powers()
    round_power = get_round_power()
    gods_name = []

    while len(gods_name) < 1:
        real_god = all_gods_list
        if real_god[3] not in round_power:
            gods_name.append(real_god)

    return gods_name

    print("gods name", gods_name)
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
        round_asked = self.num_rounds_entry.get()

        #reset label and entry box ( for when user comes back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config()

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        #checks that amount to be converted is a number above absolute zero
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

        self.round_asked = ()
        self.round_played = IntVar()
        self.round_played.set(0)

        self.round_power_list = ()
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box, bg="#ffe6cc")
        self.game_frame.grid(padx=10,pady=10)

        self.game_heading_label = Label(self.game_frame, text= f"Round 1 of {_amount_}", font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        # body font for the labels
        body_font = ("Arial", 12)
        # List of label details (text|font|bg|row)
        play_label_list = [

            ["Name of the God:", ("Arial", 16, "bold"), "#ffe6cc", 1],
            ["Choose a power below", body_font, "#D5E8D4", 2],
            ["You chose , result", body_font, "#D5E8D4", 4]
        ]

        play_label_ref = []
        for item in play_label_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_label_ref.append(self.make_label)

        # retrieving the labels
        self.name_label = play_label_ref[0]
        self.chosen_label = play_label_ref[2]

        # powers for the buttons
        self.power_frame = Frame(self.game_frame, bg="#ffe6cc")
        self.power_frame.grid(row=3)

        # set up the power buttons
        self.power_button_ref = []
        self.power_button_list = []

        # create 4 buttons in a 2 x 2 grid to choose the powers
        for item in range(0, 4):
            self.power_button = Button(self.power_frame, font=("Arial", 12), text="Power" ,width=15,
                                       bg="#008cff", command=partial(self.round_result, item))
            self.power_button.grid(row=item// 2, column=item % 2, padx=5, pady=5)

            self.power_button_ref.append(self.power_button)

        # control for button (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8",self.next_round ,21, 5, None],
            #[self.game_frame, "stats", "#0057D8", self.to_stats, 21, 6, None]
            [self.game_frame, "End Game", "#990000", self.close_play, 21, 7, None]
        ]

        #create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],command=item[3],
                                         font=("Arial", 16, "bold"), fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

            # retrieve next round, and end game button
            self.next_round_button = control_ref_list[0]
            self.stats_button = Button(self.game_frame, text="Stats", font=("Arial", 16, "bold"),
                                          fg="#FFFFFF", bg="#EFBF04",width=21,command=self.to_stats)
            self.stats_button.grid(row=6, pady=5)
            self.end_game_button = Button(self.game_frame, text="End Game", font=("Arial", 16, "bold"),
                                          fg="#FFFFFF", bg="#990000", width=21,command=self.close_play)
            self.end_game_button.grid(row=7,pady=5)

        self.next_round()
    def next_round(self):
        """
        Chooses four colours, works out meadian for real_god to beat. configures buttons with chosen colours
        """
        # retrieve number of rounds played, add one tp it and configure heading
        rounds_played = self.round_played.get()
        rounds_played += 1
        self.round_played.set(rounds_played)

        rounds_requested = self.round_asked
        # update heading and real_gods to beat labels. "hides" results label
        # self.game_heading_label.config(text=f"Round {rounds_played} of {rounds_requested}")
        # self.chosen_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        self.round_power_list = get_round_power()
        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round)
        for count, item in enumerate(self.power_button_ref):
            print("button text?", self.round_power_list)
            item.config(text=self.round_power_list, state=NORMAL)

        self.next_round_button.config(state=DISABLED)

    def round_result(self, user_choice):
        """
        retrieves which power button was pressed
        """
        real_god = vars(self.round_power_list[user_choice][3])

        # alternate way to get button name. good for buttons have been scrambled
        power_name = self.power_button_ref[user_choice].cget('text')

        # retrieve target real_god and compare with user real_god to find round result
        name_of_god = self.real_god.append()


        if real_god >= name_of_god:
            result_text = f"Success! {power_name} earned you {real_god} points"
            result_bg = "#82B366"
            self.all_real_gods_list.append(real_god)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
        else:
            result_text = f"Oops {power_name} is not for ({real_god})."
            result_bg = "#F8CECH"
            self.all_gods_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enables stats & next button, disable colour buttons
        self.next_round_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # # checks to see if game is over

        rounds_played = self.round_played.get()
        rounds_played += 1
        self.round_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get()

        # code for when the game ends
        if rounds_played == rounds_wanted:

            #work out the success rate
            success_rate = rounds_won / rounds_played * 100
            success_string = (f"Success Rate: "
                              f"{rounds_won} / {rounds_played} "
                              f"({success_rate:.0f}%)")

            #CONFIGURE 'END GAME' labels / buttons
            self.heading_label.config(text="Game Over")
            self.choose_label.config(text="Please click the stats button for more info.")

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
        stats_bundle = [rounds_won]

        Stats(self, stats_bundle)

    def close_play(self):
        # shows the root and end current
        root.deiconify()
        # allows new game to start
        self.play_box.destroy()
class Stats:
    """
    Displays stats for Colour Quest Game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        rounds_won = all_stats_info[0]
        user_real_gods = all_stats_info[1]
        high_real_gods = all_stats_info[2]

        # sort user real_gods to find high real_god...
        user_real_gods.sort()
        self.stats_box = Toplevel()

        # disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        # Math to populate Stats dialogue...
        rounds_played = len(user_real_gods)

        success_rate = rounds_won / rounds_played * 100
        total_real_god = sum(user_real_gods)
        max_possible = sum(high_real_gods)

        best_real_god = user_real_gods[-1]
        average_real_god = total_real_god / rounds_played

        # Strings for Stats labels...

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_real_god_string = f"Total real_god: {total_real_god}"
        max_possible_string = f"Maximum Possible real_god: {max_possible}"
        best_real_god_string = f"Best real_god: {best_real_god}"

        # comment formatting, default alignment is W (left), but if
        # we don't have a comment we want our dashes to be centered.
        comment_alignment = "W"
        if total_real_god == max_possible:
            comment_string = ("Amazing!  You got the highest "
                              "possible real_god!")
            comment_colour = "#D5E8D4"

        elif total_real_god == 0:
            comment_string = ("Oops - You've lost every round!  "
                              "You might want to look at the hints!")
            comment_colour = "#F8CECH"
            best_real_god_string = f"Best real_god: n/a"
        else:
            # comment_string = f"{' ' * 15}{'*' * 7}"
            comment_string = ""
            comment_colour = "#F0F0F0"
            comment_alignment = ""

        average_real_god_string = f"Average real_god: {average_real_god:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_real_god_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, comment_alignment],
            ["\nRound Stats", heading_font, ""],
            [best_real_god_string, normal_font, "W"],
            [average_real_god_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1], wraplength=300,
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        # closes help dialogue (used by button and x at top of dialogue)

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