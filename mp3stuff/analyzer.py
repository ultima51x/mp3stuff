import os

import termcolor

from validators import ValidationAggregator
from mp3 import Mp3Collection

class Analyzer:
    def __init__(self):
        self.validator = ValidationAggregator.getTheValidators()

    def analyze_recursively(self, path):
        print "-------------------------"
        print "STARTING id3 TAG ANALYSIS"
        print "-------------------------"
        collection = Mp3Collection(path)
        for mp3 in collection.folder_mp3s():
            messages = self.validator.validate_all(mp3)
            if len(messages) == 0:
                print termcolor.colored(mp3 + " is good.", 'green')
            else:
                print termcolor.colored(mp3 + " has " + str(len(messages)) + " problems:", 'yellow'),
                i = 0
                for m in messages:
                    color = 'red'
                    if i % 2 == 1:
                        color = 'yellow'
                    print termcolor.colored(m,color),
                    i += 1
                print
