import os
import re
import urllib
import unicodedata

class MusicCollection:
    def __init__(self, folder="."):
        self.folder = folder

    @staticmethod
    def is_music(filename):
        filename, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == ".mp3" or ext == ".flac":
            return True
        else:
            return False

    def music(self):
        s = set()
        for (path, dirs, files) in os.walk(self.folder):
            for f in files:
                if self.is_music(f):
                    full_path = unicode(os.path.join(path,f),'utf-8')
                    s.add(unicodedata.normalize('NFC',full_path))
        return s

# copy and paste the xml file i have fool
class ItunesCollection(MusicCollection):
    def __init__(self, folder, itunes_xml_path):
        self.folder = folder
        self.itunes_xml_path = itunes_xml_path
        self.music_collection = MusicCollection(folder)

    def music(self):
        s = set()
        for line in open(self.itunes_xml_path):
            if "<key>Location</key>" in line and "Music/mp3" in line:
                match = re.search(r'<string>file://localhost(.+)</string>',line)
                if match is None:
                    match = re.search(r'<string>file://(.+)</string>',line)
                filename = match.group(1)
                decoded_filename = unicode(urllib.unquote(filename.replace("&#38;","&")),'utf-8')
                if self.is_music(decoded_filename):
                    s.add(unicodedata.normalize('NFC',decoded_filename))
        return s

    def not_in_my_collection(self):
        l = list(self.music() - self.music_collection.music())
        l.sort()
        return l

    def missing_from_itunes(self):
        l = list(self.music_collection.music() - self.music())
        l.sort()
        return l

