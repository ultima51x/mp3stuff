import os
import termcolor

from music_collection import MusicCollection

class Analyzer:
    def analyze_recursively(self, path):
        print "-------------------------"
        print "STARTING TAG ANALYSIS"
        print "-------------------------"
        if path is None:
            collection = MusicCollection()
        else:
            collection = MusicCollection([path])
        files = list(collection.music())
        files.sort()
        for f in files:
            messages = collection.validate(f)
            if len(messages) == 0:
                print termcolor.colored(f + " is good.", 'green')
            else:
                print termcolor.colored(f + " has " + str(len(messages)) +
                                        " problems:", 'yellow'),
                i = 0
                for m in messages:
                    color = 'red'
                    if i % 2 == 1:
                        color = 'yellow'
                    print termcolor.colored(m,color),
                    i += 1
                print
