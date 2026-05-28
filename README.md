###Scrips y guia de utilización de ellos de parte de proyecto de tesis de Héctor en SPEL:

"analisis.py"

Este scrip funciona con un main de argsave, tiene 3 argumentos a entregar:

-carpeta de entrada de imagenes normalizadas

-proceso a realizar: linealidad, SNR, distribucion

-nombre con extension .csv de salida

Comando de ejmplo: python analisis.py norm_max103 linealidad linealidad_norm_max103.csv


"normalizar.py"

Este scrip sirve para normalizar las imagenes tomadas con anterioridad, recibe 2 argumentos con un main de argsave tambien:

- Ubicación de la carpeta de las imagenes a normalizar

-Nombre de la carpeta donde se agregaran las  imagenes normalizadas (si no existe la crea)

Comando de ejemplo: python normalizar.py max103 norm_max103

