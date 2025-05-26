import pymongo
from dotenv import load_dotenv
import os

#Load dotenv
load_dotenv()

def spin_up_db():
    """Make sure that the patients database and collection has been created"""
    mongo_uri = os.getenv("MONGO_URI")
    mongo_client = pymongo.MongoClient(mongo_uri)

    patient_db = mongo_client["patient_database"]

    return patient_db

def load_patients_mongodb(patient_db, data):
    """Make sure the patients collection is empty and then insert patients data"""

    patient_collection = patient_db["patients_collection"]

    patient_collection.drop()

    if not patient_collection.count_documents({}):
        patient_collection.insert_many(data)

    return patient_collection

def retrieve_from_mongodb(patient_collection, query=None):
    """Retrieve data from mongodb"""

    if query is None:
        query = {}

    documents = patient_collection.find(query)

    return list(documents)
