"""
This code defines a small custom library of functions for getting XML, as a
string, from a URL, and then converting that string into an XML object.
"""

# Standard imports.
import time
import xml.etree.ElementTree as eltree
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlopen
from xml.dom.minidom import parseString

# Local constants.
ENCODING = "utf-8"
PATH_TO_HTTP_ERROR_LOG = "http_errors.log"

#############
# FUNCTIONS #
#############

def append_to_http_error_log(url):
    """ Ronseal. """
    string_to_write = str(datetime.now())+" | Unable to open URL: "+url+"\n"
    with open(PATH_TO_HTTP_ERROR_LOG, "a") as log_file:
        log_file.write(string_to_write)

def get_xml_from_url(url):
    """ Ronseal. """
    try:
        response = urlopen(url)
        response_bytes = response.read()
        response_string = response_bytes.decode(ENCODING)
        response.close()
    except HTTPError:
        append_to_http_error_log(url)
        return False
    result = eltree.fromstring(response_string)
    time.sleep(1) # This stops us from getting banned!
    return result

def pretty_print_xml_from_url(url):
    """ A debugging function. """
    response = urlopen(url)
    response_bytes = response.read()
    response_string = response_bytes.decode(ENCODING)
    response.close()
    xml_obj = parseString(response_string)
    pretty_string = xml_obj.toprettyxml()
    time.sleep(1) # This stops us from getting banned!
    print(pretty_string)

###########
# TESTING #
###########

def demo():
    """ Run a demonstration. """
    pretty_print_xml_from_url(
        "https://musicbrainz.org/ws/2/"+
        "artist?query=\"engelbert%20humperdinck\"")

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    demo()

if __name__ == "__main__":
    run()
