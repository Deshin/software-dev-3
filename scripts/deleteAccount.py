#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(username):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.deleteAccount(username)
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
