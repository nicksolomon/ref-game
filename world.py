import room as rm
import os
from player import Player
import item
import patron
import character
import puzzle
import world
import os
import datetime as dt
import random
#from IPython.display import clear_output as clear

all_books = item.book_import()
all_names = patron.name_import()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class World:
    def __init__(self):
        self.patrons = []
        self.characters = []
        self.num_books = 5
        self.books = random.sample(all_books, self.num_books)
        self.book_rooms = [rm.Book_room(book, puzzle.rand_puzzle()) for book in self.books]
        self.studies = [rm.Study_room() for i in range(self.num_books)]
        self.computers = [rm.Comp_room(book) for book in self.books]
        self.num_patrons = 0
        self.num_killed = 0
        self.updates = []
        self.start = rm.Room("This is the library, find the books.")

        # Let's build a random world! Start with everything unconnected except the starting room
        unconnected_rooms = self.book_rooms + self.studies + self.computers
        connected_rooms = [self.start]

        def connect_rooms(connected, unconnected):
            """
            Recursive function for connecting rooms. Base case is all
            rooms are connected. Otherwise choose a random room that's
            already on the map. If it has unused directions, connect a
            random room that's not yet on the map to one of them, then
            that room is now connected. Lather, rinse, repeat until a
            world is built.
            """
            if not unconnected:
                return None
            else:
                rand_room = random.choice(connected)
                if len(rand_room.exits) != 4:
                    rand_unroom = random.choice(unconnected)
                    done = True
                    while done:
                        direc = random.choice([("north", "south"), ("south", "north"), ("east", "west"), ("west", "east")])
                        if direc[0] not in rand_room.exitNames():
                            rm.Room.connectRooms(rand_room, direc[0], rand_unroom, direc[1])
                            done = False
                            unconnected.remove(rand_unroom)
                            connected.append(rand_unroom)
                connect_rooms(connected, unconnected)
        connect_rooms(connected_rooms, unconnected_rooms)
        
        # Let's add some people to the study rooms.
        for i in range(random.randint(3, 7)):
            rand_type = patron.random_patron()
            in_room = random.choice(self.studies)
            rand_type(random.choice(all_names), in_room, self)

        for i in range(random.randint(3, 7)):
            rand_type = character.rand_char()
            in_room = random.choice(self.studies)
            rand_type(random.choice(all_names), in_room, self)

        self.register(self)


    def addPatron(self, patron):
        self.patrons.append(patron)
        patron.room.addPatron(patron)
        self.num_patrons += 1
    def removePatron(self, patron):
        self.patrons.remove(patron)
        patron.room.removePatron(patron)
        self.num_killed += 1
    def addCharacter(self, character):
        self.characters.append(character)
        character.room.addCharacter(character)
    def removeCharacter(self, character):
        self.characters.remove(character)
        character.room.removeCharacter(character)
    def update(self):
        """
        at every tick, add a random patron with probability equal
        to the ratio of patrons killed to patrons created. This
        means the more you talk to patrons, the more often they will
        be created.
        """
        if random.random() < self.num_killed/self.num_patrons:
            patron.random_patron()(random.choice(all_names), random.choice(self.studies), self)

    # I moved the update functionality from the starter code into the
    # world class for simplicity.
    def updateAll(self, ticks = 1):
        for i in range(ticks):
            for u in self.updates:
                u.update()

    def register(self, thing):
        self.updates.append(thing)

    def deregister(self, thing):
        self.updates.remove(thing)

    def clear(self):
        for room in self.studies:
            room.characters = []
            room.patrons = []
        self.characters = []
        self.patrons = []




            