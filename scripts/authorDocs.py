#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi
import json

def main(username):
    db = SqliteWrapper()
    rest = RestApi(db)

    result = rest.getAllAccountDocs(username)
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
    
    main(username)
