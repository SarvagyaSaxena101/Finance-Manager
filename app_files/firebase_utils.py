
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import json

def initialize_firebase():
    """
    Initializes the Firebase app using the service account.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("app_files/firebase_config.json")
        firebase_admin.initialize_app(cred)

def get_firestore_db():
    """
    Returns the Firestore database client.
    """
    return firestore.client()

def initialize_pyrebase():
    """
    Initializes Pyrebase for authentication.
    """
    with open("app_files/firebase_config.json") as f:
        config = json.load(f)

    firebase = pyrebase.initialize_app(config)
    return firebase.auth()
