#!/usr/bin/env python

import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(username,hash):
    db = SqliteWrapper()
    rest = RestApi(db)
    result=rest.getLoginCredentials(username)
    if result=="401":
        result="401"
    else:
        if result[0]!=hash:
            result="401"
    if result == "401":
        print "Status:401"
        print "Content-Type: text/html"
        print
        print ""
        print "401 - Could not login."
    else:
        print "Content-Type: application/json"
        print
        print ""
        print result[1]
        
        
if __name__ == "__main__":
    form = cgi.FieldStorage()
    username = form.getvalue("username", None)
    hash = form.getvalue("hash", None)
    main(username,hash)  