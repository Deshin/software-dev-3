#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getAllDocuments()
    if result == "404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "404 - No documents were found."
    else:
        print "Content-Type: application/json"
        print ""
        print result

if __name__ == "__main__":
    main()
