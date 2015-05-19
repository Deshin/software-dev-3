#!/usr/bin/env python

import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(simpleSearch, skip, length):
    db = SqliteWrapper()
    rest = RestApi(db)
    if simpleSearch == None:
        result = rest.getAllDocuments(skip, length)
    else:
        result = rest.simpleSearch(simpleSearch, skip, length)
    if result == "404":
        print "Status:404"
        print "Content-Type: text/html"
        print
        print ""
        print "404 - No documents were found."
    else:
        print "Content-Type: application/json"
        print
        print ""
        print result

if __name__ == "__main__":
    form = cgi.FieldStorage()
    simpleSearch = form.getvalue("simpleSearch", None)
    skip = form.getvalue("skip", None)
    length = form.getvalue("length", None)
    main(simpleSearch, skip, length)    
