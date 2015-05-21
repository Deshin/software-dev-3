#!/usr/bin/env python
"""RESTful endpoint for finding requirements for csv files"""

import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main():
    """ Prints the result of :func: `restInsertion.getCSVFormats` """

    db = SqliteWrapper()
    rest = RestApi(db)
    print "Content-Type: application/json"
    print
    print ""
    print rest.getCSVFormats()

if __name__ == "__main__":
    main()
