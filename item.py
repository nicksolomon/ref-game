import os
from text import *
import random
#from IPython.display import clear_output as clear

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, cost = 0):
        self.name = name
        self.desc = desc
        self.cost = cost
        self.loc = None
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)
    def inspect(self):
        clear()
        print(underline(self.name + ":"))
        print(self.desc)
        print("Weight: " + bold(str(self.cost)))
        if self.loc.__class__.__name__ == "Player":
            print("Item is in inventory.")
        print()
        input("Press enter to continue...")

class Coffee(Item):
    def __init__(self, name = "Coffee", desc = "Helps you keep you energy levels up, but don't get too stressed out!", cost = 10):
        Item.__init__(self, name, desc, cost)
        self.health_boost = 10
        self.stress_boost = 10
    
    def use(self, player):
        """
        Adds up to 10 health and up to 10 stress, but checks to make
        sure it's not over the max
        """
        if player.health <= player.maxhealth - self.health_boost:
            player.health += self.health_boost
            print("Health is now " + str(player.health))
            if player.stress <= player.maxstress - self.stress_boost:
                player.stress += self.stress_boost
                print("Stress is now " + str(player.stress))
            else:
                player.stress = player.maxstress
                print("Stress is now " + str(player.stress))
            return True
        elif player.health < player.maxhealth:
            player.health = player.maxhealth
            print("Health is now " + str(player.health))
            if player.stress <= player.maxstress - stress_boost:
                player.stress += self.stress_boost
                print("Stress is now " + str(player.stress))
            else:
                player.stress = player.maxstress
                print("Stress is now " + str(player.stress))
            return True
        else:
            print("Health is already full")
        return False

class Beer(Item):
    def __init__(self, name = "Beer", desc = "Decrease stress, but you'll become more clumsy. Don't get shushed!", cost = 10):
        Item.__init__(self, name, desc, cost)
        self.stress_boost = -10
        self.stealth_boost = -10

    def use(self, player):
        """
        Subtracts up to 10 stress and up to 10 stealth, but doesn't
        let either go negative.
        """
        if player.stress >= -self.stress_boost:
            player.stress += self.stress_boost
        elif player.stress > 0:
            player.stress = 0
        else:
            print("Stress is already 0")
            return False

        if player.stealth >= -self.stealth_boost:
            player.stealth += self.stealth_boost
        else:
            player .stealh = 0

        print("Stress is now " + str(player.stress))
        print("Stealth is now " + str(player.stealth))
        return True

class Book(Item):
    def __init__(self, name, desc, author, call_num ,cost = 10):
        Item.__init__(self, name, desc, cost)
        self.title = name
        self.author = author
        self.cat_desc = desc
        self.call = call_num
    def use(self, player):
        print("You can't use this item")
        return False

class Kiosk(Item):
    def __init__(self, book, name = "Kiosk", desc = "Talk to Linda the Librarian for help"):
        Item.__init__(self, name, desc, cost = 999)
        self.loc = None

    def use(self, player):
        """
        Checks each neighboring room for a book and tells the player
        which direction to go.
        """
        print(underline("Librarian Linda can help you find the book you're looking for!"))
        print()
        found = False
        for exit in self.loc.exits:
            if exit[1].hasBook():
                print("There's a book you're looking for if you head " + exit[0])
                found = True
        if not found:
            print("None of the neighboring rooms have books in them. Try exploring the library a little more.")


        # direction = path_to(self.loc, book.loc)
        # print("Head " + direction[1])

class Printer(Item):
    def __init__(self, name = "Printer", desc = "Printer"):
        Item.__init__(self, name, desc, cost = 999)
        self.paper_level = random.randint(0,100)
        self.checked = False
    def check_paper(self):
        print("The paper tray is " + str(self.check_paper)+ "% full.")
    def fill_paper(self):
        self.paper_level = 100
        self.checked = True
    def use(self, player):
        print("I hope you're not doing homework on the job. Check how much paper is left in the printer before you leave this room.")

def book_import():
    """
    Reads in data file of book info. Special thanks to Abigail Bibee
    in the library for this data!
    """
    # output = [Book("Book " + str(i), "Book " + str(i) + " out of 1000", "The Author", "QA76." + str(i)) for i in range(1000)]
    # with open("data/books.txt", "w") as book_file:
    #     for book in output:
    #         out_line = book.title + "," + book.cat_desc + "," + book.author + "," + book.call + "\n"
    #         book_file.writelines(out_line)
    output = []
    with open("data/books.txt", "r", encoding = "utf-8") as book_file:
        for line in book_file:
            args = line.split("\t")
            output.append(Book(args[0], args[1], args[2], args[3]))
    return output



