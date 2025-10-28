
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import json

def initialize_firebase(firebase_config):
    """
    Initializes the Firebase app using the service account.
    """
    if not firebase_admin._apps:
        # Extract only the service account credentials for firebase_admin.credentials.Certificate
        service_account_info = {
            "type": firebase_config["type"],
            "project_id": firebase_config["project_id"],
            "private_key_id": firebase_config["private_key_id"],
            "private_key": firebase_config["private_key"],
            "client_email": firebase_config["client_email"],
            "client_id": firebase_config["client_id"],
            "auth_uri": firebase_config["auth_uri"],
            "token_uri": firebase_config["token_uri"],
            "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebase_config["client_x509_cert_url"],
            "universe_domain": firebase_config["universe_domain"],
        }
        cred = credentials.Certificate(service_account_info)
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
