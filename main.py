import random
import room as rm
from player import Player
import item
import patron
import character
import puzzle
import world as wld
import os
import datetime as dt
from text import *
import string
# from IPython.display import clear_output as clear

# try:
#     import readline #this module doesn't work on windows 
# except:
#     None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    clear()
    # Print a bunch of status info
    print(underline("Time: " + player.time.strftime("%I:%M") + " | " + "Health: " + str(player.health) + " | " + "Stress: " + str(player.stress) + " | " + "Stealth: " + str(player.stealth) + " | " + "Books found: " + str(player.num_books) + "/" + str(world.num_books)))
    print()
    print(player.location.desc)
    # If the room is a book room, but you already got the book,
    # make that clear
    if player.location.__class__.__name__ == "Book_room" and not player.location.hasBook():
        print(bold("You've already gotten the book you need from this room."))
    print()
    if player.location.hasPatrons():
        print(bold("This room contains the following people:"))
        for m in player.location.patrons:
            print(red(m.name)) # Patrons are red
        for c in player.location.characters:
            print(green(c.name)) # Characters are green
        print()
    if player.location.hasBook():
        print(bold("There's a book in here:"))
        for book in player.location.items:
            if book.__class__.__name__ == "Book":
                print(book.name)
        print()
    if player.location.hasItems():
        temp = []
        for i in player.location.items:
            if i.__class__.__name__ != "Book": #make a list of non-book items
                temp.append(i)
        print(bold("This room contains the following items:"))
        list_items(temp, bold_item = False)
        print()
    print(bold("You can go in the following directions:"))
    for e in sorted(player.location.exitNames()):
        print(e)
    print()

def showHelp():
    clear()
    print(underline("Available commands:"))
    print()
    print(bold("go <direction>") + " -- moves you in the given direction")
    print(bold("inventory") + " ------- opens your inventory")
    print(bold("drop <item>") + " ----- drops the item from you inventory")
    print(bold("pickup <item>") + " --- picks up an item in the room")
    print(bold("use <item>") + " ------ uses <item>")
    print(bold("wait <number>") + " --- waits <number> minutes")
    print(bold("status") + " ---------- shows game status")
    print(bold("inspect <item>") + " -- shows more information about an item")
    print(bold("solve") + " ----------- lets you try to solve the puzzle")
    print(bold("talk <name>") + " ----- talks to <name>")
    print(bold("help") + " ------------ show this screen")
    print()
    input("Press enter to continue...")

clear()
# print(underline("Welcome to my game!"))
# print()
# loaded = False
# load = input("Would you like to load a saved game? (y/n) ").lower()
# if load[0] == "y":
#     loaded = True
#     print(underline("Available games:"))
#     dirs = os.listdir("saves")
#     for save in dirs:
#         if save[0] != ".":
#             print(save)
#     name = input("What is the name of your game: ")
#     file = "saves/"+name
#     try:
#         with open(file + "/world.pickle", "rb") as world_save:
#             world_save_bytes = world_save.read() 
#             world = pickle.loads(world_save_bytes)
#         with open(file + "/player.pickle", "rb") as player_save: 
#             player_save_bytes = player_save.read()
#             player = pickle.loads(player_save_bytes)
#         # with open(file + "/updater.pickle", "rb") as updater_save: 
#         #     updater = pickle.load(updater_save)
#     except:
#         loaded = False
#         input("Couldn't load that game...")
#         world = wld.World()
#         player = Player(world)
#         raise
# else:
world = wld.World()
player = Player(world)


