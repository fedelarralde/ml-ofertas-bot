"""
scraper.py
Consulta la API publica de MercadoLibre (sin necesidad de token) y devuelve
una lista normalizada de productos para las keywords que configures.

Docs: https://developers.mercadolibre.com.ar/es_ar/items-y-busquedas
"""

import requests
import time

# Cambia esto por tu sitio: MLA = Argentina, MLM = Mexico, MLB = Brasil,
# MCO = Colombia, MLC = Chile, MPE = Peru, etc.
SITE_ID = "MLA"

BASE_URL = f"https://api.mercadolibre.com/sites/{SITE_ID}/search"


def buscar_productos(keyword: str, limite: int = 20) -> list[dict]:
    """
    Busca productos por keyword y devuelve una lista de dicts normalizados.
    """
    params = {
        "q": keyword,
        "limit": limite,
    }

    resp = requests.get(BASE_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    productos = []
    for item in data.get("results", []):
        precio_actual = item.get("price")
        precio_original = item.get("original_price")  # viene solo si esta en oferta

        productos.append({
            "id": item.get("id"),
            "titulo": item.get("title"),
            "precio_actual": precio_actual,
            "precio_original": precio_original,
            "moneda": item.get("currency_id"),
            "link": item.get("permalink"),
            "imagen": item.get("thumbnail", "").replace("http://", "https://"),
            "envio_gratis": item.get("shipping", {}).get("free_shipping", False),
            "condicion": item.get("condition"),
        })

    return productos


def buscar_multiples(keywords: list[str], limite_por_keyword: int = 20) -> list[dict]:
    """
    Recorre una lista de keywords y junta todos los resultados.
    Espera 1 segundo entre requests para no saturar la API.
    """
    todos = []
    for kw in keywords:
        try:
            todos.extend(buscar_productos(kw, limite_por_keyword))
        except requests.RequestException as e:
            print(f"[WARN] Error buscando '{kw}': {e}")
        time.sleep(1)
    return todos


if __name__ == "__main__":
    # Prueba rapida
    resultados = buscar_productos("notebook gamer", limite=5)
    for p in resultados:
        print(p["titulo"], "-", p["precio_actual"], p["moneda"])
