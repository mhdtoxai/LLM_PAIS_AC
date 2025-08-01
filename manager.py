import os
import requests
import json
import re
from dotenv import load_dotenv
from prompts import PROMPT_CLASIFICADOR, PROMPT_CONSULTAS, PROMPT_ACCIONES

load_dotenv()

SAPTIVA_API_KEY = os.getenv("SAPTIVA_API_KEY")
SAPTIVA_URL = "https://api.saptiva.com/v1/chat/completions"
session = requests.Session()  # Para reusar conexión


def extraer_json_valido(texto: str) -> dict:
    try:
        # Limpieza de bloques ```json
        texto_limpio = texto.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(texto_limpio)
    except:
        try:
            match = re.search(r'\{.*?\}', texto, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception as e:
            print(f"⚠️ Error extrayendo JSON con regex: {e}")
        print(f"⚠️ Texto inválido: {texto}")
        return {}


def detectar_intencion(message: str) -> str:
    try:
        response = session.post(
            SAPTIVA_URL,
            headers={
                "Authorization": f"Bearer {SAPTIVA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Saptiva Turbo",
                "messages": [
                    {"role": "system", "content": PROMPT_CLASIFICADOR},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.0,
                "max_tokens": 50
            },
            timeout=10
        )
        raw = response.json()["choices"][0]["message"]["content"]
        data = extraer_json_valido(raw)
        return data.get("intencion", "consulta_general")
    except Exception as e:
        print(f"❌ Error en clasificador: {e}")
        return "consulta_general"


def ai_manager(message: str, member: bool = False) -> str:
    print(f"📩 Mensaje: '{message}' | ¿Miembro?: {member}")
    intencion = detectar_intencion(message)
    print(f"🔍 Intención detectada: {intencion}")

    if intencion == "fuera_de_dominio":
        return "Lo siento, solo puedo ayudarte con información relacionada con PAIS AC"

    prompt = PROMPT_CONSULTAS if intencion == "consulta_general" else PROMPT_ACCIONES
    if intencion == "accion_personal" and not member:
        return "Esta información está disponible solo para miembros afiliados a PAIS AC Si deseas afiliarte, con gusto te explico cómo hacerlo. 😊"

    try:
        response = session.post(
            SAPTIVA_URL,
            headers={
                "Authorization": f"Bearer {SAPTIVA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Saptiva Turbo",
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.2,
                "max_tokens": 400
            },
            timeout=20
        )
        raw = response.json()["choices"][0]["message"]["content"]

        if intencion == "accion_personal":
            data = extraer_json_valido(raw)
            return json.dumps(data) if data else "No se pudo obtener la acción."
        else:
            return raw.strip()

    except Exception as e:
        print(f"❌ Error en AI: {e}")
        return "Ocurrió un error al generar la respuesta."
