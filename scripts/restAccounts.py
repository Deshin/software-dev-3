#!/usr/bin/env python

def createAccount(self,username, password, permission, firstName, surname, initials):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount!=[]:
            return "409"
        else:
            self._databaseWrapper.query("INSERT INTO Users(Username, Permission, Password, FirstName, Surname, Initials) VALUES(?,?,?,?,?,?)",[username,permission,password,firstName,surname,initials])
            self._databaseWrapper.commit()
            return "Added!"
    except:
        return"400"
    
def deleteAccount(self,username):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "404"
        else:
            self._databaseWrapper.query("DELETE FROM Users WHERE Username=?",[username])
            self._databaseWrapper.commit()
            return "Account Deleted"
    except:
        return "400"
    
def getAllAccountDocs(self,username,skip, length, sortBy, sort):
    try:
        existingAccount=self._databaseWrapper.query("SELECT * FROM Users WHERE Username=?",[username])
        if existingAccount==[]:
            return "409"
        else:
            userData={"username":existingAccount[0][1],"firstname":existingAccount[0][4],"surname":existingAccount[0][5], "initials":existingAccount[0][6]}
            authorPubs=self.databaseWrapper.query("SELECT * FROM Authors WHERE FirstName=? AND Surname=? AND Initials=?",[userData["firstname"],userData["surname"],userData["initials"]])
            documentDetails=[]
            for item in authorPubs:
                pubs = self._databaseWrapper.query("SELECT * FROM Publications WHERE ID=? "+self.sortDocuments(sortBy, sort) + " LIMIT ? OFFSET ?", (item[1],length, skip))
                if pubs == []:
                    return "404"
                
                data = []
                for i in range(0,len(pubs)):
                    auth = self.getAuthors(pubs[i][0])
                    
                    data.append({"PublicationId" : pubs[i][0], 
                                 "Title" : pubs[i][1], 
                                 "Category" : pubs[i][2], 
                                 "Year" : pubs[i][3], 
                                 "Publisher" :pubs[i][4],
                                 "Authors" : auth})
                    documentDetails.append(data)
                result={"userDetails":userData, "documentDetails":documentDetails}
                return result
    except:
        return"404"

        