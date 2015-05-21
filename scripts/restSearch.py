""" Contains functions relating to searching for publications."""
import json
import string

dbCols = {  "Title":"Publications.Title",
            "First Name":"Authors.FirstName",
            "Surname":"Authors.Surname ",
            "Book Title":"Books.BookTitle ",
            "Conference Title":"Conferences.ConferenceTitle ",
            "Publication Title":"Publications.Title ",
            "Journal Title":"Journals.JournalTitle ",
            "Accreditation":"Publications.Accreditation",
            "Initials":"Authors.Initials",
            "Year":"Publications.Year"
            } 

def simpleSearch(self, searchTerm, skip, length, sortBy, sort):
    """Does a simple search on the database entries.

    :param searchTerm: The string term to search the database for.
    :param skip: An integer defining which result to return first: for pagination.
    :param length: An integer defining how many terms to return: for pagination.
    :param sortBy: A database column name to sort the results by.
    :param sort: A string defining whether to sort ascending or descending.

    :return: A stringified json array with objects containing details of publications matching the search-term"""
    query = "SELECT  Publications.* "\
        "FROM Publications JOIN Authors ON Authors.PublicationID=Publications.ID "\
        "WHERE "\
        "Authors.FirstName LIKE ? OR "\
        "Authors.Surname Like ? OR "\
        "Publications.Title LIKE ? "\
        "GROUP BY Publications.Title "+sortDocuments(self,sortBy, sort)+\
        "LIMIT ? OFFSET ? "
    pubs = self._databaseWrapper.query(query, ('%'+searchTerm+'%','%'+searchTerm+'%','%'+searchTerm+'%', length, skip))
    return json.dumps(addAuthors(self,pubs))

def sortDocuments(self, sortBy, sort):
    """ Generates a SQL command to do sorting 

    :param sortBy: A String representing a database column to sort by.
    :param sort: A string which determines whether to sort ascending or decending. """
    validSortBy=["Title", "Category", "Year", "Publisher"]
    validSort=["ASC", "DESC"]
    
    sortString=""
    
    if sortBy in validSortBy and sort in validSort:
        if sortBy!="Title":
            sortString=" ORDER By "+sortBy+" COLLATE NOCASE "+sort+ " ,Title COLLATE NOCASE ASC "
        sortString=" ORDER BY "+sortBy+" COLLATE NOCASE "+sort+" "
        
    return sortString

def getAdvancedSearchFields():
    """ Finds the fields by which an advanced search may be done

    :return: A json array containing all the fields by which an advanced search may be done."""
    fields = []
    for a in dbCols.keys():
        fields.append(a)
    return json.dumps(fields)


def advancedSearch(self, searchTerms, skip, length, sortBy, sort):
    """ Performs an advanced search on the database.
    :param searchTerms: A json array containing json objects with three fields: `field`, `operator` and `value`. 
    
    Valid `field`s may be found by :func:`restSearch.getAdvancedSearchFields` 
    Valid `operator`s are "equals" and "contains".
    Valid `value`s may be any string.
    :param skip: Pagination- start of page.
    :param length: Pagination- amount of results.
    :param sortBy: A string representing a db column to sort the results by.
    :param sort: A tring that determines whether to sort ascending or decenting. 
    
    :return: A json array of objects representing publications and their authors."""
    query = "SELECT Publications.* "\
        "FROM Publications "\
        "LEFT JOIN Authors ON Authors.PublicationID=Publications.ID "\
        "LEFT JOIN BookPublications ON BookPublications.PublicationID=Publications.ID "\
        "LEFT JOIN Books ON Books.ID=Bookpublications.BooksID "\
        "LEFT JOIN ConferencePublicationDetail ON ConferencePublicationDetail.PublicationID=Publications.ID "\
        "LEFT JOIN Conferences ON Conferences.ID=ConferencePublicationDetail.ConferenceID "\
        "LEFT JOIN JournalPublicationDetail ON JournalPublicationDetail.PublicationID=Publications.ID "\
        "LEFT JOIN Journals ON Journals.ID=JournalPublicationDetail.JournalID "\
        "WHERE "
    
    terms = json.loads(searchTerms) 
    terms = updateAdvancedSearchTermsFields(terms, dbCols)
    terms = decorateAdvancedSearchTerms(terms)
    (queryPart, queryValues) = getSQLQueryAndValues(terms)

    query += queryPart
    query += "GROUP BY Publications.Title "
    query += sortDocuments(self,sortBy, sort)
    query += "LIMIT ? OFFSET ? "   
    queryValues.append(length)
    queryValues.append(skip)

    pubs = self._databaseWrapper.query(query, queryValues)
    data = []
    return json.dumps(addAuthors(self,pubs))

def updateAdvancedSearchTermsFields(terms, dbCols):
    """Replaces the `field` term values with the actual database column names

    :param terms: The json search terms. See "func:`restSearch.advancedSearch`
    :param dbCols: A dictionary containing the database columns, indexed by their `field` name."""
    oldEntries = terms;
    for entry in oldEntries:
        entry["field"] = dbCols[entry["field"]] + " "
    return oldEntries

def decorateAdvancedSearchTerms(terms):
    """ Update the `field` term so as to add 'LIKE' or '=' so it may be used in an SQL statement."""
    oldEntries = terms;
    for entry in oldEntries:
        if entry["operator"] == "contains" :
            entry["value"] = "%" + entry["value"] + "%"
        else :
            entry["value"] = entry["value"] 
    return oldEntries

def getSQLQueryAndValues(terms):
    """Decomposes the json array of search terms to an SQL query and a string array of values to be sanitized before they are inserted into the query. See :func:`SqliteWrapper.query` """
    values = []
    query = ""
    for entry in terms:
        if entry["operator"] == "contains" :
            query += entry["field"] + "LIKE ? "
        else:
            query += entry["field"] + "= ? "
        if entry != terms[-1]:
            query += "AND "
        values.append(entry["value"])

    return (query, values)

# to be called with pubs being the result of: "SELECT Publications.* WHERE ..."
def addAuthors(self, pubs):
    """ Adds authors to the SQL result of getting publications.*

    :param pubs: A List of publication details"""
    if pubs == []:
        return "200"
    data = []
    for i in range(0,len(pubs)):
        auths = self._databaseWrapper.query("SELECT * FROM Authors WHERE PublicationID=? ", (str(pubs[i][0]),))
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0], "PublicationID":auths[j][1], "First Name" : auths[j][2], "Surname" : auths[j][3],  "Initials" : auths[j][4]})
        data.append({"PublicationId" : pubs[i][0], "Title" : pubs[i][1], "Category" : pubs[i][2], "Year" : pubs[i][3], "Publisher" :pubs[i][4], "Authors" : auth})
    return data
