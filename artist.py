"""
This code defines a class which, given a string representing a given ARTIST,
scrapes data for that artist from internet databases, and thereby adds data
to its various fields.
"""

# Standard imports.
import os
from numpy import mean, std
from urllib.parse import quote_plus

# Non-standard imports.
from progressbar import progressbar

# Local imports.
from db_manager import DBManager, DEFAULT_PATH_TO_DB
from track import Track
from xml_from_url import get_xml_from_url

# Local constants.
MUSIC_BRAINZ_STEM = "https://musicbrainz.org/ws/2/"
ARTIST_LIST_TAG = "{http://musicbrainz.org/ns/mmd-2.0#}artist-list"
ARTIST_TAG = "{http://musicbrainz.org/ns/mmd-2.0#}artist"
RECORDING_LIST_TAG = "{http://musicbrainz.org/ns/mmd-2.0#}recording-list"
RECORDING_TAG = "{http://musicbrainz.org/ns/mmd-2.0#}recording"
TITLE_TAG = "{http://musicbrainz.org/ns/mmd-2.0#}title"
MAX_LIMIT = 100

##############
# MAIN CLASS #
##############

class Artist:
    """ The class in question. """
    def __init__(self, human_readable_name):
        self.name = human_readable_name
        self.mbid = self.get_mbid() # MBID = Music Brainz ID
        self.set_of_tracks = None
        self.list_of_track_objects = None
        self.list_of_word_counts = None
        self.mean_word_count = None
        self.std_word_count = None
        self.mean_word_length = None
        self.attempt_to_fill_from_local()

    def attempt_to_fill_from_local(self):
        """ Fill the remaining fields of this object from the local
        database, otherwise consult online resources. """
        dbm = DBManager()
        artist_dict = dbm.get_artist_dict(self.mbid)
        if artist_dict:
            self.mean_word_count = artist_dict["mean_word_count"]
            self.std_word_count = artist_dict["std_word_count"]
            self.mean_word_length = artist_dict["mean_word_length"]
        else:
            self.fill_from_remote()

    def fill_from_remote(self):
        """ Fill the fields of this object from online resources. """
        if not self.mbid:
            return
        self.set_of_tracks = self.get_set_of_tracks()
        self.list_of_track_objects = self.get_list_of_track_objects()
        self.list_of_word_counts = self.get_list_of_word_counts()
        self.mean_word_count = self.get_mean_word_count()
        self.std_word_count = self.get_std_word_count()
        self.mean_word_length = self.get_mean_word_length()

    def get_mbid(self):
        """ Nothing fancy here: just return the first match. """
        print("Fetching MusicBrainz ID code...")
        xml_obj = get_xml_from_url(MUSIC_BRAINZ_STEM+"artist?query="+
                                   "\""+quote_plus(self.name)+"\"")
        if not xml_obj:
            return False
        for artist_list in xml_obj.findall(ARTIST_LIST_TAG):
            for artist in artist_list.findall(ARTIST_TAG):
                result = artist.attrib["id"]
                return result
        return False

    def get_set_of_tracks(self):
        """ Build a set from the names of recordings for this artist. """
        print("Fetching list of tracks...")
        result = set()
        offset = 0
        recordings = get_recordings(self.mbid, offset)
        while len(recordings) > 0:
            for recording in recordings:
                result.add(recording)
            offset = offset+MAX_LIMIT
            recordings = get_recordings(self.mbid, offset)
        return result

    def get_list_of_track_objects(self):
        """ Ronseal. """
        result = []
        list_of_tracks = list(self.set_of_tracks)
        print("Gathering data for all tracks by "+self.name+"...")
        for track_title in progressbar(list_of_tracks):
            track = Track(self.name, track_title)
            result.append(track)
        return result

    def get_list_of_word_counts(self):
        """ Get a list of word counts for all the tracks on the list. """
        result = []
        for track in self.list_of_track_objects:
            if track.word_count:
                result.append(track.word_count)
        return result

    def get_mean_word_count(self):
        """ Ronseal. """
        if len(self.list_of_word_counts) == 0:
            return False
        result = mean(self.list_of_word_counts)
        return result

    def get_std_word_count(self):
        """ Ronseal. """
        if len(self.list_of_word_counts) == 0:
            return False
        result = std(self.list_of_word_counts)
        return result

    def get_mean_word_length(self):
        """ Get a list of the mean word lengths for each track. """
        list_of_mean_word_lengths = []
        for track in self.list_of_track_objects:
            if track.mean_word_length:
                list_of_mean_word_lengths.append(track.mean_word_length)
        result = mean(list_of_mean_word_lengths)
        return result

    def save_to_database(self):
        """ Save the fields of this object to the database. """
        dbm = DBManager()
        if dbm.get_artist_dict(self.mbid):
            return
        dbm.add_artist_record(self)

####################
# HELPER FUNCTIONS #
####################

def get_recordings(mbid_of_artist, offset):
    """ Get a list of the names of recordings for a given artist and offset,
    which is a means of pagination. """
    if not mbid_of_artist:
        return
    result = []
    xml_obj = get_xml_from_url(MUSIC_BRAINZ_STEM+
                               "recording?artist="+mbid_of_artist+
                               "&limit="+str(MAX_LIMIT)+
                               "&offset="+str(offset))
    for recording_list in xml_obj.findall(RECORDING_LIST_TAG):
        for recording in recording_list.findall(RECORDING_TAG):
            for item in recording.findall(TITLE_TAG):
                result.append(item.text)
    return result

###########
# TESTING #
###########

def test():
    """ Run the unit tests. """
    os.system("rm -i "+DEFAULT_PATH_TO_DB)
    arnold_dorsey = Artist("Engelbert Humperdinck")
    assert arnold_dorsey.mbid == "62c28bc0-f696-4c50-8e54-5f8e9120bdb8"
    travis = Artist("Travis")
    assert travis.mbid == "22a40b75-affc-4e69-8884-266d087e4751"
    small_t_travis = Artist("travis")
    assert small_t_travis.mbid == travis.mbid
    gobbledygook = Artist("dsklnvsldkjfnv")
    assert not gobbledygook.mbid
    print("Tests passed!")

def demo():
    """ Run a demonstration. """
    os.system("rm -i "+DEFAULT_PATH_TO_DB)
    travis = Artist("Travis")
    travis.save_to_database()

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    #test()
    demo()

if __name__ == "__main__":
    run()
