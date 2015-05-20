#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi
import json

def main(username, password, permission, firstName, surname, initials):
    db = SqliteWrapper()
    rest = RestApi(db)

    result = rest.createAccount(username, password, permission, firstName, surname, initials)
    if result=="400":
        print "Status:400"
        print "Content-Type: text/html"
        print ""
        print "Account couldnt be added"
    elif result=="409":
        print "Status:409"
        print"Content-Type: text/html"
        print ""
        print "Username is not unique"
    else:
        print "Content-Type: application/json"
        print ""
        print result    

if __name__ == "__main__":
    form = cgi.FieldStorage()
    username = form.getvalue("username", None)
    password = form.getvalue("password", None)
    permission = "registered"
    firstName=form.getvalue("firstname", None)
    surname=form.getvalue("surname", None)
    initials=form.getvalue("initials",None)
    
    main(username, password, permission, firstName, surname, initials)
