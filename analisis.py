import cv2
import numpy as np
import os
import glob
import csv
import argparse

def procesar_imagenes_camara(folder_path, tarea, nombre_csv):
    """
    Analiza imágenes de una carpeta según la tarea solicitada.
    Tareas disponibles: 'linealidad', 'snr', 'distribucion'
    """
    
    # 1. Detectar imágenes y tiempos de exposición, formato esperado: nombre_exptime_...png
    imagenes = sorted(glob.glob(os.path.join(folder_path, "*.png")))
    if not imagenes:
        raise FileNotFoundError(f"No hay imágenes en: {folder_path}")

    # Extraer tiempos únicos (asumiendo formato nombre_exptime_...)
    exptimes = sorted(list(set(float(os.path.basename(img).split("_")[1]) for img in imagenes)))

    # 2. Preparar el archivo CSV según la tarea
    with open(nombre_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        
        if tarea == "snr":
            writer.writerow(["name", "exptime", "SNR", "mean", "std", "pares_procesados"])
        elif tarea == "linealidad":
            writer.writerow(["name", "exptime", "mean", "std"])
        elif tarea == "distribucion":
            writer.writerow(["name", "par", "exptime", "bin_center", "count"])
        else:
            raise ValueError("Tarea no válida. Usa: 'snr', 'linealidad' o 'distribucion'")

        # 3. Procesar por tiempo de exposición
        for exptime in exptimes:
            # Filtrar imágenes de este tiempo
            imagenes_filtradas = [img for img in imagenes if float(os.path.basename(img).split("_")[1]) == exptime]
            n = len(imagenes_filtradas)
            

            if tarea == "linealidad":
                for i in range(n):
                    # Cargar imagen, guardar media y desviación estándar para la linealidad
                    img = cv2.imread(imagenes_filtradas[i], cv2.IMREAD_UNCHANGED).astype(np.float32)
                    name = os.path.basename(imagenes_filtradas[i])
                    writer.writerow([name, exptime, np.mean(img), np.std(img, ddof=1)])
            
            if tarea == "snr":
                for i in range(0, n - 1, 2):
                    #cargar dos imágenes consecutivas, calcular media, desviación estándar de la resta y SNR    
                    img1 = cv2.imread(imagenes_filtradas[i], cv2.IMREAD_UNCHANGED).astype(np.float32)
                    img2 = cv2.imread(imagenes_filtradas[i+1], cv2.IMREAD_UNCHANGED).astype(np.float32)
                    img_suma = (img1 + img2) / 2
                    img_resta = img1 - img2
                    I_mean = np.mean(img_suma)
                    sigma = np.std(img_resta, ddof=1)   
                    snr_val = np.sqrt(2) * I_mean / sigma  #EMVA Standard 1288
                    name = os.path.basename(imagenes_filtradas[i])
                    writer.writerow([name, exptime, snr_val, I_mean, sigma, (i//2)+1])  # Pares procesados
            if tarea == "distribucion":
                limite_pares = min(n - 1, 10)
                for i in range(0, limite_pares, 2):
                    # Cargar dos imágenes consecutivas, calcular la resta y generar el histograma de los valores de la resta
                    img1 = cv2.imread(imagenes_filtradas[i], cv2.IMREAD_UNCHANGED).astype(np.float32)
                    img2 = cv2.imread(imagenes_filtradas[i+1], cv2.IMREAD_UNCHANGED).astype(np.float32)
                    img_resta = img1 - img2
                    img_r = img_resta.flatten()
                    bin_width = 40 #ancho de cada bin del histograma
                    name = os.path.basename(imagenes_filtradas[i])
                    rango_total = (-65536, 65536)
                    span_total = rango_total[1] - rango_total[0]  # Esto da 131,072 unidades de rango

                    # Dividimos el rango total entre el ancho deseado: 
                    num_bins = int(span_total / bin_width)

                    counts, bin_edges = np.histogram(img_r, bins=num_bins, range=rango_total)
                    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

                    # Eliminar los bines donde count < 10
                    umbral = 10
                    mascara_validos = counts >= umbral

                    counts_filtrados = counts[mascara_validos]
                    bin_centers_filtrados = bin_centers[mascara_validos]
                    par_img=i//2 + 1
                    #guardamos los bins
                    for e in range(len(counts_filtrados)):
                        writer.writerow([name, par_img, exptime, bin_centers_filtrados[e], counts_filtrados[e]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesamiento de imágenes.")
    
    # Definimos qué palabras aceptará la terminal
    parser.add_argument("carpeta", type=str, help="Carpeta de entrada")
    parser.add_argument("tarea", type=str, choices=['snr', 'linealidad', 'distribucion'], help="Análisis a realizar")
    parser.add_argument("salida", type=str, help="Nombre del CSV resultante con extensión .csv")

    args = parser.parse_args()

    # Ejecutamos la función usando lo que el usuario escribió en la terminal
    procesar_imagenes_camara(args.carpeta, args.tarea, args.salida)
