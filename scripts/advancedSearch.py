#!/usr/bin/env python

import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(self, searchTerms):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.advancedSearch(self, searchTerms)

    print "Content-Type: application/json"
    print
    print ""
    print result

if __name__ == "__main__":
    form = cgi.FieldStorage()
    simpleSearch = form.getvalue("advancedSearch", None)
    main(advancedSearch)    



