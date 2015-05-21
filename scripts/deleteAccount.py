#!/usr/bin/env python
"""RESTful endpoint for deleting a user-account"""

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi

def main(username):
    """Prints the output of :func:`restAccounts.deleteAccount`, thus, the result of attempting to delete a user-account."""
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.deleteAccount(username)
    if result=="400":
        print "Status:400"
        print "Content-Type: text/html"
        print ""
        print "Account couldnt be deleted"
    elif result=="404":
        print "Status:404"
        print "Content-Type: text/html"
        print ""
        print "Account does not exists"
    elif result=="403":
        print "Status:403"
        print "Content-Type: text/html"
        print ""
        print "Admin account cannot be deleted!"
    else:
        print "Content-Type: text/html"
        print ""
        print result

if __name__ == "__main__":
    form = cgi.FieldStorage()
    username = form.getvalue("username", None)
    main(username)
