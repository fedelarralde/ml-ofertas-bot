"""
main.py
Orquesta el flujo diario completo:
1. Consulta en MercadoLibre los productos definidos en productos.py
2. Compara contra el historico y detecta bajas de precio reales
3. Manda TODAS las ofertas detectadas al canal de Telegram
4. Publica en Instagram solo la MEJOR oferta del dia (para no floodear el feed)

Se ejecuta periodicamente via GitHub Actions (ver .github/workflows/daily.yml)
"""

from scraper import buscar_por_ids
from comparador import detectar_bajas
from notificador_telegram import enviar_ofertas
from auth_mercadolibre import obtener_access_token
from productos import PRODUCTOS_A_TRACKEAR


def main():
    print("Autenticando con MercadoLibre...")
    access_token = obtener_access_token()

    print(f"Consultando {len(PRODUCTOS_A_TRACKEAR)} productos...")
    productos = buscar_por_ids(PRODUCTOS_A_TRACKEAR, access_token)
    print(f"Se encontraron {len(productos)} productos en total")

    ofertas = detectar_bajas(productos)
    print(f"Se detectaron {len(ofertas)} ofertas con baja real de precio")

    if not ofertas:
        print("No hay ofertas nuevas hoy. Fin.")
        return

    # 1) Telegram: mandamos todas las ofertas (hasta un tope)
    enviar_ofertas(ofertas, maximo=10)
    print("Ofertas enviadas a Telegram")

    # 2) Instagram: solo la mejor oferta del dia
    # Descomentar cuando ya tengas configuradas las credenciales de Instagram
    # from publicador_instagram import publicar_oferta
    # mejor_oferta = ofertas[0]
    # media_id = publicar_oferta(mejor_oferta)
    # print(f"Publicado en Instagram: {media_id}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
