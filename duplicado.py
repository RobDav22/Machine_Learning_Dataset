import os
from PIL import Image
import imagehash

# 📁 Ruta del dataset (ajústala)
DATASET_DIR = "anacahuita"

# ⚙️ Configuración
HASH_SIZE = 8              # Tamaño del hash (8 es buen equilibrio)
DUPLICATE_THRESHOLD = 5    # Diferencia máxima para considerar dos imágenes como iguales

# 📦 Recolectar todas las rutas de imágenes
valid_extensions = {".jpg", ".jpeg", ".png"}
image_paths = [
    os.path.join(DATASET_DIR, f)
    for f in os.listdir(DATASET_DIR)
    if os.path.splitext(f)[1].lower() in valid_extensions
]

print(f"🔍 Analizando {len(image_paths)} imágenes en busca de duplicados...")

hashes = {}
removed = 0

for img_path in image_paths:
    try:
        with Image.open(img_path) as img:
            img_hash = imagehash.average_hash(img, hash_size=HASH_SIZE)
    except Exception as e:
        print(f"⚠️ No se pudo procesar {img_path}: {e}")
        continue

    # Buscar duplicado visualmente similar
    duplicate_found = False
    for existing_hash, existing_path in hashes.items():
        if abs(img_hash - existing_hash) <= DUPLICATE_THRESHOLD:
            print(f"🗑️ Duplicado detectado: {img_path} ≈ {existing_path}")
            os.remove(img_path)
            removed += 1
            duplicate_found = True
            break

    if not duplicate_found:
        hashes[img_hash] = img_path

print(f"\n✅ Limpieza completa.")
print(f"Total de duplicados eliminados: {removed}")
print(f"Total de imágenes únicas restantes: {len(hashes)}")
