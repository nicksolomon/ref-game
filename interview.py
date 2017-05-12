import pickle

class Answer:
    """
    A class for answers to reference questions
    """
    def __init__(self, ans, right):
        self.ans = ans
        self.next_q = None
        self.right = right

    def next(self):
        if self.next_q == None:
            return self.right
        else:
            return self.next

    def __repr__(self):
        return "Answer(**%r)" % (self.__dict__)
    def __str__(self):
        return self.ans

class Question:
    """
    A class for questions
    """
    def __init__(self, q, *args):
        self.q = q
        self.ans = args

    def ask(self):
        print(self.q)
        print()
        i = 0
        while i < len(self.ans):
            print(str(i + 1) + ") " + str(self.ans[i]))
            i += 1
        ans = int(input("> ")) - 1
        if self.ans[ans].next_q:
            self.ans[ans].next_q.ask()
        else:
            print(str(self.ans[ans].right))
            return self.ans[ans].right
    # def __repr__(self):
    #     return "Question(**%r)" % (self.__dict__)

class Interview:
    """
    Putting it all together in an interview
    """
    def __init__(self, first_q):
        self.first_q = first_q

    def do(self):
        return self.first_q.ask()



# Make a test interview
# ans1 = Answer("Nick", True)
# ans2 = Answer("Bob", False)
# ans3 = Answer("First or last?", False)
# ans4 = Answer("Nick", True)
# ans5 = Answer("Tom", False)
# first_q = Question("What's my name?", ans1, ans2, ans3)
# q2 = Question("First?", ans4, ans5)
# ans3.next_q = q2
# temp = Interview(first_q)
#
# Pickle and unpickle it
# with open("test.txt", "bw") as my_file:
#     pickler = pickle.Pickler(my_file, protocol = 0)
#     pickler.dump(temp)
#
# with open("test.txt", "br") as my_file:
#     unpickler = pickle.Unpickler(my_file)
#     temp = unpickler.load()
