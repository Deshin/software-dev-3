#!/usr/bin/env python

from RestApi import RestApi
from SqliteWrapper import SqliteWrapper
import cgi
import string

def main(search):
    search = search.translate(string.maketrans("",""), string.punctuation)
    searchTerms = search.split()

    db = SqliteWrapper()
    rest = RestApi(db)

    return rest.simpleSearch(searchTerms[0])


if __name__ == "__main__":
    form = cgi.Fieldstorage()
    search = form.getValue("simpleSearch")
    main(search)

#if __name__ == "__main__":
    #print main("Sarah")
