import requests
import os
import time

# 🔑 CONFIGURACIÓN — reemplaza con tus claves reales
API_KEY = "AIzaSyBuVLFlSqDThrU6YeYIaYcoY4SmdWX5trE"
CX = "034fa0667dcbc4c01"

RESULTS_PER_REQUEST = 10   # Máximo permitido por la API
MAX_IMAGES = 200           # Número total de imágenes a intentar descargar

# 🌿 Parámetros de búsqueda
FLOWER_NAME = "corona_de_cristo"
SEARCH_QUERY = "Euphorbia milii Crown of Thorns flower Espina de Cristo"

# 📁 Crear carpeta para guardar las imágenes
BASE_DIR = "corona_de_cristo"
os.makedirs(BASE_DIR, exist_ok=True)

downloaded = 0
print(f"\n💜 Descargando imágenes de: {FLOWER_NAME}")

# 🔄 Ciclo para ir pidiendo lotes de resultados
for start in range(1, MAX_IMAGES, RESULTS_PER_REQUEST):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": SEARCH_QUERY,
        "searchType": "image",
        "num": RESULTS_PER_REQUEST,
        "start": start,
        "imgType": "photo",
        "imgColorType": "color",
        "safe": "active",
        "imgSize": "xlarge"
        # Puedes quitar "rights" si quieres más resultados:
        # "rights": "cc_publicdomain,cc_attribute,cc_sharealike",
    }

    try:
        response = requests.get(url, params=params, timeout=10).json()
        items = response.get("items", [])
        if not items:
            print("⚠️ No se encontraron más imágenes.")
            break

        for item in items:
            if downloaded >= MAX_IMAGES:
                break

            image_url = item["link"]
            try:
                img_data = requests.get(image_url, timeout=10).content
                filename = f"{FLOWER_NAME}_{downloaded+1}.jpg"
                filepath = os.path.join(BASE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                downloaded += 1
                print(f"✅ {FLOWER_NAME} [{downloaded}] — {image_url}")

            except Exception as e:
                print(f"❌ Error con {image_url}: {e}")

        time.sleep(1)  # ⏳ Espera para evitar límite de peticiones

    except Exception as e:
        print(f"⚠️ Error en la consulta API: {e}")
        break

print(f"\n🎉 Descarga completada. Total: {downloaded} imágenes guardadas en '{BASE_DIR}'.")