def game(player):
    playing = True
    ticks = 1
    player.status()
    showHelp()
    while playing and player.is_alive():
        printSituation()
        commandSuccess = False
        timePasses = False
        while not commandSuccess:
            commandSuccess = True
            command = input(bold("What now? "))
            print()
            commandWords = command.lower().split() + [""]
            if commandWords == []:
                commandSuccess = False
            elif commandWords[0].lower() == "go":   #cannot handle multi-word directions
                if commandWords[1] in player.location.exitNames():
                    player.goDirection(commandWords[1]) 
                    timePasses = True
                    # When stealth gets lower, you're more likely to get shushed
                    if random.random() > player.stealth/player.maxstealth:
                        player.shush()
                        print("You got shushed, better lay off the beer...")
                        input("Press enter to continue...")
                else:
                    print("Can't go that way")
                    commandSuccess = False
            elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
                targetName = command[7:]
                target = player.location.getItemByName(targetName)
                if target != False:
                    commandSuccess = player.pickup(target)
                else:
                    print("No such item.")
                    commandSuccess = False
            elif commandWords[0].lower() == "drop":
                targetName = command[5:]
                if player.getItemByName(targetName):
                    item = player.getItemByName(targetName)
                    commandSuccess = player.drop(item)
                else:
                    print("You don't have that item.")
                    commandSuccess = False
            elif commandWords[0].lower() == "inventory":
                player.showInventory()        
            elif commandWords[0].lower() == "help":
                showHelp()
            elif commandWords[0].lower() == "exit":
                # save = input("Save game? (y/n)").lower()
                # if save[0] == "y":
                #     if not loaded:
                #         while True:
                #             game_name = input("Name your game: ")
                #             for char in game_name:
                #                 if char not in string.ascii_letters:
                #                     print("Letters only, please.")
                #                     break
                #             else:
                #                 break
                #         file = "saves/"+game_name
                #     os.makedirs(file, exist_ok = True)
                #     with open(file+"/world.pickle", "wb") as world_save:
                #         world_bytes = pickle.dumps(world, protocol = pickle.HIGHEST_PROTOCOL)
                #         world_save.write(world_bytes)
                #     with open(file+"/player.pickle", "wb") as player_save:
                #         player_bytes = pickle.dumps(player, protocol = pickle.HIGHEST_PROTOCOL)
                #         player_save.write(player_bytes)
                #     # with open(file+"/updater.pickle", "wb") as updater_save:
                #     #     pickle.dump(updater, updater_save, protocol = pickle.HIGHEST_PROTOCOL)
                playing = False
            elif commandWords[0].lower() == "wait":
                if len(commandWords) > 2:
                    turns = int(commandWords[1])
                else:
                    turns = 1
                timePasses = True
                ticks = turns
            elif commandWords[0].lower() == "status":
                player.status()
            elif commandWords[0].lower() == "inspect":
                targetName = command[8:]
                # Try to find the item in the inventory then in the room
                if player.location.getItemByName(targetName):
                    target = player.location.getItemByName(targetName)
                elif player.getItemByName(targetName):
                    target = player.getItemByName(targetName)
                else:
                    print("No such item.")
                    commandSuccess = False
                    continue
                target.inspect()
            elif commandWords[0].lower() == "use":
                targetName = command[4:]
                # same deal as inspect
                target_player = player.getItemByName(targetName)
                target_room = player.location.getItemByName(targetName)
                if target_player != False:
                    if player.useItem(target_player) == False:
                        commandSuccess = False
                elif target_room != False:
                    target_room.use(player)
                    commandSuccess = False
                else:
                    print("You don't have that item")
                    commandSuccess = False
            elif commandWords[0] == "solve":
                if player.location.hasBook():
                    if player.location.puzzle(player.location.book):
                        # if the puzzle is solved use the special book method
                        player.pickup_book(player.location.book)
                    if player.num_books == world.num_books:
                        # A victory condition!
                        clear()
                        print(underline("Victory!"))
                        print()
                        print("You did it! You have all the books!")
                        input("Press enter to continue...")
                        playing = False
                else:
                    print("You've already solved this puzzle!")
                    commandSuccess = False
            elif commandWords[0] == "talk":
                target = player.location.getPatronByName(commandWords[1])
                if target:
                    target.talk(player)
                    timePasses = True
                else:
                    print("Nobody with that name...")
                    commandSuccess = False
            else:
                print("Not a valid command")
                commandSuccess = False
        if timePasses == True:
            world.updateAll(ticks)
            ticks = 1

def go():
    game(player)
    
go()

