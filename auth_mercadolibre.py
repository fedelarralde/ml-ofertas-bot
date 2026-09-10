"""
auth_mercadolibre.py
Maneja la autenticacion OAuth de la API de MercadoLibre.

Desde abril de 2025, MercadoLibre exige que las consultas al endpoint de
busqueda vayan autenticadas con un access_token. Este modulo usa un
refresh_token (que no expira mientras se use) para pedir un access_token
nuevo en cada corrida del bot.

Necesita 3 variables de entorno:
- ML_CLIENT_ID
- ML_CLIENT_SECRET
- ML_REFRESH_TOKEN
"""

import os
import requests

ML_CLIENT_ID = os.environ["ML_CLIENT_ID"]
ML_CLIENT_SECRET = os.environ["ML_CLIENT_SECRET"]
ML_REFRESH_TOKEN = os.environ["ML_REFRESH_TOKEN"]

TOKEN_URL = "https://api.mercadolibre.com/oauth/token"


def obtener_access_token() -> str:
    """
    Cambia el refresh_token por un access_token valido (dura ~6 horas).
    Se llama una vez al principio de cada corrida del bot.
    """
    payload = {
        "grant_type": "refresh_token",
        "client_id": ML_CLIENT_ID,
        "client_secret": ML_CLIENT_SECRET,
        "refresh_token": ML_REFRESH_TOKEN,
    }
    resp = requests.post(TOKEN_URL, data=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"]
