from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

def get_mongo_client():
    """Kreira i vraća MongoDB klijent"""
    try:
        client = MongoClient(MONGO_URI)
        # Testiraj vezu
        client.admin.command('ping')
        print("Uspješno spojen na MongoDB!")
        return client
    except ConnectionFailure as e:
        print(f"Greška pri spajanju na MongoDB: {e}")
        return None

def get_mongo_collection():
    """Dohvaća kolekciju iz MongoDB baze"""
    try:
        client = get_mongo_client()
        if client is not None:
            db = client[MONGO_DB_NAME]
            collection = db[MONGO_COLLECTION_NAME]
            return collection
        return None
    except Exception as e:
        print(f"Greška pri dohvaćanju kolekcije: {e}")
        return None

def insert_patients_data(patients_data):
    """Ubacuje podatke o pacijentima u MongoDB"""
    try:
        collection = get_mongo_collection()
        if collection is not None and patients_data:
            # Izbriši postojeće podatke za iste kohorte (opcionalno)
            cohorts = list(set([patient['cancer_cohort'] for patient in patients_data]))
            collection.delete_many({'cancer_cohort': {'$in': cohorts}})
            
            # Ubaci nove podatke
            result = collection.insert_many(patients_data)
            print(f"U MongoDB ubaceno {len(result.inserted_ids)} dokumenata.")
            return True
        return False
    except OperationFailure as e:
        print(f"Greška pri ubacivanju u MongoDB: {e}")
        return False

def get_patients_by_cohort(cohort_name):
    """Dohvaća sve pacijente za određenu kohortu"""
    try:
        collection = get_mongo_collection()
        if collection is not None:
            patients = list(collection.find({'cancer_cohort': cohort_name}, {'_id': 0}))
            return patients
        return []
    except Exception as e:
        print(f"Greška pri dohvaćanju pacijenata po kohorti: {e}")
        return []

def get_patient_by_id(patient_id):
    """Dohvaća podatke za određenog pacijenta"""
    try:
        collection = get_mongo_collection()
        if collection is not None:
            patient = collection.find_one({'patient_id': patient_id}, {'_id': 0})
            return patient
        return None
    except Exception as e:
        print(f"Greška pri dohvaćanju pacijenta: {e}")
        return None