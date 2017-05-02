# This file contains algorithms and data structures used throughout the project

class Enum:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<%s , %s >" % (self.__class__.__name__ , self.name)

    __repr__ = __str__