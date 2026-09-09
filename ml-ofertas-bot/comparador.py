"""
comparador.py
Compara los precios de hoy contra el historico guardado en data/precios.json
y devuelve la lista de productos que bajaron de precio (o que ML marca
como oferta con descuento).
"""

import json
import os

RUTA_HISTORICO = os.path.join("data", "precios.json")

# Umbral minimo de baja para considerarlo una "oferta real" (evita ruido)
UMBRAL_BAJA_PORCENTAJE = 5  # 5% o mas


def cargar_historico() -> dict:
    if not os.path.exists(RUTA_HISTORICO):
        return {}
    with open(RUTA_HISTORICO, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_historico(historico: dict) -> None:
    os.makedirs("data", exist_ok=True)
    with open(RUTA_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


def detectar_bajas(productos: list[dict]) -> list[dict]:
    """
    Recibe la lista de productos de hoy, la compara contra el historico,
    actualiza el historico y devuelve solo los que bajaron de precio.
    """
    historico = cargar_historico()
    ofertas_detectadas = []

    for p in productos:
        pid = p["id"]
        precio_hoy = p["precio_actual"]

        if precio_hoy is None:
            continue

        registro_previo = historico.get(pid)

        if registro_previo:
            precio_anterior = registro_previo["precio_actual"]
            if precio_anterior and precio_anterior > precio_hoy:
                baja_pct = round((1 - precio_hoy / precio_anterior) * 100, 1)
                if baja_pct >= UMBRAL_BAJA_PORCENTAJE:
                    p["precio_anterior"] = precio_anterior
                    p["baja_porcentaje"] = baja_pct
                    ofertas_detectadas.append(p)

        # Tambien consideramos oferta si ML marca un original_price mas alto
        elif p.get("precio_original") and p["precio_original"] > precio_hoy:
            baja_pct = round((1 - precio_hoy / p["precio_original"]) * 100, 1)
            if baja_pct >= UMBRAL_BAJA_PORCENTAJE:
                p["precio_anterior"] = p["precio_original"]
                p["baja_porcentaje"] = baja_pct
                ofertas_detectadas.append(p)

        # Actualizamos el historico con el precio de hoy
        historico[pid] = {
            "titulo": p["titulo"],
            "precio_actual": precio_hoy,
        }

    guardar_historico(historico)

    # Ordenamos de mayor a menor baja porcentual
    ofertas_detectadas.sort(key=lambda x: x["baja_porcentaje"], reverse=True)
    return ofertas_detectadas
