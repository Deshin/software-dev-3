#!/usr/bin/env python

import json

def insertDocument(self, details):
    #try:
    if details["Category"].lower().startswith("conference"):
        insertConferencePaper(self,details)
        
    elif details["Category"].lower().startswith("journal"):
        insertJournalPaper(self,details)
        
    elif details["Category"].lower().startswith("book"):
        insertBookSection(self,details)
    return 200
        
    #except:
    #    return "404"
        
def insertConferencePaper(self,details):
    existingConference=self._databaseWrapper.query("SELECT * FROM Conferences WHERE ConferenceTitle="+details["ConferenceTitle"])
    print existingConference
    
def insertJournalPaper(self,details):
    print details
    
def insertBookSection(self,details):
    print details
    