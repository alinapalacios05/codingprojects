"""
Simplified Blackjack
Alina Palacios
October 2019

This program was created to simulate the game blackjack, where the user is constrained
by a limit and must play ten rounds of the game. The first two cards must be less than
or equal to the limit The variables "char" and "length" were added as a way for the
character "=" to be multipled 20 times after each round was over. 
"""

from random import*


def main():
    limit = 15
    char = str("=")
    length = int(20)
    over = 0

    for i in range(10):
        print(char*length)
        total = oneHand(limit)
        if total < 21:
            print("Game " + str(i+1) + " Final total = " + str(total))
        elif total > 21:
            over = over + 1
            print("Game " + str(i+1) + " Final total = " + str(total) + " :(")
        else:
            print("Game " + str(i+1) + " Final total = " + str(total) + " :)")


    print("For 10 games and limit=" + str(limit) + ": " + str(over) + " went over." )


def oneHand(limit):
    card_1 = randrange(1,11)
    card_2 = randrange(1,11)

    total = card_1 + card_2

    print("Card1: " + str(card_1) + ", Card2: " + str(card_2) + " -- " + "total = " + str(total))
    while total <= limit:
        nextcard = randrange(1,11)
        total = total + nextcard
        print("Next Card: " + str(nextcard) + "          " + "total: " + str(total))

    return total


main()
