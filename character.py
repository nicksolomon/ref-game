import random
import room
# import os
from text import *
# from IPython.display import clear_output as clear

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Character:
    def __init__(self, name, room, world):
        self.name = name
        self.room = room
        world.addCharacter(self)
        world.register(self)

    def update(self):
        None

    def talk(self, player):
        clear()
        print(underline("What does " + self.name + " have to say?"))
        responses = ["Be quite! I'm trying to get some work done!", "The kiosks will tell you if there's a book you need near you.", "I've been lost in here for three days! Do you know how to get out?!?", "Watch out for some of the other people around here. They'll give you stuff, but talking to them is exhausting."]
        print(random.choice(responses))
        input("Press enter to continue...")




def rand_char():
    all_chars = [Character]
    return random.choice(all_chars)