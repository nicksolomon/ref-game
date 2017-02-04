# import os

import datetime as dt
from text import *
from IPython.display import clear_output as clear

# def clear():
    # os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, world):
        self.location = world.start
        self.items = []
        self.maxhealth = 100
        self.health = 100
        self.stress = 0
        self.maxstress = 100
        self.stealth = 100
        self.maxstealth = 100
        self.time = dt.datetime(2016, 11, 26, 0)
        self.desc = "In inventory"
        self.inv_max = 100
        self.inv_weight = 0
        self.world = world
        self.num_books = 0
        world.register(self)
    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)
    def pickup(self, item):
        if item.__class__.__name__ != "Book":
            # Can't just pickup a book! You have to solve the puzzle!
            if self.inv_weight + item.cost <= self.inv_max:
                self.items.append(item)
                item.loc = self
                self.location.removeItem(item)
                self.inv_weight += item.cost
                return True
            else:
                print("Not enough room in inventory. Maybe you can use this item without picking it up.")
                return False
        else:
            print("You have to solve the puzzle first!")
            return False
    def get(self, item):
        """
        A method for getting loot from NPCs
        """
        if self.inv_weight + item.cost <= self.inv_max:
            self.items.append(item)
            self.inv_weight += item.cost
            item.loc = self
        else:
            self.location.addItem(item)
    def pickup_book(self, item):
        """
        A special method for picking up books, becuase regular
        pickup can't do it
        """
        if self.inv_weight + item.cost <= self.inv_max:
            self.items.append(item)
            item.loc = self
            self.location.removeItem(item)
            self.num_books += 1
            self.inv_weight += item.cost
            return True
        else:
            print("Not enough room in inventory. Get rid of some stuff and solve the puzzle again.")
            return False
    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def drop(self, item):
        if item.__class__.__name__ != "Book":
            # Only let them drop non books cause pickup doesn't work on books
            self.items.remove(item)
            item.loc = self.location
            self.location.addItem(item)
            return True
        else:
            print("Don't drop your book!")
            return False

    def useItem(self, item):
        result = item.use(self)
        if result:
            self.items.remove(item)
        return False
    def showInventory(self):
        clear()
        print("You are currently carrying:")
        print()
        list_items(self.items) #see text.py
        print()
        tot_weight = 0
        for item in self.items:
            tot_weight += item.cost
        print("Weight: " + str(self.inv_weight) + " of 100")
        print()
        input("Press enter to continue...")
    # def attackMonster(self, mon):
    #     clear()
    #     print("You are attacking " + mon.name)
    #     print()
    #     print("Your health is " + str(self.health) + ".")
    #     print(mon.name + "'s health is " + str(mon.health) + ".")
    #     print()
    #     if self.health > mon.health:
    #         self.health -= mon.health
    #         print("You win. Your health is now " + str(self.health) + ".")
    #         mon.die()
    #     else:
    #         print("You lose.")
    #         self.alive = False
    #     print()
    #     input("Press enter to continue...")
    def talk(self, other):
        other.talk(self)
    def status(self):
        """
        Lists remaining books. All other important info is displayed
        at the top of the main screen.
        """
        clear()
        print(underline("Player status"))
        print()
        print("You have to find the books you need before the library closes at 2:30.")
        print("These are the ones you still need to find:")
        print()
        i = 1
        for book in self.world.books:
            if i < 10:
                num = "[" + str(i) + "]  "
            else:
                num = "[" + str(i) + "] "
            if book not in self.items:
                print_list(bold(num) + bold(book.title))
                i += 1
        print()
        print("Don't let your health get to zero, your stress get to 100, or the time get to 2:30. Good luck!")
        input("Press enter to continue...")
    def shush(self):
        self.stress += 5
        self. health -= 1
    def update(self):
        self.time = self.time + dt.timedelta(minutes = 1)
        self.health -= 1
        self.stress += 1
        if self.stealth < self.maxstealth:
            self.stealth += 1
    def is_alive(self):
        if self.health > 0 and self.stress < 100 and self.time <= dt.datetime(2016, 11, 26, 2, 30):
            return True
        else:
            clear()
            print(underline("Game over!"))
            print()
            print("Time: " + self.time.strftime("%I:%M") + " | " + "Health: " + str(self.health) + " | " + "Stress: " + str(self.stress) + " | " + "Stealth: " + str(self.stealth) + " | " + "Books found: " + str(self.num_books) + "/" + str(self.world.num_books))
            print()
            input("Press enter to exit...")
            return False

