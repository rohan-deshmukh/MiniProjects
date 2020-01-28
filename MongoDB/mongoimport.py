import pandas as pd
from pymongo import MongoClient
import json

def mongoimport(json_path, db_name, coll_name, db_url='localhost', db_port=27017)
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    payload = json.loads(json_path)
    coll.remove()
    coll.insert(payload)
    return coll.count()


def main():
    mongoimport()
