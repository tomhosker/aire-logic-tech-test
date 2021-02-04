"""
This code defines a small custom library of functions for getting XML, as a
string, from a URL, and then converting that string into an XML object.
"""

# Standard imports.
import time
import json
from urllib.error import HTTPError
from urllib.request import urlopen

# Local imports.
from xml_from_url import append_to_http_error_log

# Local constants.
ENCODING = "utf-8"

#############
# FUNCTIONS #
#############

def get_json_from_url(url):
    """ Ronseal. """
    try:
        response = urlopen(url)
        response_bytes = response.read()
        response_string = response_bytes.decode(ENCODING)
        response.close()
    except HTTPError:
        append_to_http_error_log(url)
        return False
    result = json.loads(response_string)
    time.sleep(1) # This stops us from getting banned!
    return result

###########
# TESTING #
###########

def demo():
    """ Run a demonstration. """
    json_dict = get_json_from_url(
                    "https://api.lyrics.ovh/v1/Travis/Driftwood")
    print(json_dict["lyrics"])

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    demo()

if __name__ == "__main__":
    run()
