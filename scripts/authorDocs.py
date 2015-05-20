#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi
import json

def main(username,skip, length, sortBy, sort):
    db = SqliteWrapper()
    rest = RestApi(db)

    result = rest.getAllAccountDocs(username,skip, length, sortBy, sort)
    if result=="400":
        print "Status:400"
        print "Content-Type: text/html"
        print ""
        print "Account couldnt be added"
    else:
        print "Content-Type: application/json"
        print ""
        print result

if __name__ == "__main__":
    form = cgi.FieldStorage()
    username = form.getvalue("username", None)
    skip = form.getvalue("skip", None)
    length = form.getvalue("length", None)
    sortBy=form.getvalue("sortBy", None)
    sort=form.getvalue("sort", None)
    
    main(username,skip, length, sortBy, sort)
