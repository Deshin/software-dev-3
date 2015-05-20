#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(username, password, permission, firstName, surname, initials):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.createAccount(username, password, permission, firstName, surname, initials)
    if result=="404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "No document details were found"
    print "Content-Type: application/json"
    print ""
    print result    

if __name__ == "__main__":
#     form = cgi.FieldStorage()
#     username = form.getvalue("username", None)
#     password = form.getvalue("password", None)
#     permission = form.getvalue("permission", None)
#     firstName=form.getvalue("firstName", None)
#     surname=form.getvalue("surname", None)
#     initials=form.getvalue("initials",None)

    username="bob1234"
    password="obbofecbobofeob"
    permission="registered user"
    firstName="bob"
    surname="bobbington"
    initials="b"
    
    main(username, password, permission, firstName, surname, initials)
