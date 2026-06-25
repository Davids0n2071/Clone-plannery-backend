import firebase_admin
from firebase_admin import credentials, firestore
import os

# Inicializa Firebase solo una vez cuando arranca el servidor
def init_firebase():
    if not firebase_admin._apps:  # evita inicializarlo dos veces
        cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccount.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_db():
    """Devuelve el cliente de Firestore listo para usar."""
    return firestore.client()