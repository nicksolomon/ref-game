import random
import item
import os
from text import *
# from IPython.display import clear_output as clear

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Patron:
    def __init__(self, name, room, world, health = 100):
        self.name = name
        self.health = health
        self.room = room
        self.world = world
        world.addPatron(self)
        world.register(self)
    def update(self):
        if random.random() < .5:
            self.moveTo(random.choice(self.world.studies))
    def moveTo(self, room):
        self.room.removePatron(self)
        self.room = room
        room.addPatron(self)
    def die(self):
        self.world.deregister(self)
        self.world.removePatron(self)


class Talker(Patron):
    def talk(self, player):
        clear()
        #updater.updateAll(ticks = 2)
        player.update() #Waste some time....
        player.update()
        count = 0
        for i in range(random.randint(1,3)): #Do some damage...
            player.shush()
            count += 1
        print(underline("It was a talker!"))
        print()
        print("They wouldn't stop talking, so much time wasted, and you got shushed " + str(count) + " times!")
        print("But they go kicked out of the library, so you shouldn't see them again!")
        self.die() # you always win...
        input("Press enter to continue...")

class Wanter(Patron):
    def talk(self, player):
        clear()
        player.health -= random.randint(5, 10) # Do some damage
        #updater.updateAll(ticks = 2)
        player.update() # waste some time
        player.update()
        print(underline("Turns out they want the same book as you!"))
        print()
        print("They tried to trade coffee for it, but fighting with them used up some time...")
        print("They stormed off when you wouldn't give up the book, so I guess you win!")
        player.get(item.Coffee()) # give a coffee
        self.die() #You always win
        input("Press enter to continue...")

class Drinker(Patron):
    def talk(self, player):
        clear()
        print(underline("They sure were a party animal"))
        print()
        count = 0
        for i in range(random.randint(1,3)):
            player.update() # Waste time and give beer
            player.get(item.Beer())
            count += 1
        print("That wasted some time but maybe " + str(count) + " free beers is worth it?")
        print("And it looks like they got kicked out for drinking in the library.")
        self.die() #dead
        input("Press enter to continue...")

def random_patron():
    all_patrons = [Talker, Wanter, Drinker]
    return random.choice(all_patrons)

def name_import():
    """
    Imports data file of names registered to social security
    in 1880. Retrieved from data.gov
    """
    with open("data/names.txt", "r") as name_file:
        names = name_file.readlines()
    i = 0
    for line in names:
        names[i] = line.split(",")[0]
        i+=1
    return names



