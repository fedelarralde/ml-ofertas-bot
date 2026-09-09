"""
notificador_telegram.py
Envia las ofertas detectadas a un canal/chat de Telegram usando el Bot API
(100% gratis, sin limites de uso razonable).

Necesitas:
- TELEGRAM_BOT_TOKEN: token que te da BotFather
- TELEGRAM_CHAT_ID: id del canal/chat donde vas a publicar (ej: @mi_canal o -1001234567890)
"""

import os
import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def formatear_mensaje(p: dict) -> str:
    moneda = p.get("moneda", "$")
    return (
        f"🔥 <b>OFERTA</b>\n\n"
        f"{p['titulo']}\n\n"
        f"~{moneda} {p['precio_anterior']:,.0f}~ ➜ "
        f"<b>{moneda} {p['precio_actual']:,.0f}</b> "
        f"(-{p['baja_porcentaje']}%)\n\n"
        f"{'🚚 Envio gratis' if p.get('envio_gratis') else ''}\n"
        f"👉 {p['link']}"
    )


def enviar_oferta(p: dict) -> None:
    """Envia una foto con caption a Telegram."""
    url = f"{API_URL}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": formatear_mensaje(p),
        "parse_mode": "HTML",
        "photo": p["imagen"],
    }
    resp = requests.post(url, data=payload, timeout=15)
    if not resp.ok:
        print(f"[WARN] Telegram error para {p['id']}: {resp.text}")


def enviar_ofertas(ofertas: list[dict], maximo: int = 10) -> None:
    """Envia hasta `maximo` ofertas para no floodear el canal."""
    if not ofertas:
        return
    for p in ofertas[:maximo]:
        enviar_oferta(p)
