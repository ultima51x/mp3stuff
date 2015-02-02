from mutagen.flac import FLAC
from PIL import Image
import os.path

class NoTags:
    def check(self,f):
        return len(f.tags) > 0

    def message(self,f):
        return "There are no tags."

class TextField:
    def field(self):
        raise NotImplementedError

    def check(self,f):
        t = f.get(self.field())
        return t != None and len(t) == 1 and t[0].lstrip() != ""

    def message(self,f):
        return self.field() + " cannot be empty or blank."

class IntField:
    def field(self):
        raise NotImplementedError

    def check(self,f):
        t = f.get(self.field())
        return t != None and len(t) == 1 and t[0].isdigit()

    def message(self,f):
        return self.field() + " cannot be empty or blank or not an integer."

class Artist(TextField):
    def field(self):
        return "artist"

class AlbumArtist(TextField):
    def field(self):
        return "albumartist"

class Album(TextField):
    def field(self):
        return "album"

class Title(TextField):
    def field(self):
        return "title"

class TrackNumber(IntField):
    def field(self):
        return "tracknumber"

class TotalTracks(IntField):
    def field(self):
        return "tracktotal"

class DiscNumber(IntField):
    def field(self):
        return "discnumber"

class TotalDiscs(IntField):
    def field(self):
        return "disctotal"

class Date:
    def check(self,f):
        t = f.get('date')
        return t != None and len(t) == 1 and t[0].isdigit() and len(t[0]) == 4

    def message(self,f):
        return "Date cannot be empty, blank, or not 4 digits."

class NoGenre:
    def check(self,f):
        t = f.get('genre')
        return t is None or len(t) == 0 or (len(t) == 1 and t[0].lstrip() == '')

    def message(self,f):
        return "I don't like genres."

class FrontCover:
    def check(self,f):
        self.reason = ""
        if (len(f.pictures) > 0):
            self.reason += "There is an embedded image. "

        path_to_use = os.path.join(os.path.dirname(f.filename),"cover.jpg")
        if (os.path.exists(path_to_use)):
            image = Image.open(path_to_use)
            width, height = image.size
            if (width != height):
                self.reason += "Height and width are not equivalent. "
            if (width < 500 or height < 500):
                self.reason += "Height or width < 500px. "
        else:
            self.reason += "cover.jpg does not exist. "

        if (self.reason == ""):
            return True
        else:
            return False

    def message(self,f):
        return self.reason

class NoComment:
    def check(self,f):
        t = f.get('comment')
        return t is None or len(t) == 0 or (len(t) == 1 and t[0].lstrip() == '')

    def message(self,f):
        ret_str = ""
        for a in f.get('comment'):
            ret_str += a
        return "Comments? " + ret_str

class ReplayGain:
    def check(self,f):
        fields = ["replaygain_album_gain","replaygain_album_peak","replaygain_track_gain","replaygain_track_peak"]
        for field in fields:
            t = f.get(field)
            if t == None or len(t) == 0:
                return False
        return True

    def message(self,f):
        return "Replay gain tags should exist."

class ExtraTags:
    def extra_fields(self,f):
        tagfields = set(f.keys())
        okfields = set(['artist','albumartist','album','title','tracknumber','tracktotal','discnumber','disctotal','date','genre','comment','replaygain_album_gain','replaygain_album_peak','replaygain_track_gain','replaygain_track_peak','source'])

        a = []
        for field in tagfields - okfields:
            v = f.get(field)
            if len(v) > 0 and v[0] != '':
                a.append([field,v])
        return a

    def check(self,f):
        return len(self.extra_fields(f)) == 0

    def message(self,f):
        return "There are extra tags" + str(self.extra_fields(f))

class Validator:
    @staticmethod
    def prerules():
        return [NoTags]

    @staticmethod
    def rules():
        return [Artist,AlbumArtist,Album,Title,TrackNumber,TotalTracks,DiscNumber,TotalDiscs,Date,NoGenre,FrontCover,NoComment,ReplayGain,ExtraTags]

    def load(self,filename):
        return FLAC(filename)
