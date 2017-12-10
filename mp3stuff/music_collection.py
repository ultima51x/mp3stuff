import re
import urllib.request, urllib.parse, urllib.error
import unicodedata
import os

from mp3stuff.validators.mp3 import Validator as Mp3Validator
from mp3stuff.validators.flac import Validator as FlacValidator
from mp3stuff.validators.mp4 import Validator as Mp4Validator

class MusicCollection:
    def __init__(self, folders=[os.getcwd()]):
        self.folders = folders

    @staticmethod
    def extension(filename):
        filename,ext = os.path.splitext(filename)
        return ext.lower()

    @staticmethod
    def validators():
        return {".mp3": Mp3Validator, ".flac": FlacValidator, ".m4a": Mp4Validator}

    @classmethod
    def is_music(cls,filename):
        if cls.extension(filename) in list(cls.validators().keys()):
            return True
        else:
            return False

    @staticmethod
    def normalized_path(path):
        if os.name == 'posix':
            if type(path) == str:
                return path
            else:
                return unicodedata.normalize('NFC',str(path,'utf-8'))
        else:
            return path

    def validate(self,filename):
        ext = self.extension(filename)
        vr = self.validators()[ext]()   # dynamically calling constructor
        f = vr.load(filename)

        messages = []
        for r in vr.prerules():
            cr = r()
            if cr.check(f) is False:
                messages.append(cr.message(f))
        if len(messages) > 0:
            return messages

        for r in vr.rules():
            cr = r()
            if cr.check(f) is False:
                messages.append(cr.message(f))
        return messages

    def music(self):
        s = set()
        for folder in self.folders:
            for (path, dirs, files) in os.walk(folder):
                for f in files:
                    if self.is_music(f):
                        s.add(self.normalized_path(os.path.join(path,f)))
        return s

# TODO need a more general case to avoid podcasts
class ItunesCollection(MusicCollection):
    def __init__(self, folders, itunes_xml_path):
        self.folders = folders
        self.itunes_xml_path = itunes_xml_path
        self.music_collection = MusicCollection(self.folders)

    def music(self):
        s = set()
        for line in open(self.itunes_xml_path):
            if "<key>Location</key>" in line and ("Music/mp3" in line or "Music/alac" in line):
                match = re.search(r'<string>file://localhost(.+)</string>',line)
                if match is None:
                    match = re.search(r'<string>file://(.+)</string>',line)
                filename = match.group(1)
                decoded_filename = urllib.parse.unquote(filename.replace("&#38;","&"))
                if self.is_music(decoded_filename):
                    s.add(self.normalized_path(decoded_filename))
        return s

    def not_in_my_collection(self):
        l = list(self.music() - self.music_collection.music())
        l.sort()
        return l

    def missing_from_itunes(self):
        l = list(self.music_collection.music() - self.music())
        l.sort()
        return l

