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


def buscar_productos(keyword: str, access_token: str, limite: int = 20) -> list[dict]:
    """
    Busca productos por keyword y devuelve una lista de dicts normalizados.
    Requiere un access_token valido (ver auth_mercadolibre.py), porque desde
    abril de 2025 MercadoLibre exige autenticacion para este endpoint.
    """
    params = {
        "q": keyword,
        "limit": limite,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    resp = requests.get(BASE_URL, params=params, headers=headers, timeout=15)
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


def buscar_por_ids(ids: list[str], access_token: str) -> list[dict]:
    """
    Busca productos puntuales por su ID (ej: MLA35277842).
    Usa el endpoint /items?ids=... que SI sigue funcionando (a diferencia
    de /sites/MLA/search, que MercadoLibre restringio para desarrolladores
    externos). MercadoLibre permite hasta 20 ids por llamada, asi que esta
    funcion los agrupa en lotes de a 20 automaticamente.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    productos = []
    lote_tamano = 20

    for i in range(0, len(ids), lote_tamano):
        lote = ids[i:i + lote_tamano]
        params = {"ids": ",".join(lote)}

        try:
            resp = requests.get(
                "https://api.mercadolibre.com/items",
                params=params,
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            resultados = resp.json()
        except requests.RequestException as e:
            print(f"[WARN] Error buscando lote {lote}: {e}")
            continue

        for entry in resultados:
            if entry.get("code") != 200:
                print(f"[WARN] No se pudo obtener {entry.get('body', {}).get('id')}: {entry.get('code')}")
                print(f"[WARN] Detalle completo: {entry}")
                continue

            item = entry["body"]
            precio_actual = item.get("price")
            precio_original = item.get("original_price")

            productos.append({
                "id": item.get("id"),
                "titulo": item.get("title"),
                "precio_actual": precio_actual,
                "precio_original": precio_original,
                "moneda": item.get("currency_id"),
                "link": item.get("permalink"),
                "imagen": (item.get("pictures") or [{}])[0].get("secure_url", ""),
                "envio_gratis": item.get("shipping", {}).get("free_shipping", False),
                "condicion": item.get("condition"),
            })

        time.sleep(1)

    return productos
