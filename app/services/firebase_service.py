import firebase_admin
from firebase_admin import credentials, firestore
import os
import json


def init_firebase():
    if not firebase_admin._apps:
        firebase_credentials = os.getenv("FIREBASE_CREDENTIALS", "serviceAccount.json")

        # Si empieza con { es un JSON completo (caso Render)
        # Si no, es una ruta de archivo (caso local)
        if firebase_credentials.strip().startswith("{"):
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate(firebase_credentials)

        firebase_admin.initialize_app(cred)


def get_db():
    return firestore.client()