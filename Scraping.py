
# # SCRAPING

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "es-MX,es;q=0.9"
# }

# def scrapear_mercado_libre(estado_busqueda, tipo_inmueble="casa"):
#     resultados = []
#     # Cambiamos 'casas' por la variable tipo_inmueble
#     url = f"https://inmuebles.mercadolibre.com.mx/{tipo_inmueble}/venta/{estado_busqueda}/"

#     print(f"Buscando {tipo_inmueble} en {estado_busqueda}...")

#     try:
#         response = requests.get(url, headers=HEADERS, timeout=10)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Selección de anuncios
#         anuncios = soup.find_all('div', class_=lambda x: x and 'ui-search-result__wrapper' in x)
#         if not anuncios:
#             anuncios = soup.select(".ui-search-layout__item")

#         for anuncio in anuncios:
#             try:
#                 precio_elem = anuncio.find('span', class_='andes-money-amount__fraction')
#                 precio = precio_elem.text.replace(',', '') if precio_elem else "0"

#                 titulo_elem = anuncio.find('h2') or anuncio.find('h3')
#                 titulo = titulo_elem.text.strip() if titulo_elem else "Sin título"

#                 atributos = anuncio.find_all('li', class_='ui-search-card-attributes__attribute')
#                 m2 = atributos[0].text if len(atributos) > 0 else "N/A"
#                 recamaras = atributos[1].text if len(atributos) > 1 else "N/A"

#                 link_elem = anuncio.find('a')
#                 link = link_elem['href'] if link_elem else ""

#                 resultados.append({
#                     "Tipo": tipo_inmueble,
#                     "Estado": estado_busqueda,
#                     "Precio": precio,
#                     "Dimensiones": m2,
#                     "Habitaciones": recamaras,
#                     "Titulo": titulo,
#                     "Link": link
#                 })
#             except Exception:
#                 continue

#         print(f"Se encontraron {len(resultados)} anuncios.")

#     except Exception as e:
#         print(f"Error en la conexión: {e}")

#     return pd.DataFrame(resultados)

# # --- Ejecución ---
# # Ahora puedes elegir: "departamentos", "casas", "terrenos", etc.
# df = scrapear_mercado_libre("Yucatan", "departamento")

# if not df.empty:
#     df.to_csv("datos_departamentos_mch.csv", index=False)
#     print("Archivo guardado con éxito.")

# # if not df.empty:
# #     df.to_csv("datos_casas_mch.csv", index=False)
# #     print("Archivo guardado con éxito.")










# # UNIFICAR CSV
# import pandas as pd
# import glob
# import os

# # Ruta de la carpeta donde están los archivos
# ruta_carpeta = r"C:\Users\Usuario\OneDrive\DATOS TESIS"

# # Buscar todos los archivos que empiecen por "datos" y sean .csv
# archivos = glob.glob(os.path.join(ruta_carpeta, "datos*.csv"))

# # Lista para guardar los DataFrames
# lista_df = []

# # Leer cada archivo y agregarlo a la lista
# for archivo in archivos:
#     df = pd.read_csv(archivo, encoding="utf-8")  # Puedes cambiar encoding si es necesario
#     lista_df.append(df)

# # Unir todos los DataFrames
# df_final = pd.concat(lista_df, ignore_index=True)

# # Guardar el archivo unificado en formato .xlsx
# df_final.to_excel(os.path.join(ruta_carpeta, "datos_unificados.xlsx"), index=False)

# print("Archivos CSV unificados y exportados a Excel correctamente.")









# # UNIFICAR XLSX
# import pandas as pd
# import glob
# import os

# # Ruta de la carpeta donde están los archivos
# ruta_carpeta = r"C:\Users\Usuario\OneDrive\DATOS TESIS"

# # Buscar todos los archivos que empiecen por "datos" y sean .xlsx
# archivos = glob.glob(os.path.join(ruta_carpeta, "datos*.xlsx"))

# # Lista para guardar los DataFrames
# lista_df = []

# # Leer cada archivo y agregarlo a la lista
# for archivo in archivos:
#     df = pd.read_excel(archivo)  # Ya no necesita encoding
#     lista_df.append(df)

# # Unir todos los DataFrames
# df_final = pd.concat(lista_df, ignore_index=True)

# # Guardar el archivo unificado en formato .xlsx
# df_final.to_excel(os.path.join(ruta_carpeta, "datos.xlsx"), index=False)

# print("Archivos XLSX unificados y exportados correctamente.")








# ## ELIMINAR DUPLICADOS
# import pandas as pd
# # Ruta del archivo
# ruta_archivo = r"C:\Users\Usuario\OneDrive\DATOS TESIS\datos_unificados2.xlsx"

