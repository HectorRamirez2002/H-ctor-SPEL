import cv2
import numpy as np
import os
import glob
import csv
import matplotlib.pyplot as plt
import argparse

def normalizar_imagenes(in_folder, out_folder):
    """Normaliza las imágenes de una carpeta usando sus respectivas imágenes promedio."""

    os.makedirs(out_folder, exist_ok=True)

    # 1. Detectar imágenes y tiempos de exposición, formato esperado: nombre_exptime_...png
    imagenes = sorted(glob.glob(os.path.join(in_folder, "*.png")))
    if not imagenes:
        raise FileNotFoundError(f"No hay imágenes en: {in_folder}")

    # Extraer tiempos únicos (asumiendo formato nombre_exptime_...)
    exptimes = sorted(list(set(float(os.path.basename(img).split("_")[1]) for img in imagenes)))

    for exptime in exptimes:
            # Filtrar imágenes de este tiempo
            imagenes_filtradas = [img for img in imagenes if float(os.path.basename(img).split("_")[1]) == exptime]
    

            suma = None
            imagenes_cargadas = []
            for ruta in imagenes_filtradas:
                img = cv2.imread(ruta, cv2.IMREAD_UNCHANGED).astype(np.float32)
                imagenes_cargadas.append((ruta, img))
                if suma is None:
                    suma = np.zeros_like(img, dtype=np.float32)
                suma += img
            n = len(imagenes_cargadas)
            # Imagen promedio
            img_promedio = suma / n
            mean_img_promedio = np.mean(img_promedio)
            #aseguramos que no haya ceros en el promedio para evitar división por cero
            img_promedio_segura = np.where(img_promedio == 0, 1.0, img_promedio)
            # Normalizar cada imagen y guardarla
            for ruta, img in imagenes_cargadas:
                img_normalizada = (img / img_promedio_segura) * mean_img_promedio
                
                # Recortar al rango dinámico de 16 bits seguro y guardar
                img_normalizada = np.clip(img_normalizada, 0, 65535).astype(np.uint16)
                
                salida = os.path.join(out_folder, os.path.basename(ruta))
                cv2.imwrite(salida, img_normalizada)
               

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="normalización de imágenes.")
    
    # Definimos qué palabras aceptará la terminal
    parser.add_argument("carpeta", type=str, help="Carpeta de entrada")
    parser.add_argument("salida", type=str, help="Carpeta de salida")

    args = parser.parse_args()

    # Ejecutamos la función usando lo que el usuario escribió en la terminal
    normalizar_imagenes(args.carpeta, args.salida)
