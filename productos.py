"""
productos.py
Lista de productos que el bot va a trackear, buscando bajas de precio.

Como sumar un producto nuevo:
1. Entra al producto en MercadoLibre (mercadolibre.com.ar).
2. Copia el ID que aparece en la URL. Tiene el formato MLA + numeros.
   Puede aparecer de 2 formas en la URL:
   - .../p/MLA35277842   (productos con variantes/catalogo)
   - .../MLA-928853579-... (publicaciones individuales, con un guion
     despues de MLA que hay que sacar: queda MLA928853579)
3. Agregalo a la lista de abajo, como un string mas.

Los productos de este archivo son solo un punto de partida de ejemplo,
verificados al momento de armar el bot pero es buena practica revisar
cada tanto que sigan activos (un producto dado de baja simplemente no
va a aparecer en los resultados, no rompe nada).
"""

PRODUCTOS_A_TRACKEAR = [
    "MLA35277842",   # Notebook Asus Vivobook 16 i7
    "MLA40164574",   # Notebook Lenovo Ideapad 1 15.6 i5
    "MLA928853579",  # Soporte para notebook gamer RGB
    "MLA1119125231", # Notebook HP 15 Gamer Ryzen 5
    # Agrega tus propios productos aca abajo, uno por linea:
    # "MLAxxxxxxxxx",
]
