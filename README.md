# Scripts de Análisis y Procesamiento de imágenes - Tesis (SPEL - Héctor Ramírez)

Este repositorio contiene los scripts necesarios para el procesamiento y análisis estadístico de imágenes capturadas en el SUCHAI 4 para obtener datos sobre la linealidad, SNR o distribución de ruido para su posterior estudio.

---

### `analisis.py`

Este script utiliza `argparse` para gestionar los parámetros de ejecución. Requiere tres argumentos basicos para funcionar, pero puede incluirse un cuarto opcional :

1. **Carpeta de entrada:** Directorio que contiene las imágenes normalizadas o sin normalizar a utilizar.
2. **Proceso a realizar:** Tarea a ejecutar (`linealidad`, `snr` o `distribucion`).
3. **Archivo de salida:** Nombre del archivo resultante con extensión `.csv`.
4. **(Opcional) Número de histogramas de distribución:** Agregando `--max_pares`al final y un número, se puede ajustar la cantidad de histogramas por tiempo de exposición, por defecto esta en 3.

**Comandos de ejemplo:**
```bash
python analisis.py norm_max103 linealidad linealidad_norm_max103.csv
```

```bash
python analisis.py norm_max103 distribución dist_norm_max103.csv --max_pares 8
```
---
### `normalizar.py`

Este scrip tambien utiliza `argparse` para gestionar los parámetros de ejecución. Requiere dos argumentos para funcionar:

1. **Carpeta de entrada**: Directorio que contiene las imágenes que se requiere normalizar
2. **Carpeta de salida**: Directorio que contendra a las imágenes normalizadas, en caso de no existir se puede crear en la carpeta de ejecución del scrip solo dando un nombre

**Comando de ejemplo:**

```bash
python normalizar.py max103 norm_max103
```
---
## Prerrequisitos e Instalación

Este proyecto requiere Python 3.12 o superior y un conjunto de librerías externas para el procesamiento de matrices e imágenes. 

Para configurar tu entorno e instalar todas las dependencias con las versiones exactas utilizadas en el desarrollo, abre una terminal en la raíz de este proyecto y utilizando `requirements.txt` ejecuta:

```bash
pip install -r requirements.txt


