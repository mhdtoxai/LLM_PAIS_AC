import logging
import os

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Verificar si se cargó la URL y el TOKEN
if not os.getenv('TOKEN'):
    raise ValueError("TOKEN no encontrado. Por favor, revisa tu archivo .env.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != os.getenv('TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

