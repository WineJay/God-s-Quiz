import csv
import random

# retrieve the CSV file to put into a list

file= open("gods_name_power_lists.csv", "r")
all_gods = list(csv.reader(file, delimiter=","))
file.close()

# print("all gods", all_gods)


round_power = []
round_gods_names = []

#loop until we have 4 different powers
while len(round_power) < 4:
    potential_power = random.choice(all_gods)
    print(potential_power)

    # get the correct power of the god and no duplicates
    if potential_power[3] not in round_gods_names:
        print("potential power 1", potential_power[3])
        round_power.append(potential_power)

        round_gods_names.append(potential_power[3])


print(round_power)
print(round_gods_names)




# print("gods names", round_gods_names)
# print("round power", round_power)

