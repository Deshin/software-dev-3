#!/usr/bin/env python
"""RESTful endpoint for retrieving the possible advanced search fields"""

import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main():
    """ Prints the result of :func:`restSearch.getAdvancedSearchFields` """
    db = SqliteWrapper()
    rest = RestApi(db)
    print "Content-Type: application/json"
    print
    print ""
    print rest.getAdvancedSearchFields()

if __name__ == "__main__":
    main()
