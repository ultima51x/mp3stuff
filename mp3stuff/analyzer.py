import os

import termcolor

from validators import ValidationAggregator
from music_collection import MusicCollection

class Analyzer:
    def __init__(self):
        self.validator = ValidationAggregator.getTheValidators()

    def analyze_recursively(self, path):
        print "-------------------------"
        print "STARTING TAG ANALYSIS"
        print "-------------------------"
        collection = MusicCollection(path)
        for file in collection.music():
            messages = self.validator.validate_all(file)
            if len(messages) == 0:
                print termcolor.colored(file + " is good.", 'green')
            else:
                print termcolor.colored(file + " has " + str(len(messages)) + " problems:", 'yellow'),
                i = 0
                for m in messages:
                    color = 'red'
                    if i % 2 == 1:
                        color = 'yellow'
                    print termcolor.colored(m,color),
                    i += 1
                print
