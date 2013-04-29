import os

import termcolor

from validators import ValidationAggregator

class Analyzer:
    def __init__(self):
        self.validator = ValidationAggregator.getTheValidators()

    def is_mp3(self, filename):
        filename, ext = os.path.splitext(filename)
        if ext == ".mp3" or ext == ".MP3":
            return True
        else:
            return False

    def list_of_mp3s(self, path):
        l = []
        for (path, dirs, files) in os.walk(path):
            for f in files:
                if self.is_mp3(f):
                    l.append(os.path.join(path,f))
        return l

    def analyze_recursively(self, path='.'):
        print "-------------------------"
        print "STARTING id3 TAG ANALYSIS"
        print "-------------------------"
        for mp3 in self.list_of_mp3s(path):
            messages = self.validator.validate_all(mp3)
            if len(messages) == 0:
                print termcolor.colored(mp3 + " is good.", 'green')
            else:
                print termcolor.colored(mp3 + " has problems.", 'yellow')
                for m in messages:
                    print "  ",
                    print termcolor.colored(m,'red')
