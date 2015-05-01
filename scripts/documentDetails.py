from RestApi import RestApi
from SqliteWrapper import SqliteWrapper

def main():
    db = SqliteWrapper()
    rest = RestApi(db)
    result = rest.getDocumentDetails("1")
    print result

if __name__ == "__main__":
    main()