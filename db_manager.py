"""
This code defines a class which handles the reading from, and writing to,
this project's database.
"""

# Standard imports.
import os
import sqlite3

# Local constants.
DEFAULT_PATH_TO_DB = "data.db"
DEFAULT_CREATE_DROP_SCRIPT = (
    "DROP TABLE IF EXISTS Artist",
    ("CREATE TABLE Artist ( "+
         "mbid TEXT, "+
         "human_readable_name TEXT NOT NULL, "+
         "mean_word_count INTEGER, "+
         "std_word_count INTEGER, "+
         "mean_word_length INTEGER, "+
         "PRIMARY KEY(mbid) "+
     ");")
)

##############
# MAIN CLASS #
##############

class DBManager:
    """ The class in question. """
    def __init__(self, path_to_db=DEFAULT_PATH_TO_DB):
        self.path_to_db = path_to_db
        self.connection = None
        self.cursor = None
        self.initialise_as_necessary()

    def establish_connection(self):
        """ Ronseal. """
        self.connection = sqlite3.connect(self.path_to_db)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """ Ronseal. """
        self.connection.close()
        self.connection = None
        self.cursor = None

    def execute_write(self, query, params=None):
        """ Execute a query which alters the database. """
        self.establish_connection()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()

    def execute_fetch(self, query, params=None):
        """ Execute a query which fetches data from the database. """
        self.establish_connection()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    def create_drop(self, create_drop_script=DEFAULT_CREATE_DROP_SCRIPT):
        """ Execute the database's create-drop script. """
        for query in create_drop_script:
            self.execute_write(query)

    def initialise_as_necessary(self):
        """ Create the database from scratch, if it doesn't yet exist. """
        if os.path.exists(self.path_to_db):
            return
        os.system("touch "+self.path_to_db)
        self.create_drop()

    def add_artist_record(self, artist):
        """ Add a record for a given artist using an instance of the Artist
        class. """
        query = ("INSERT INTO Artist "+
                     "(mbid, human_readable_name, mean_word_count, "+
                      "std_word_count, mean_word_length) "+
                 "VALUES (?, ?, ?, ?, ?)")
        mbid = artist.mbid
        human_readable_name = artist.name
        if artist.mean_word_count:
            mean_word_count = artist.mean_word_count
        else:
            mean_word_count = -1
        if artist.std_word_count:
            std_word_count = artist.std_word_count
        else:
            std_word_count = -1
        if artist.mean_word_length:
            mean_word_length = artist.mean_word_length
        else:
            mean_word_length = -1
        params = (mbid, human_readable_name, mean_word_count,
                  std_word_count, mean_word_length)
        self.execute_write(query, params=params)

    def get_artist_dict(self, mbid):
        """ Get a dictionary of a given artist's data. """
        query = "SELECT * FROM Artist WHERE mbid = ?;"
        extract = self.execute_fetch(query, params=(mbid,))
        if len(extract) == 0:
            return False
        result = extract[0]
        return result

####################
# HELPER FUNCTIONS #
####################

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
