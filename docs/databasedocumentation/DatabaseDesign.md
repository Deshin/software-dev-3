##Publications
ID: primary key, auto-increment, not null, integer, unique
Title: not null, varchar
Category: not null, varchar
Year: not null,integer
Publisher: not null, varchar
TableOfContentsPath: not null, varchar
ScanPath: not null, varchar
Accreditation: not null, varchar

##Authors
ID: primary key, auto-increment, not null, integer, unique
PublicationID: foreign key, not null, integer
FirstName: not null, varchar
Surname: not null, varchar
Initials: not null, varchar

##BookPublications
ID: primary key, auto-increment, not null, integer, unique
PublicationID: foreign key, not null, integer
Chapter:not null, int
Abstract: varchar
BooksID: foreign key, integer

##BooksID
ID: primary key, auto-increment, not null, integer, unique
ISBN: not null, integer
BookTitle: not null, varchar
Type: not null, varchar

##ConferencePublicationDetail
ID: primary key, auto-increment, not null, integer, unique
PublicationID: foreign key, not null, integer
ConferenceID: foreign key, not null, integer
Abstract: not null, varchar
MotivationForAccreditation: not null, varchar
PeerReviewProcess: not null, varchar

##Conferences
ID: primary key, auto-increment, not null, integer, unique
ConferenceTitle: not null, varchar
year: not null, integer
Country: not null, integer

##JournalPublication
ID: primary key, auto-increment, not null, integer, unique
PublicationID: foreign key, not null, integer
JournalID: foreign key, not null, integer
volume: integer
issue: integer
Abstract: not null, varchar

##Journals
ID: primary key, auto-increment, not null, integer, unique
JournalTitle: not null, varchar
ISSN: not null, integer,unique
HIndex: integer
Type: not null, varchar

##PeerReviewDocumentation
ID: primary key, auto-increment, not null, integer, unique
PublicationID: foreign key, not null, integer
PathToFile: not null, varchar
DocumentTitle: not null, varchar

##Users
ID: primary key, auto-increment, not null, integer, unique
Username: not null, varchar, unique
Permission: not null, varchar
Password: not null, varchar
FirstName: not null, string
Surname: not null, string
Initials: not null, varchar

