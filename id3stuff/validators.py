import eyed3

class ValidationAggregator:
    def __init__(self):
        self.validators = []

    def add(self, validator):
        self.validators.append(validator)

    def validate_all(self, filename):
        self.f = eyed3.load(filename)
        messages = []
        if self.f.tag is None:
            messages.append("NO TAG EXISTS.")
            return messages
        for v in self.validators:
            if v.validate(self.f) == False:
                messages.append(v.message())
        return messages

    @staticmethod
    def getTheValidators():
        validator = ValidationAggregator()
        validator.add(ID3v2VersionValidator())
        validator.add(ID3v2VersionValidator())
        validator.add(NoID3v1TagValidator())
        validator.add(ArtistValidator())
        validator.add(AlbumValidator())
        validator.add(TitleValidator())
        validator.add(TrackNumberValidator())
        validator.add(TotalTracksValidator())
        validator.add(DiscNumberValidator())
        validator.add(TotalDiscsValidator())
        validator.add(DateValidator())
        validator.add(NoGenreValidator())
        validator.add(NoImagesValidator())
        validator.add(NoCommentValidator())
        validator.add(NoLyricsValidator())
        validator.add(ReplayGainValidator())
        validator.add(AlbumArtistValidator())
        validator.add(ExtraTextTagValidator())
        validator.add(CustomTextFramesValidator())
        return validator

class ID3v2VersionValidator:
    def validate(self,f):
        one, two, three = f.tag.version
        return two == 3

    def message(self):
        return "ID3v2 version is not 2.3"

class NoID3v1TagValidator:
    def validate(self,f):
        v1 = eyed3.load(f.path,eyed3.id3.tag.ID3_V1)
        return v1.tag is None

    def message(self):
        return "ID3v1 tag exists."

class ArtistValidator:
    def validate(self,f):
        return f.tag.artist != None and f.tag.artist.lstrip() != ""

    def message(self):
        return "Artist cannot be empty or blank."

class AlbumValidator:
    def validate(self,f):
        return f.tag.album != None and f.tag.album.lstrip() != ""

    def message(self):
        return "Album cannot be empty or blank."

class TitleValidator:
    def validate(self,f):
        return f.tag.title != None and f.tag.title.lstrip() != ""

    def message(self):
        return "Title cannot be empty or blank."

class TrackNumberValidator:
    def validate(self,f):
        track, total = f.tag.track_num
        return track != None

    def message(self):
        return "Track number cannot be empty or blank."

class TotalTracksValidator:
    def validate(self,f):
        track, total = f.tag.track_num
        return total != None

    def message(self):
        return "Total # tracks cannot be empty or blank."

class DiscNumberValidator:
    def validate(self,f):
        disc, total = f.tag.disc_num
        return disc != None

    def message(self):
        return "Disc number cannot be empty or blank."

class TotalDiscsValidator:
    def validate(self,f):
        disc, total = f.tag.disc_num
        return total != None

    def message(self):
        return "Total # discs cannot be empty or blank."

class DateValidator:
    def validate(self,f):
        return f.tag.recording_date != None and len(str(f.tag.recording_date)) == 4

    def message(self):
        return "Date cannot be empty, blank, or not 4 digits."

class NoGenreValidator:
    def validate(self,f):
        return f.tag.genre is None

    def message(self):
        return "I don't like genres."

class NoImagesValidator:
    def validate(self,f):
        return len(f.tag.images) == 0

    def message(self):
        return "Embedded images exist. Add them after they're in iTunes."

class NoCommentValidator:
    def validate(self,f):
        return len(f.tag.comments) == 0

    def message(self):
        return "Are you sure you want comments?"

class NoLyricsValidator:
    def validate(self,f):
        return len(f.tag.lyrics) == 0

    def message(self):
        return "Lyrics should not exist."

class ReplayGainValidator:
    def validate(self,f):
        tf = f.tag.user_text_frames
        return tf.get(u"replaygain_album_gain") != None and tf.get(u"replaygain_album_peak") != None and tf.get(u"replaygain_track_gain") != None and tf.get(u"replaygain_track_peak") != None

    def message(self):
        return "Replay gain tags should exist."

class AlbumArtistValidator:
    def validate(self,f):
        return f.tag.getTextFrame("TPE2") is None or f.tag.getTextFrame("TPE2") != f.tag.artist

    def message(self):
        return "Are you sure you want album artist tags?"

class ExtraTextTagValidator:
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

    def validate(self,f):
        state = True
        for t in self.text_tags:
            if f.tag.getTextFrame(t[0]) is not None:
                if f.tag.getTextFrame(t[0]).lstrip() != '':
                    state = False
                    self.messages.append(t[0] + " (" + t[1]  + ")")
        return state

    def message(self):
        message_string = ', '.join(self.messages)
        self.messages = []
        return "Extra Text Frames: " + message_string

class CustomTextFramesValidator:
    def __init__(self):
        self.extra_frames = []

    def validate(self,f):
        valid_frames = [u'replaygain_album_gain',u'replaygain_album_peak',u'replaygain_track_gain',u'replaygain_track_peak',u'CATALOGNUMBER']
        status = True
        for t in f.tag.user_text_frames:
            if t.description not in valid_frames:
                if t.text.lstrip() != '':
                    status = False
                    self.extra_frames.append(t.description)
        return status

    def message(self):
        message = ', '.join(self.extra_frames)
        self.extra_frames = []
        return "Extra TXXX frames found: " + message
