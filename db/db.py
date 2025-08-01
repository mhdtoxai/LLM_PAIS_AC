import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Verificar que la URL esté definida
if not os.getenv('MONGODB_URL'):
    raise ValueError("MONGODB_URL no encontrado. Por favor, revisa tu archivo .env.")

# Verificar que la base de datos esté definida
if not os.getenv('DATABASE'):
    raise ValueError("DATABASE no encontrado. Por favor, revisa tu archivo .env.")

# Verificar que la colección esté definida
if not os.getenv('MONGODB_COLLECTION'):
    raise ValueError("MONGODB_COLLECTION no encontrado. Por favor, revisa tu archivo .env.")

# Conectar al cliente de MongoDB
client = MongoClient(os.getenv('MONGODB_URL'))

# Acceder a la base de datos desde la variable de entorno
db = client[os.getenv('DATABASE')]

# Acceder a la colección desde la variable de entorno
collection = db[os.getenv('MONGODB_COLLECTION')]

# Función para obtener una colección específica
def get_collection(collection_name: str):
    return db[collection_name]
