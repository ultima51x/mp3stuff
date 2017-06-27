from PIL import Image
from mutagen.mp3 import MP3
import os.path

class NoTags:
    def check(self,f):
        return len(f.tags) > 0

    def message(self,f):
        return "There are no tags"

class TextField:
    def field(self):
        raise NotImplementedError

    def check(self,f):
        t = f.tags.get(self.field())
        return t != None and len(t) == 1 and t[0].lstrip() != ""

    def message(self,f):
        return self.description() + " cannot be empty or blank."

class TupleField:
    def field(self):
        raise NotImplementedError

    def check(self,f):
        t = f.tags.get(self.field())
        return t != None and len(t) == 1 and len(t[0]) == 2

    def message(self,f):
        return self.description() + " must have a number and a total."

class ID3v2Version:
    def check(self,f):
        one, two, three = f.tags.version
        return two == 3

    def message(self,f):
        return "ID3v2 version is not 2.3"

# TODO
class NoID3v1Tag:
    def check(self,f):
        v1 = eyed3.load(f.path,eyed3.id3.tag.ID3_V1)
        return v1.tag is None

    def message(self,f):
        return "ID3v1 tag exists."

class Artist(TextField):
    def description(self):
        'Artist'

    def field(self):
        return "TPE1"

class AlbumArtist(TextField):
    def description(self):
        'Album Artist'

    def field(self):
        return "TPE2"

class Album(TextField):
    def description(self):
        'Album'

    def field(self):
        return "TALB"

class Title(TextField):
    def description(self):
        'Title'

    def field(self):
        return "TIT2"

class NoGenre(TextField):
    def description(self):
        'Genre'

    def field(self):
        return "TCON"

    def message(self,f):
        "Genre should not exist"

class TrackNumber(TupleField):
    def description(self):
        'Track Number'

    def field(self):
        return "TRCK"

class DiscNumber(TupleField):
    def description(self):
        'Disc Number'

    def field(self):
        return "TPOS"

class Date:
    def check(self,f):
        t = f.get('TDRC')
        return t != None and str(t).isdigit() and len(str(t)) == 4

    def message(self,f):
        return "Date cannot be empty, blank, or not 4 digits."

# TODO
class FrontCover:
    def check(self,f):
        self.reason = ""
        if (len(f.tag.images) > 0):
            self.reason += "There is an embedded image. "

        path_to_use = os.path.join(os.path.dirname(f.path),"cover.jpg")
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
        return len(f.tags.getall('COMM')) == 0

    def message(self,f):
        ret_str = ""
        for a in f.tags.getall('COMM'):
            ret_str += "TEXT: " + str(a)
        return "Comments? " + ret_str

# TODO
class NoLyrics:
    def check(self,f):
        return len(f.tag.lyrics) == 0

    def message(self,f):
        return "Lyrics should not exist."

class CustomFieldChecker:
    def check(self,f,field):
        tags = f.tags.getall('TXXX')
        for t in tags:
            if t.desc == field:
                return len(t.text) > 1
        return False

class ReplayGain:
    def check(self,f):
        c = CustomFieldChecker()
        return c.check(f,u"replaygain_album_gain") and c.check(f,u"replaygain_album_peak") and c.check(f,u"replaygain_track_gain") and c.check(f,u"replaygain_track_peak")

    def message(self,f):
        return "Replay gain tags should exist."

class ExtraTextTag:
    def __init__(self):
        self.text_tags = [
            ['TBPM','BPM'],
            ['TCOM','Composer'],
            ['TCOP','Copyright'],
            ['TDAT','Date'],
            ['TDEN','Encoding Time'],
            ['TDLY','Playlist Delay'],
            ['TDOR','Original Release Date'],
            ['TDRC','Playlist Delay'],
            ['TDRL','Release Time'],
            ['TDTG','Tagging Time'],
            ['TENC','Encoded by'],
            ['TEXT','Lyricist'],
            ['TFLT','File Type'],
            ['TIME','Time'],
            ['TIPL','Involved People List'],
            ['TIT3','Subtitle'],
            ['TKEY','Initial Key'],
            ['TLAN','Language'],
            ['TLEN','Length'],
            ['TMCL','Musician Credits List'],
            ['TMED','Media Type'],
            ['TMOO','Mood'],
            ['TOAL','Original Title'],
            ['TOPE','Performer'],
            ['T0FN','Original Filename'],
            ['T0LY','Original Lyricist'],
            ['T0WN','File Owner'],
            ['TPE3','Conductor'],
            ['TPE4','Interpreted or Remixed By'],
            ['TPRO','Produced'],
            ['TPUB','Publisher'],
            ['TRDA','Recording Dates'],
            ['TRSN','Internet Radio Station Name'],
            ['TRSO','Internet Radio Station Owner'],
            ['TSOA','Album Sort Order'],
            ['TSOP','Performer Sort Order'],
            ['TSOT','Title Sort Order'],
            ['TSIZ','Size'],
            ['TSRC','ISRC'],
            ['TSSE','Encoding Settings'],
            ['TSST','Set Subtitle']
        ]
        self.messages = []

    def check(self,f):
        state = True
        for t in self.text_tags:
            if f.tags.get(t[0]) is not None:
                if f.tag.getTextFrame(t[0]).lstrip() != '':
                    state = False
                    self.messages.append(t[0] + " (" + t[1]  + ")")
        return state

    def message(self,f):
        message_string = ', '.join(self.messages)
        self.messages = []
        return "Extra Text Frames: " + message_string

class CustomTextFrames:
    def __init__(self):
        self.extra_frames = []

    def check(self,f):
        # TODO
        return True

class Validator:
    @staticmethod
    def prerules():
        return [NoTags]

    @staticmethod
    def rules():
        return [ID3v2Version,NoID3v1Tag,Artist,Album,Title,TrackNumber,
            DiscNumber,Date,NoGenre,FrontCover,NoComment,NoLyrics,
            ReplayGain,AlbumArtist,ExtraTextTag,CustomTextFrames]

    def load(self,filename):
        return MP3(filename)

