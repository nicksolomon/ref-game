import random
import item
import os
import string
from text import *
# from IPython.display import clear_output as clear

all_books = item.book_import()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def make_scramble(book):

    def scram_title(title):
        """
        Takes a title, splits it into words, scrambles each word,
        then puts the whole thing back together again.
        """
        words = title.split(" ")
        output = []
        for word in words:
            output.append("".join(random.sample(list(word), len(list(word)))))
        output_str = ""
        for word in output:
            output_str += word + " "
        return output_str[:len(output_str)-1]

    def scramble(book):
        title = scram_title(book.title)
        titles = []
        # This is kinda wonky. It makes 4 different scrambles with
        # some wrong letters put it.
        for i in range(4):
            temp = scram_title(book.title).split(" ")
            scramd = []
            for word in temp:
                temp_word = list(word)
                if len(word) > 1:
                    for j in range(random.randint(1, min(3,len(word)))):
                        index = random.randint(0, len(temp_word)-1)
                        temp_word[index] = random.choice(string.ascii_letters) #insert some wrong letters
                scramd.append("".join(temp_word))
            titles.append(" ".join(scramd))
        correct = random.randint(0,4) # choose an index for the right title, then insert it into the list
        titles.insert(correct, title)
        guessed = False
        tries = 0
        while not guessed:
            clear()
            print(underline("Puzzle"))
            print("All the titles got scrambled, only one of these is has all the same letters as " + book.title)
            print()
            i = 1
            for line in titles:
                print_list(bold("[" + str(i) + "] ") + line)
                i += 1
            while True:
                try:
                    guess = int(input("Which is the book you're looking for (enter a number from 1 to 10)? ")) - 1
                    break
                except ValueError:
                    print("That's not a number.")

            tries += 1
            if guess == correct:
                clear()
                print(underline("Puzzle"))
                print("Great! You got the book!")
                input("Press enter to continue...")
                return True
            elif tries < 3:
                clear()
                print(underline("Puzzle"))
                print("Sorry, that's not the right book.")
                input("Press enter to try again...")
            else:
                print("Sorry, you're out of guesses! You'll have to come back later.")
                return False
    return scramble(book)

def make_hangman(book):
    title = book.title.lower()
    def hangman(title):
        guesses = 0
        correct = False
        blanks = []
        # Build a list of underscores etc. for hangman
        for char in title:
            if char == " ":
                blanks.append(" | ")
            elif char not in string.ascii_letters:
                blanks.append(char)
            else:
                blanks.append(" _ ")

        while not correct and guesses < 6 :
            clear()
            print(underline("Puzzle"))
            print()
            print("Do you remember the title of the book in this room?")
            print(str(guesses) + "/6 guesses taken")
            print("".join(blanks))
            guess = input("guess a letter: ").lower()
            i = 0
            worked = False
            for char in title:
                # Fill in the guess
                if char == guess:
                    blanks[i] = guess
                    worked = True
                i += 1
            if not worked:
                guesses += 1
            if " _ " not in blanks: #if there's no more _'s you filled it in!
                correct = True
                print("You got the book!")
                input("Press enter to continue...")
        if not correct:
            clear()
            print(underline("Puzzle"))
            print("You ran out of guesses, I guess you'll have to try again")
        return correct
    return hangman(title)

def make_matching(book):
    def matching(book):
        title = book.title
        cat_desc = book.cat_desc
        unique = True
        #grab 4 different books and make sure none of them are
        # the one the player is solving for
        while unique:
            descriptions = random.sample(all_books, 4)
            unique = book in descriptions
        for i in range(len(descriptions)):
            descriptions[i] = descriptions[i].cat_desc #get descriptions
        correct = random.randint(0, 3) # put the right one it
        descriptions.insert(correct, cat_desc)
        guesses = 0
        did_it = False
        while not did_it and guesses < 3:
            clear()
            print(underline("Puzzle"))
            print()
            print("One of these books is " + title + " but all the titles are worn off! I guess you'll just have to go by the descriptions...")
            print()
            i = 1
            for desc in descriptions:
                # Print them, but truncate at 200 characters so it all fits on one screen.
                print_list(bold("[" + str(i) + "] ") + desc[:min(len(desc), 200)] + "...")
                i += 1
            print()
            while True:
                try:
                    guess = int(input("Which is the description of the book you're looking for? ")) - 1
                    break
                except ValueError:
                    print("That's not a number.")
            guesses += 1
            if guess == correct:
                did_it = True
                clear()
                print(underline("Puzzle"))
                print("You got the book!")
                input("Press enter to continue...")
                return did_it
            else:
                clear()
                print(underline("Puzzle"))
                print()
                print("That's not the one. You have " + str(3 - guesses) + " geusses left.")
                input("Press enter to try again...")
        return False
    return matching(book)

def make_lc(book):
    def lc(book):
        # pretty much the same as matching.
        title = book.title
        lc_num = book.call
        unique = True
        while unique:
            rand_books = random.sample(all_books, 4)
            unique = book in rand_books
        call_nums = []
        for i in range(len(rand_books)):
            call_nums.append(rand_books[i].call)
        correct = random.randint(0,3)
        call_nums.insert(correct, lc_num)
        did_it = False
        guesses = 0
        while not did_it and guesses < 3:
            clear()
            print(underline("Puzzle"))
            print()
            print("One of these books is " + title + "but you can only see the the Library of Congress call numbers. For more information about these look at this website: https://www.loc.gov/catdir/cpso/lcco/")
            i = 1
            for num in call_nums:
                print_list(bold("[" + str(i) + "] ") + num)
                i += 1
            while True:
                try:
                    guess = int(input("Which call number is the book you're looking for? ")) - 1
                    break
                except ValueError:
                    print("That's not a number")
            guesses += 1
            if guess == correct:
                did_it = True
                clear()
                print(underline("Puzzle"))
                print("You got the book!")
                input("Press enter to continue...")
                return did_it
            else:
                clear()
                print(underline("Puzzle"))
                print()
                print("That's not the one. You have " + str(3 - guesses) + " geusses left.")
                input("Press enter to try again...")
        return False
    return lc(book)

def rand_puzzle():
    puzzles = [make_scramble, make_hangman, make_matching, make_lc]
    return random.choice(puzzles)

