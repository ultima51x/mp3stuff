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
                print mp3, "is good."
            else:
                print mp3, "has", len(messages), "problems:",
                for m in messages:
                    print m,
                print
