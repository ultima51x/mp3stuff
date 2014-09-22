import os
import re
import urllib
import unicodedata

class Mp3:
    @staticmethod
    def is_mp3(filename):
        filename, ext = os.path.splitext(filename)
        if ext == ".mp3" or ext == ".MP3":
            return True
        else:
            return False

class Mp3Collection:
    def __init__(self, folder_path=".", itunes_path=os.path.join(os.path.expanduser('~'),"Music","mp3")):
        self.folder_path = folder_path
        self.itunes_path = itunes_path

    def itunes_mp3s(self):
        s = set()
        for line in open(self.itunes_path):
            if "<key>Location</key>" in line and "Music/mp3" in line:
                filename = re.search(r'<string>file://localhost(.+)</string>',line).group(1)
                decoded_filename = unicode(urllib.unquote(filename.replace("&#38;","&")),'utf-8')
                if Mp3.is_mp3(decoded_filename):
                    s.add(unicodedata.normalize('NFC',decoded_filename))
        return s

    def folder_mp3s(self):
        s = set()
        for (path, dirs, files) in os.walk(self.folder_path):
            for f in files:
                if Mp3.is_mp3(f):
                    full_path = unicode(os.path.join(path,f),'utf-8')
                    s.add(unicodedata.normalize('NFC',full_path))
        return s

    def not_in_my_collection(self):
        list_of_mp3s = list(self.itunes_mp3s() - self.folder_mp3s())
        list_of_mp3s.sort()
        return list_of_mp3s

    def missing_from_itunes(self):
        list_of_mp3s = list(self.folder_mp3s() - self.itunes_mp3s())
        list_of_mp3s.sort()
        return list_of_mp3s
