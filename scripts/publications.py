#!/usr/bin/env python
"""RESTful endpoint for finding or searching for publications"""
import json
import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(simpleSearch, advancedSearch, skip, length, sortBy, sort):
    """Runs :func:`restRetrieval.getAllDocuments`,
    see :func:`restSearch.simpleSearch` or
    see :func:`restSearch.getAdvancedSearchFields` depending on the parameters, and prints the resulting stringified json object
    
    :param simpleSearch: String of search-terms for simpleSearch
    :param advancedSearch: Stringified json array with objects for advancedSearch.
    :param skip: An integer number defining which is the first result to be returned.
    :param length: An integer defining how many terms must be returned.
    :param sortBy: A string identifying the column to sort by.
    :param sort: A string defining whether to sort ascending or descending."""

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

