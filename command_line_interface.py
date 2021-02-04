"""
This code defines a class which holds the command line interface for this
program.
"""

# Local imports.
from artist import Artist

##############
# MAIN CLASS #
##############

class CommandLineInterface:
    """ The class in question. """
    def __init__(self):
        self.artist_name = None
        self.artist_obj = None

    def print_intro(self):
        """ Ronseal. """
        print("Welcome. This is a program which compiles statistics for "+
              "the words to the songs of musical artists.")

    def get_artist_name(self):
        """ Get a string from the user. """
        print("Please enter the name of the artist you'd like to know "+
              "more about.")
        candidate_artist_name = input()
        while candidate_artist_name == "":
            print("I'm going to need a bit more than that!")
            candidate_artist_name = input()
        print("You entered: "+candidate_artist_name)
        self.artist_name = candidate_artist_name

    def build_artist_obj(self):
        """ Go through the time-consuming process of building an instance
        of the Artist class. """
        self.artist_obj = Artist(self.artist_name)

    def print_statistical_data(self):
        """ Print the statistical findings to the screen. """
        if self.artist_obj.mbid:
            print("Statistics for all tracks by "+self.artist_name+":")
            print("    Mean word count: "+
                  str(self.artist_obj.mean_word_count))
            print("    Standard deviation of word counts: "+
                  str(self.artist_obj.std_word_count))
            print("    Mean word length: "+
                  str(self.artist_obj.mean_word_length))
        else:
            print("Sorry, but I couldn't find any data for: "+
                  self.artist_name)

    def offer_to_save(self):
        """ Give the user the opportunity to save these results to the
        database. """
        if not self.artist_obj.mbid:
            return
        print("Would you like to save these results to the local "+
              "database? (y/n)")
        response = input()
        if response == "y":
            self.artist_obj.save_to_database()
            print("Saved.")

    def print_outro(self):
        """ Ronseal. """
        print("Bye!")

    def run_me(self):
        """ Run the interface. """
        self.print_intro()
        self.get_artist_name()
        self.build_artist_obj()
        self.print_statistical_data()
        self.offer_to_save()
        self.print_outro()

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    cli = CommandLineInterface()
    cli.run_me()

if __name__ == "__main__":
    run()
