
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import json

def initialize_firebase(firebase_config):
    """
    Initializes the Firebase app using the service account.
    """
    if not firebase_admin._apps:
        # Use the firebase_config dictionary directly
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)

def get_firestore_db():
    """
    Returns the Firestore database client.
    """
    return firestore.client()

def initialize_pyrebase(firebase_config):
    """
    Initializes Pyrebase for authentication.
    """
    # Use the firebase_config dictionary directly
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.auth()
