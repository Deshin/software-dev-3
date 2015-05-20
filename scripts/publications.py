#!/usr/bin/env python
import json
import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(simpleSearch, advancedSearch, skip, length, sortBy, sort):
    db = SqliteWrapper()
    rest = RestApi(db)
    if simpleSearch == None and advancedSearch == None:
        result = rest.getAllDocuments(skip, length, sortBy, sort)
    elif simpleSearch != None:
        result = rest.simpleSearch(simpleSearch, skip, length, sortBy, sort)
    elif advancedSearch != None:
        result = rest.advancedSearch(advancedSearch, skip, length, sortBy, sort)
    print "Content-Type: application/json"
    print
    print ""
    print result

if __name__ == "__main__":
    form = cgi.FieldStorage()
    simpleSearch = form.getvalue("simpleSearch", None)
    advancedSearch = form.getvalue("advancedSearch", None)
    skip = form.getvalue("skip", None)
    length = form.getvalue("length", None)
    sortBy=form.getvalue("sortBy", None)
    sort=form.getvalue("sort", None)
    main(simpleSearch, advancedSearch, skip, length, sortBy, sort)    

#if __name__ == "__main__":
#    advS = [{"field":"Accreditation","value":"Not Yet Accredited","operator":"equals"}]
#    main(None, json.dumps(advS), 0, 20, None, None)

