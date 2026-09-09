"""
publicador_instagram.py
Publica la mejor oferta del dia en Instagram usando la Graph API de Meta
(gratis para uso personal/propio, sin necesidad de revision de app).

Necesitas:
- IG_ACCESS_TOKEN: access token de larga duracion de tu app en Meta for Developers
- IG_BUSINESS_ID: el ID de tu cuenta de Instagram Business/Creator

Proceso de publicacion en 2 pasos (asi funciona la API de Meta):
1. Crear un "media container" con la imagen y el caption
2. Publicar ese container
"""

import os
import time
import requests

IG_ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
IG_BUSINESS_ID = os.environ["IG_BUSINESS_ID"]

GRAPH_URL = "https://graph.facebook.com/v21.0"


def formatear_caption(p: dict) -> str:
    moneda = p.get("moneda", "$")
    return (
        f"🔥 OFERTA DEL DIA 🔥\n\n"
        f"{p['titulo']}\n\n"
        f"Antes: {moneda} {p['precio_anterior']:,.0f}\n"
        f"Ahora: {moneda} {p['precio_actual']:,.0f} (-{p['baja_porcentaje']}%)\n\n"
        f"Link en el primer comentario 👇\n"
        f"#ofertas #descuentos #mercadolibre"
    )


def publicar_oferta(p: dict) -> str | None:
    """Publica una oferta como post de imagen en Instagram. Devuelve el media_id."""

    # Paso 1: crear el contenedor
    crear_url = f"{GRAPH_URL}/{IG_BUSINESS_ID}/media"
    payload_crear = {
        "image_url": p["imagen"],
        "caption": formatear_caption(p),
        "access_token": IG_ACCESS_TOKEN,
    }
    r1 = requests.post(crear_url, data=payload_crear, timeout=20)
    if not r1.ok:
        print(f"[WARN] Error creando media container: {r1.text}")
        return None

    container_id = r1.json().get("id")
    if not container_id:
        return None

    # Pequena espera para que Meta procese la imagen antes de publicar
    time.sleep(5)

    # Paso 2: publicar el contenedor
    publicar_url = f"{GRAPH_URL}/{IG_BUSINESS_ID}/media_publish"
    payload_publicar = {
        "creation_id": container_id,
        "access_token": IG_ACCESS_TOKEN,
    }
    r2 = requests.post(publicar_url, data=payload_publicar, timeout=20)
    if not r2.ok:
        print(f"[WARN] Error publicando: {r2.text}")
        return None

    media_id = r2.json().get("id")

    # Opcional: comentar el link del producto en el post recien publicado
    if media_id:
        comentar_url = f"{GRAPH_URL}/{media_id}/comments"
        requests.post(
            comentar_url,
            data={"message": p["link"], "access_token": IG_ACCESS_TOKEN},
            timeout=15,
        )

    return media_id
