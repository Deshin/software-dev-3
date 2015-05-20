#!/usr/bin/env python
import cgi
from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def getAdvancedSearchFields():
    db = SqliteWrapper()
    rest = RestApi(db)
    print rest.getAdvancedSearchFields()


if __name__ == "__main__":
    advancedSearchFields()
