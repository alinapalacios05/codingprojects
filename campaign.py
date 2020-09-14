"""
Campign Lab
Alina Palacios
November 19 2019
"""

from electiondata import *

#_cand = "/usr/local/doc/2020all.txt"


def main():
    donor_info = []
    choice = 0
    while choice != "0":
        print("Please select one of the following choices: ")
        print("0. Quit")
        print("1. Load file")
        print("2. Print top donations")
        print("3. Filter by campaign ID")
        print("4. Filter by state")
        print("5. Filter by city")


        choice = input("Choice?: ")

        if choice == "1":
            donor_info = load_file(donor_info)
            print("Number of current records: " , len(donor_info))
        elif choice == "2":
            top_donations(donor_info)
            print("Number of current records: " , len(donor_info))
        elif choice == "3":
            donor_info = campaign_ID(donor_info)
            print("Number of current records: " , len(donor_info))
        elif choice == "4":
            donor_info = filter_state(donor_info)
            print("Number of current records: " , len(donor_info))
        elif choice == "5":
            donor_info = filter_city(donor_info)
            print("Number of current records: " , len(donor_info))
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please enter valid choice. ")
       
       def read_input(filename):
    """
    This function loads the data from the donor_info file and puts into a
    list of lists.
    """
    donor_info = []
    f = open(filename, 'r')
    for line in f:
        info = line.strip().split("|")
        d = Donation(info[0],info[1],info[2],info[3],
        int(info[4]), int(info[5]),  int(info[6]),  int(info[7]))
        donor_info.append(d)
    f.close()

    return donor_info

def load_file(donor_info):
    """
    This helper function is responible for asking the user to select one of the
    valid filenames in the submenu. It returns a new list of donation records and
    prints the number of records returned.
    """
    print("Data files: ")

    print("1. Grouped by candidates (2020candidates.txt)")
    print("2. Grouped by month (2020months.txt)")
    print("3. Grouped by state (2020states.txt)")
    print("4. Grouped by donor (2020donors.txt)")
    print("5. All records (2020all.txt)")

    file_choice = input("Your choice?: ")

    #while file_choice != 0:
    print("Data files: ")

    if file_choice == "1":
        lst = read_input("/usr/local/doc/2020candidates.txt")
        file_choice1 = len(lst)
    elif file_choice == "2":
        lst = read_input("/usr/local/doc/2020months.txt")
        file_choice1 = len(lst)
    elif file_choice == "3":
        lst = read_input("/usr/local/doc/2020states.txt")
        file_choice1 = len(lst)
        #donor_info = campaign_ID(donor_info)
        #print(donor_info)
    elif file_choice == "4":
        lst = read_input("/usr/local/doc/2020donors.txt")
        file_choice1 = len(lst)
    elif file_choice == "5":
        lst = read_input("/usr/local/doc/2020all.txt")
        file_choice1 = len(lst)

    return lst

def top_donations(donor_info):
    """
    This helper function is called when the user inputs "2" to view the top donations
    and print the n number of top donations in decreasing order with the highest
    amount first. The function compares the first and second element to see which one
    is greater. If the second element is greater than the first, this function swaps the
    elements until the list is from greatest to least. 
    """

    keepGoing = True

    while keepGoing == True:
        keepGoing = False
        for i in range(len(donor_info)-1):
          if donor_info[i].get_amt() < donor_info[i+1].get_amt():
              swap(donor_info, i, i+1)
              keepGoing = True

    n_donations = int(input("How many?: "))

    for i in range(n_donations):
       cand = get_candidates()
       for j in range (len(cand)):
           if donor_info[i].get_candidate() == cand[j].get_candidate_id():
              print(cand[j].get_name() + ": ", (donor_info[i].get_amt()))
              print(donor_info[i])
              print(" ")

def swap(donor_info, i, j):
    """
    Swap serves as the foundation for sorting the donor_info masterlist in the
    top_donations helper function.
    """
    temp = donor_info[i]
    donor_info[i] = donor_info[j]
    donor_info[j] = temp

def campaign_ID(donor_info):
    candidate_id = get_candidates()
    id = get_candidates()
    choice_ID = input("Please enter a campaign ID: ")

    filter_campaign_lst = []

    for i in range (len(donor_info)):
        if donor_info[i].get_candidate() == choice_ID:
            filter_campaign_lst.append(donor_info[i])
    return filter_campaign_lst

def filter_state(donor_info):
    """
    This helper function filters the state of the file that the user chose to load
    beforehand. user_city prompts the user to type in a state and attached to the
    input it has upper(), which turns the input string into all uppercase letters.
    There is an empty list that get filled with the filtered content from the file
    that the user chose to load.
    """

    user_state = input("State?: ").upper()

    filter_state_lst = []

    #matches = 0
    for i in range (len(donor_info)):
        if donor_info[i].get_state() == user_state:
            filter_state_lst.append(donor_info[i])
    return filter_state_lst

def filter_city(donor_info):
    """
    This helper function filters the city of the file that the user chose to load
    beforehand. user_city prompts the user to type in a city and attached to the
    input it has upper(), which turns the input string into all uppercase letters.
    """
    user_city = input("City?: ").upper()
    #user_city.isupper()

    filter_city_lst = []

    for i in range (len(donor_info)):
        if donor_info[i].get_city() == user_city:
            filter_city_lst.append(donor_info[i])
    return filter_city_lst

def exit_program():
    """
    This function is used for the user to exit the program. When they input "0"
    in the main menu, this function will return True, satisfying the condition in
    main and exit the program.
    """
    print("Closing program...")
    return True


main()
