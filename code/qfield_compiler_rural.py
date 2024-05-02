# Este código crea el ejecutable QField/QGIS para cada subdirectorio en qfield ====================

from qgis.core import *
import os
from pathlib import Path

# Inicializar QGIS
carpeta_ruta_relative_path = r'..\code\ruta_qgis_app_qgis.txt'

# Directorio base del proyecto
base_directory2 = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas
# Carpeta de destino
carpeta_destino2 = os.path.abspath(os.path.join(base_directory2, carpeta_ruta_relative_path))


with open(carpeta_destino2, "r") as archivo:
    carpeta_origen = archivo.readline().strip()


QgsApplication.setPrefixPath(carpeta_origen, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Configurar el entorno
project = QgsProject.instance()
project.setCrs(QgsCoordinateReferenceSystem('EPSG:3115'))  # Definir sistema de coordenadas

# Configurar GDAL para ignorar la discrepancia de proyección
os.environ['GDAL_DATA'] = os.path.join(QgsApplication.prefixPath(), 'share', 'gdal')



ruta_base_relative_path = r'..\qfield'

# Directorio base del proyecto
base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas
# Carpeta de destino
ruta_basepath = os.path.abspath(os.path.join(base_directory, ruta_base_relative_path))

import shutil

def limpiar_carpeta(carpeta):
    # Lista de elementos a no borrar
    elementos_a_no_borrar = ['ortofoto', 'shp',"imagen_rural"]
    
    # Obtener el nombre de la carpeta consultada
    carpeta_nombre = os.path.basename(carpeta)
    elementos_a_no_borrar.append(carpeta_nombre)
    
    # Agregar el nombre del archivo que tiene el mismo nombre que la carpeta concatenado con "_Rural.qgs"
    archivo_rural = f'{carpeta_nombre}_Urbano.qgs'
    elementos_a_no_borrar.append(archivo_rural)
    
    # Iterar sobre los elementos de la carpeta
    for elemento in os.listdir(carpeta):
        # Ruta completa del elemento
        elemento_path = os.path.join(carpeta, elemento)
        
        # Verificar si es una carpeta
        if os.path.isdir(elemento_path):
            # Si el nombre de la carpeta no está en la lista de elementos a no borrar
            if elemento not in elementos_a_no_borrar:
                # Borrar el contenido de la carpeta (recursivamente)
                shutil.rmtree(elemento_path)
        # Verificar si es un archivo
        elif os.path.isfile(elemento_path):
            # Si el nombre del archivo no está en la lista de elementos a no borrar
            if elemento not in elementos_a_no_borrar:
                # Borrar el archivo
                os.remove(elemento_path)

# Directorio base
directorio_base = ruta_basepath

# Iterar sobre las carpetas dentro del directorio base
for carpeta in os.listdir(directorio_base):
    carpeta_path = os.path.join(directorio_base, carpeta)
    # Verificar si es una carpeta
    if os.path.isdir(carpeta_path):
        # Limpiar la carpeta
        limpiar_carpeta(carpeta_path)

#=====================================================================================================

# Ruta base
ruta_base = Path(ruta_basepath)

# Recorrer las subcarpetas dentro de la ruta base
for subcarpeta in ruta_base.iterdir():
    if subcarpeta.is_dir():
        print(f"Procesando subcarpeta: {subcarpeta.name}")

        # Limpiar el proyecto
        project.removeAllMapLayers()

        # Cargar la ortofoto
        ruta_ortofoto = subcarpeta / "imagen_rural"
        for archivo in ruta_ortofoto.iterdir():
            if archivo.suffix.lower() in [".tif", ".ecw", ".jp2"]:
                capa_ortofoto = QgsRasterLayer(str(archivo), "Ortofoto")
                if capa_ortofoto.isValid():
                    print("Ortofoto cargada correctamente.")

                    # Aplicar transparencia para valores de píxeles de negro absoluto
                    transparency = capa_ortofoto.renderer().rasterTransparency()
                    pixel = QgsRasterTransparency.TransparentThreeValuePixel()
                    pixel.red = 0
                    pixel.green = 0
                    pixel.blue = 0
                    pixel.percentTransparent = 100
                    transparency.setTransparentThreeValuePixelList([pixel])
                    capa_ortofoto.triggerRepaint()

                    project.addMapLayer(capa_ortofoto)
                else:
                    print("Error al cargar la ortofoto.")

        # Cargar los shapefiles
        ruta_shp = subcarpeta / "shp"
        nombres_shapefiles = ["R_VEREDA", "R_TERRENO", "R_CONSTRUCCION", "R_NOMENCLATURA_VIAL"]
        for nombre_shp in nombres_shapefiles:
            ruta_shp_completa = ruta_shp / f"{nombre_shp}.shp"
            if ruta_shp_completa.exists():
                capa_shp = QgsVectorLayer(str(ruta_shp_completa), nombre_shp, "ogr")
                if capa_shp.isValid():
                    print(f"Shapefile '{nombre_shp}' cargado correctamente.")
                    project.addMapLayer(capa_shp)

                    carpeta_estilo_relative_path = r'..\qfield_estilos'

                    # Directorio base del proyecto
                    base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

                    # Rutas absolutas
                    # Carpeta de destino
                    carpeta_estilo = os.path.abspath(os.path.join(base_directory, carpeta_estilo_relative_path))


                    # Aplicar el estilo
                    ruta_estilo = Path(carpeta_estilo) / f"{nombre_shp}.qml"
                    if ruta_estilo.exists():
                        capa_shp.loadNamedStyle(str(ruta_estilo))
                        capa_shp.triggerRepaint()
                else:
                    print(f"Error al cargar el shapefile {nombre_shp}.")

        # Guardar el proyecto en la subcarpeta
        nombre_proyecto = f"{subcarpeta.name}_Rural.qgs"
        ruta_salida_proyecto = subcarpeta / nombre_proyecto
        project.write(str(ruta_salida_proyecto))
        print(f"Proyecto guardado en: {ruta_salida_proyecto}")

# Cerrar QGIS
qgs.exitQgis()