# # Cargar archivo
# df = pd.read_excel(ruta_archivo)

# # Eliminar duplicados por la columna "Link"
# df = df.drop_duplicates(subset=["Link"])

# # Guardar en el mismo archivo (lo sobrescribe)
# df.to_excel(ruta_archivo, index=False)

# print("Duplicados eliminados y archivo actualizado correctamente.")














#### WEB SCRAPPING MERCADO LIBRE
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-MX,es;q=0.9"
}

def limpiar_numero(texto):
    """Extrae solo dígitos y punto decimal de un string."""
    if not texto:
        return None
    limpio = re.sub(r'[^\d.]', '', texto.replace(',', ''))
    try:
        return float(limpio)
    except:
        return None

def extraer_atributos(anuncio):
    """
    Extrae Dimensiones, Habitaciones, Baños, Estacionamiento y Pisos
    buscando por texto en los atributos del anuncio.
    """
    datos = {
        "Dimensiones": None,
        "Habitaciones": None,
        "Baños": None,
        "Estacionamiento": None,
        "Pisos": None
    }

    atributos = anuncio.find_all('li', class_=lambda x: x and 'ui-search-card-attributes__attribute' in x)

    for attr in atributos:
        texto = attr.get_text(separator=' ').lower().strip()

        if 'm²' in texto or 'm2 construidos' in texto:
            datos["Dimensiones"] = limpiar_numero(texto)

        elif 'recámaras' in texto or 'rec.' in texto or 'habitacion' in texto or 'cuarto' in texto:
            datos["Habitaciones"] = limpiar_numero(texto)

        elif 'baño' in texto or 'baños' in texto:
            datos["Baños"] = limpiar_numero(texto)

        elif 'estacionamientos' in texto or 'cochera' in texto or 'garage' in texto:
            datos["Estacionamiento"] = limpiar_numero(texto)

        elif 'cantidad de pisos' in texto or 'nivel' in texto or 'planta' in texto:
            datos["Pisos"] = limpiar_numero(texto)

    return datos

def extraer_ubicacion(anuncio):
    """Extrae Municipio y Colonia desde la dirección del anuncio."""
    municipio, colonia = None, None

    ubicacion_elem = (
        anuncio.find('span', class_=lambda x: x and 'ui-search-item__location' in x) or
        anuncio.find('span', class_=lambda x: x and 'ui-search-item__group__element' in x and 'location' in (x or ''))
    )

    if ubicacion_elem:
        texto = ubicacion_elem.get_text(separator=',').strip()
        partes = [p.strip() for p in texto.split(',')]
        # MercadoLibre suele mostrar: Colonia, Municipio  o  Municipio, Estado
        if len(partes) >= 2:
            colonia   = partes[0]
            municipio = partes[1]
        elif len(partes) == 1:
            municipio = partes[0]

    return municipio, colonia

def extraer_moneda(anuncio):
    """Detecta si el precio es MXN o USD."""
    simbolo = anuncio.find('span', class_=lambda x: x and 'andes-money-amount__currency-symbol' in x)
    if simbolo:
        texto = simbolo.text.strip()
        if 'US' in texto or '$' == texto:
            # MercadoLibre usa 'US$' para dólares y '$' para pesos
            contenedor = anuncio.find('span', class_=lambda x: x and 'andes-money-amount' in x)
            if contenedor and 'USD' in contenedor.get('aria-label', ''):
                return 'US'
        return 'MXN'
    return 'MXN'

def scrapear_pagina(url, estado, tipo_inmueble):
    """Scrapea una sola página y devuelve lista de registros."""
    resultados = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"  Status {response.status_code} en {url}")
            return resultados, False

        soup = BeautifulSoup(response.text, 'html.parser')

        # Detectar anuncios
        anuncios = soup.find_all('div', class_=lambda x: x and 'ui-search-result__wrapper' in x)
        if not anuncios:
            anuncios = soup.select('.ui-search-layout__item')

        if not anuncios:
            return resultados, False  # No hay más páginas

        for anuncio in anuncios:
            try:
                # Precio
                precio_elem = anuncio.find('span', class_='andes-money-amount__fraction')
                precio = limpiar_numero(precio_elem.text) if precio_elem else None

                # Moneda
                tc = extraer_moneda(anuncio)

                # Ubicación
                municipio, colonia = extraer_ubicacion(anuncio)

                # Atributos físicos
                atributos = extraer_atributos(anuncio)

                # Link
                link_elem = anuncio.find('a', href=True)
                link = link_elem['href'].split('#')[0] if link_elem else None  # limpia el tracking

                # Tipo limpio
                tipo_limpio = tipo_inmueble.capitalize()

                resultados.append({
                    "Estado":           estado,
                    "Municipio":        municipio,
                    "Colonia":          colonia,
                    "Precio":           precio,
                    "Dimensiones":      atributos["Dimensiones"],
                    "Habitaciones":     atributos["Habitaciones"],
                    "Baños":            atributos["Baños"],
                    "Tipo":             tipo_limpio,
                    "Estacionamiento":  atributos["Estacionamiento"],
                    "Pisos":            atributos["Pisos"],
                    "Link":             link,
                    "TC":               tc,
                    "Fecha":            pd.Timestamp.today().date()
                })

            except Exception as e:
                continue

        return resultados, True

    except Exception as e:
        print(f"  Error de conexión: {e}")
        return resultados, False

