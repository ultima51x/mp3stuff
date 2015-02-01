from PIL import Image
import eyed3
import os.path

class NoTags:
    def check(self,f):
        return not(f.tag is None)

    def message(self,f):
        return "There are no tags"

class ID3v2Version:
    def check(self,f):
        one, two, three = f.tag.version
        return two == 3

    def message(self,f):
        return "ID3v2 version is not 2.3"

class NoID3v1Tag:
    def check(self,f):
        v1 = eyed3.load(f.path,eyed3.id3.tag.ID3_V1)
        return v1.tag is None

    def message(self,f):
        return "ID3v1 tag exists."

class Artist:
    def check(self,f):
        return f.tag.artist != None and f.tag.artist.lstrip() != ""

    def message(self,f):
        return "Artist cannot be empty or blank."

class Album:
    def check(self,f):
        return f.tag.album != None and f.tag.album.lstrip() != ""

    def message(self,f):
        return "Album cannot be empty or blank."

class Title:
    def check(self,f):
        return f.tag.title != None and f.tag.title.lstrip() != ""

    def message(self,f):
        return "Title cannot be empty or blank."

class TrackNumber:
    def check(self,f):
        track, total = f.tag.track_num
        return track != None

    def message(self,f):
        return "Track number cannot be empty or blank."

class TotalTracks:
    def check(self,f):
        track, total = f.tag.track_num
        return total != None

    def message(self,f):
        return "Total # tracks cannot be empty or blank."

class DiscNumber:
    def check(self,f):
        disc, total = f.tag.disc_num
        return disc != None

    def message(self,f):
        return "Disc number cannot be empty or blank."

class TotalDiscs:
    def check(self,f):
        disc, total = f.tag.disc_num
        return total != None

    def message(self,f):
        return "Total # discs cannot be empty or blank."

class Date:
    def check(self,f):
        return f.tag.recording_date != None and len(str(f.tag.recording_date)) == 4

    def message(self,f):
        return "Date cannot be empty, blank, or not 4 digits."

class NoGenre:
    def check(self,f):
        return f.tag.genre is None

    def message(self,f):
        return "I don't like genres."

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
        return len(f.tag.comments) == 0

    def message(self,f):
        ret_str = ""
        for a in f.tag.comments:
            ret_str += "TEXT: " + str(a.text) + " DESC: " + str(a.description)
        return "Comments? " + ret_str

class NoLyrics:
    def check(self,f):
        return len(f.tag.lyrics) == 0

    def message(self,f):
        return "Lyrics should not exist."

class ReplayGain:
    def check(self,f):
        tf = f.tag.user_text_frames
        return tf.get(u"replaygain_album_gain") != None and tf.get(u"replaygain_album_peak") != None and tf.get(u"replaygain_track_gain") != None and tf.get(u"replaygain_track_peak") != None

    def message(self,f):
        return "Replay gain tags should exist."

class AlbumArtist:
    def check(self,f):
        return f.tag.getTextFrame("TPE2") != None and f.tag.getTextFrame("TPE2").lstrip() != ""

    def message(self,f):
        return "Album artist is blank."

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
            if f.tag.getTextFrame(t[0]) is not None:
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
        valid_frames = [u'replaygain_album_gain',u'replaygain_album_peak',u'replaygain_track_gain',u'replaygain_track_peak',u'CATALOGNUMBER']
        status = True
        for t in f.tag.user_text_frames:
            if t.description not in valid_frames:
                if t.text.lstrip() != '':
                    status = False
                    self.extra_frames.append(t.description)
        return status

    def message(self,f):
        message = ', '.join(self.extra_frames)
        self.extra_frames = []
        return "Extra TXXX frames found: " + message

class Validator:
    @staticmethod
    def prerules():
        return [NoTags]

    @staticmethod
    def rules():
        return [ID3v2Version,NoID3v1Tag,Artist,Album,Title,TrackNumber,TotalTracks,
            DiscNumber,TotalDiscs,Date,NoGenre,FrontCover,NoComment,NoLyrics,
            ReplayGain,AlbumArtist,ExtraTextTag,CustomTextFrames]

    def load(self,filename):
        return eyed3.load(filename)

