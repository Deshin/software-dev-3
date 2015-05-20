import json

dbCols = {  "Title":"Publications.Title",
            "Author":"Authors.FirstName OR Authors.Surname ",
            "Surname":"Authors.Surname ",
            "Book Title":"Books.BookTitle ",
            "Conference Title":"Conferences.ConferenceTitle ",
            "Publication Title":"Publications.Title ",
            "Journal Title":"Journals.JournalTitle ",
            "Abstract":"BookPublications.Abstract OR ConferencePublicationDetail.Abstract OR JournalPublicationDetail.Abstract " 
            } 

def simpleSearch(self, searchTerm, skip, length, sortBy, sort):
    # searchTerms is a list of strings
    query = "SELECT  Publications.* "\
        "FROM Publications JOIN Authors ON Authors.PublicationID=Publications.ID "\
        "WHERE "\
        "Authors.FirstName LIKE ? OR "\
        "Authors.Surname Like ? OR "\
        "Publications.Title LIKE ? "\
        "GROUP BY Publications.Title "+sortDocuments(self,sortBy, sort)+\
        "LIMIT ? OFFSET ? "
    pubs = self._databaseWrapper.query(query, ('%'+searchTerm+'%','%'+searchTerm+'%','%'+searchTerm+'%', length, skip))
    if pubs == []:
        return "200"
    data = []
    for i in range(0,len(pubs)):
        auths = self._databaseWrapper.query("SELECT * FROM Authors WHERE PublicationID=? ", (str(pubs[i][0]),))
        auth = []
        for j in range(0, len(auths)):
            auth.append({"ID":auths[j][0], "PublicationID":auths[j][1], "First Name" : auths[j][2], "Surname" : auths[j][3],  "Initials" : auths[j][4]})
        data.append({"PublicationId" : pubs[i][0], "Title" : pubs[i][1], "Category" : pubs[i][2], "Year" : pubs[i][3], "Publisher" :pubs[i][4], "Authors" : auth})
    return json.dumps(data)

def sortDocuments(self, sortBy, sort):
    validSortBy=["Title", "Category", "Year", "Publisher"]
    validSort=["ASC", "DESC"]
    
    sortString=""
    
    if sortBy in validSortBy and sort in validSort:
        if sortBy!="Title":
            sortString=" ORDER By "+sortBy+" COLLATE NOCASE "+sort+ " ,Title COLLATE NOCASE ASC "
        sortString=" ORDER BY "+sortBy+" COLLATE NOCASE "+sort+" "
        
    return sortString

def getAdvancedSearchFields():
    fields = []
    for a in dbCols.keys():
        fields.append(a)
    return json.dumps(fields)


def advancedSearch(searchTerms, skip, length, limit, offset):
    query = "SELECT Publications.* "\
        "FROM Publications "\
        "LEFT JOIN Authors ON Authors.PublicationID=Publications.ID "\
        "LEFT JOIN BookPublications ON BookPublications.PublicationID=Publications.ID "\
        "LEFT JOIN ConferencePublicationDetail "\
            "ON ConferencePublicationDetail.PublicationID=Publications.ID "\
        "LEFT JOIN JournalPublicationDetail "\
            "ON JournalPublicationDetail.PublicationID=Publications.ID "
    
    #terms = json.loads(searchTerms) add this back
    terms = splitAdvancedSearchTerms(terms)
    terms = updateAdvancedSearchTermsFields(terms, dbCols)
    terms = decorateAdvancedSearchTerms(terms)
    (queryPart, queryValues) = getSQLQueryAndValues(terms)

    query += queryPart
    query += "GROUP BY Publications.Title "\
      "LIMIT ? OFFSET ? "   
    queryValues.append(limit)
    queryValues.append(offset)

    pubs = self._databaseWrapper.query(query, queryValues)
    result = addAuthors(self, pubs)
    return json.dumps(result)

def splitAdvancedSearchTerms(terms):
    oldEntries = terms
    newEntries = []
    for entry in oldEntries:
        bigValue = entry["value"];
        for p in string.punctuation:
            bigValue = bigValue.replace(p, " ")
        if " " in bigValue:
            values = bigValue.split()
            for smallValue in values:
                if len(smallValue) == 1:
                    newEntries.append({ "field": entry["field"], 
                                        "operator": entry["operator"], 
                                        "value": smallValue + " "})
                    newEntries.append({ "field": entry["field"], 
                                        "operator": entry["operator"], 
                                        "value": smallValue + "."})
                else:
                    newEntries.append({ "field": entry["field"], 
                                        "operator": entry["operator"], 
                                        "value": smallValue}) 
            oldEntries.remove(entry);
            oldEntries += newEntries
    return oldEntries

def updateAdvancedSearchTermsFields(terms, dbCols):
    oldEntries = terms;
    for entry in oldEntries:
        entry["field"] = dbCols[entry["field"]] + " "
    return oldEntries

def decorateAdvancedSearchTerms(terms):
    oldEntries = terms;
    for entry in oldEntries:
        if entry["operator"] == "contains" :
            entry["value"] = "LIKE %" + entry["value"] + "% "
        else :
            entry["value"] = "= " + entry["value"] + " "
    return oldEntries

def getSQLQueryAndValues(terms):
    values = []
    query = ""
    for entry in terms:
        query += entry["field"] + "? "
        if entry != terms[-1]:
            query += "OR "
        values.append(entry["value"])

    return (query, values)

# to be called with pubs being the result of: "SELECT Publications.* WHERE ..."
def addAuthors(self, pubs):
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