def scrapear_mercado_libre(estado, tipo_inmueble="casa", max_paginas=20, pausa=2):
    """
    Scrapea múltiples páginas de MercadoLibre para un estado y tipo de inmueble.
    
    Parámetros:
        estado        : nombre del estado como aparece en la URL (ej: 'jalisco')
        tipo_inmueble : 'casas' o 'departamentos'
        max_paginas   : límite de páginas a recorrer
        pausa         : segundos entre requests (respetar el servidor)
    """
    todos = []
    #base_url = f"https://inmuebles.mercadolibre.com.mx/{tipo_inmueble}/venta/{estado}/"
    ordenes = [
    "_OrderId_PRICE_ASC",
    "_OrderId_PRICE_DESC", 
    "_OrderId_USED"  # más antiguos
    ]
    for orden in ordenes:
        base_url = f"https://inmuebles.mercadolibre.com.mx/{tipo_inmueble}/venta/{estado}/{orden}"


    print(f"\n{'='*50}")
    print(f"Scraping: {tipo_inmueble} en {estado}")
    print(f"{'='*50}")

    for pagina in range(1, max_paginas + 1):
        # MercadoLibre pagina con offset: _Desde_1, _Desde_49, _Desde_97...
        offset = (pagina - 1) * 48 + 1
        url = base_url if pagina == 1 else f"{base_url}_Desde_{offset}"

        print(f"  Página {pagina} ({len(todos)} registros acumulados)...")

        registros, hay_mas = scrapear_pagina(url, estado, tipo_inmueble)
        todos.extend(registros)

        if not hay_mas or len(registros) == 0:
            print(f"  Sin más resultados en página {pagina}. Terminando.")
            break

        time.sleep(pausa)  # pausa entre páginas

    print(f"Total obtenido para {estado} - {tipo_inmueble}: {len(todos)} registros")
    return pd.DataFrame(todos)


# ============================================================
# EJECUCIÓN
# Ajusta la lista de estados y tipos según lo que necesites
# ============================================================
municipios_zmg = ["acatlan-de-juarez",
                  "el-salto",
                  "guadalajara",
                  "ixtlahuacan-de-los-membrillos",
                  "juanacatlan",
                  "san-pedro-tlaquepaque",
                  "tlajomulco-de-zuñiga",
                  "tonala",
                  "zapopan",
                  "zapotlanejo"]

estados = [
    "aguascalientes",
    "baja-california",
    "baja-california-sur",
    "campeche",
    "chiapas",
    "chihuahua",
    "coahuila",
    "colima",
    "durango",
    "guanajuato",
    "guerrero",
    "hidalgo",
    "michoacan",
    "morelos",
    "nayarit",
    "jalisco",
    "nuevo-leon",
    "ciudad-de-mexico",
    "estado-de-mexico",
    "queretaro",
    "oaxaca",
    "puebla",
    "quintana-roo",
    "san-luis-potosi",
    "sinaloa",
    "sonora",
    "tabasco",
    "tamaulipas",
    "tlaxcala",
    "veracruz",
    "yucatan",
    "zacatecas"
]

tipos = ["casa", "departamento"]

df_total = pd.DataFrame()

for estado in municipios_zmg:
    for tipo in tipos:
        df_parcial = scrapear_mercado_libre(
            estado=estado,
            tipo_inmueble=tipo,
            max_paginas=20,   # ~960 registros máx por estado/tipo
            pausa=2           # segundos entre páginas
        )
        df_total = pd.concat([df_total, df_parcial], ignore_index=True)
        time.sleep(3)  # pausa extra entre estados

# Quitar duplicados por link antes de guardar
df_total = df_total.drop_duplicates(subset=["Link"])

print(f"\nTotal final: {len(df_total)} registros únicos")
print(df_total.head())

# Guardar
df_total.to_excel(r"C:\Users\Usuario\OneDrive\DATOS TESIS\datos_scraping__.xlsx", index=False)
print("Archivo guardado: datos_scraping.xlsx")
