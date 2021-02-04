"""
This code defines a class which holds the properties of a given track.
"""

# Standard imports.
from urllib.parse import quote_plus

# Local imports.
from json_from_url import get_json_from_url

# Local constants.
LYRICS_OVH_STEM = "https://api.lyrics.ovh/v1/"

##############
# MAIN CLASS #
##############

class Track:
    """ The class in question. """
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.words = self.get_words()
        self.word_count = self.get_word_count()
        self.mean_word_length = self.get_mean_word_length()

    def get_words(self):
        """ Get the words to this track from lyrics.ovh. """
        json_dict = get_json_from_url(LYRICS_OVH_STEM+
                                      quote_plus(self.artist)+"/"+
                                      quote_plus(self.title))
        if not json_dict:
            return False
        result = json_dict["lyrics"]
        if result == "":
            return False
        return result

    def get_word_count(self):
        """ Count the number of words in this track. """
        if not self.words:
            return False
        redacted_words = purge_punctuation_etc(self.words)
        word_list = redacted_words.split(" ")
        result = len(word_list)
        return result

    def get_mean_word_length(self):
        """ Get the mean length of the words in this track. """
        if not self.words:
            return False
        redacted_words = purge_punctuation_etc(self.words)
        redacted_words = redacted_words.replace(" ", "")
        total_letters = len(redacted_words)
        result = total_letters/self.word_count
        return result

####################
# HELPER FUNCTIONS #
####################

def purge_punctuation_etc(input_string):
    """ Purge capital letters, new line characters and punctuation from a
    given string. """
    result = input_string.lower()
    result = result.replace("\n", "")
    list_of_non_letters = []
    for character in result:
        if (ord(character) < ord('a')) or (ord(character) > ord('z')):
            if character != ' ':
                list_of_non_letters.append(character)
    for non_letter in list_of_non_letters:
        result = result.replace(non_letter, "")
    while "  " in result:
        result = result.replace("  ", " ")
    return result

###########
# TESTING #
###########

def test():
    """ Run the unit tests. """
    driftwood = Track("Travis", "Driftwood")
    assert driftwood.word_count == 234
    prm = Track("Engelbert Humperdinck", "Please Release Me")
    assert prm.word_count == 95
    gobbledygook = Track("Travis", "dvvkdkvergfjnv")
    assert not gobbledygook.word_count
    print("Tests passed!")

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    test()

if __name__ == "__main__":
    run()
