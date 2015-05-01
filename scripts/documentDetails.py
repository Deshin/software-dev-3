from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main(id):
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getDocumentDetails(id)

if __name__ == "__main__":
    main("1")