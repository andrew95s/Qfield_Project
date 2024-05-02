#====Este codigo copia algunos shapes de las gdbs Actualizadas a los directorios de cada municipio====

import os
import shutil
from qgis.core import *


# Ruta relativa a la carpeta del script
carpeta = os.path.join(os.path.dirname(__file__), "..", "databases", "shps_rural")

# Comprobar si la carpeta existe
if os.path.exists(carpeta):
    # Eliminar el contenido de la carpeta
    for archivo in os.listdir(carpeta):
        archivo_path = os.path.join(carpeta, archivo)
        try:
            if os.path.isfile(archivo_path) or os.path.islink(archivo_path):
                os.unlink(archivo_path)
            elif os.path.isdir(archivo_path):
                shutil.rmtree(archivo_path)
        except Exception as e:
            print(f"No se pudo eliminar {archivo_path}: {e}")
    print("Contenido de la carpeta eliminado exitosamente.")
else:
    print("La carpeta especificada no existe.")


carpeta_destino_relative_path = r'..\databases\shps_rural'

# Directorio base del proyecto
base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas
# Carpeta de destino
carpeta_destino = os.path.abspath(os.path.join(base_directory, carpeta_destino_relative_path))

# Inicializar QGIS
qgs = QgsApplication([], False)
qgs.initQgis()

# Carpeta de origen poner ruta servidor
#carpeta_origen = r'C:\Users\osori\Documents\BASES_GRAFICAS_SNC'

# Leer la ruta desde el archivo ruta_gdb.txt

# Imprimir el directorio actual
carpeta_ruta_relative_path = r'..\code\ruta_gdb.txt'

# Directorio base del proyecto
base_directory2 = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas
# Carpeta de destino
carpeta_destino2 = os.path.abspath(os.path.join(base_directory2, carpeta_ruta_relative_path))


with open(carpeta_destino2, "r") as archivo:
    carpeta_origen = archivo.readline().strip()



# Lista de nombres de feature classes a copiar
feature_classes_a_copiar = ['R_VEREDA', 'R_TERRENO', 'R_CONSTRUCCION', 'R_NOMENCLATURA_VIAL']

print("Copiando feature classes de Geodatabases")

# Función para cargar y copiar las feature classes deseadas
def cargar_y_copiar_feature_classes(ruta_gdb, carpeta_destino_gdb):
    # Crear la carpeta de destino para la geodatabase
    os.makedirs(carpeta_destino_gdb, exist_ok=True)

    # Cargar las feature classes
    for nombre_fc in feature_classes_a_copiar:
        ruta_fc = f"{ruta_gdb}|layername={nombre_fc}"
        fc = QgsVectorLayer(ruta_fc, nombre_fc, "ogr")
        
        if fc.isValid():
            print(f"Feature class '{nombre_fc}' cargada correctamente.")
            
            # Guardar la capa como archivo shapefile
            destino = os.path.join(carpeta_destino_gdb, f"{nombre_fc}.shp")
            QgsVectorFileWriter.writeAsVectorFormat(fc, destino, "utf-8", fc.crs(), "ESRI Shapefile")
            print(f"Copiada la feature class {nombre_fc} de la geodatabase {ruta_gdb}")
        else:
            print(f"Error al cargar la feature class {nombre_fc}.")

# Obtener lista de archivos .gdb en la carpeta de origen
for filename in os.listdir(carpeta_origen):
    if filename.endswith(".gdb"):
        gdb_origen = os.path.join(carpeta_origen, filename)
        carpeta_destino_gdb = os.path.join(carpeta_destino, filename.replace('.gdb', ''))

        # Cargar y copiar las feature classes deseadas
        cargar_y_copiar_feature_classes(gdb_origen, carpeta_destino_gdb)

# Finalizar QGIS
qgs.exitQgis()
print("Proceso completado")
