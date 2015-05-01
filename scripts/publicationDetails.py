#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(id):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getDocumentDetails(id)
    print "Content-Type: application/json"
    print ""
    print result    

if __name__ == "__main__":
    main("1")
