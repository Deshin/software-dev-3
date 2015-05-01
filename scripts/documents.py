#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getAllDocuments()
    print "Content-Type: application/json"
    print result

if __name__ == "__main__":
    main()
