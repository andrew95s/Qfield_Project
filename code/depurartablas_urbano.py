#============codigo que depura la informacion de las tablas =================================================
import os
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsApplication

# Inicializar QGIS
qgs = QgsApplication([], False)
qgs.initQgis()

carpeta_destino_relative_path = r'..\databases\shps_urbano'

# Directorio base del proyecto
base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas
# Carpeta de destino
carpeta_destino = os.path.abspath(os.path.join(base_directory, carpeta_destino_relative_path))

# Lista de columnas a eliminar para cada tipo de shapefile
columnas_a_eliminar = {
    'U_NOMENCLATURA_VIAL': ['Shape', 'USUARIO_LO', 'FECHA_LOG', 'GLOBALID_S', 'GLOBALID', 'CODIGO_MUN'],
    'U_CONSTRUCCION': ['Shape', 'OBJECTID', 'USUARIO_LO', 'FECHA_LOG', 'GLOBALID_S', 'GLOBALID', 'CODIGO_MUN'],
    'U_MANZANA': ['Shape', 'OBJECTID', 'USUARIO_LO', 'FECHA_LOG', 'GLOBALID_S', 'GLOBALID', 'SHAPE_Leng', 'CODIGO_MUN'],
    'U_TERRENO': ['Shape', 'OBJECTID', 'NUMERO_SUB', 'USUARIO_LO', 'FECHA_LOG', 'GLOBALID_S', 'GLOBALID', 'CODIGO_MUN', 'SHAPE_Leng']
}

# Función para eliminar las columnas especificadas de un shapefile
def eliminar_columnas_shapefile(ruta_shapefile, columnas):
    # Cargar el shapefile
    layer = QgsVectorLayer(ruta_shapefile, "", "ogr")

    if layer.isValid():
        # Obtener los nombres de las columnas actuales
        nombres_columnas = [field.name() for field in layer.fields()]

        # Eliminar las columnas especificadas
        columnas_a_eliminar = [col for col in columnas if col in nombres_columnas]
        layer.dataProvider().deleteAttributes([layer.fields().lookupField(col) for col in columnas_a_eliminar])

        # Guardar los cambios
        layer.updateFields()

        # Guardar el shapefile
        QgsVectorFileWriter.writeAsVectorFormat(layer, ruta_shapefile, "utf-8", layer.crs(), "ESRI Shapefile")
        print(f"Columnas eliminadas en {ruta_shapefile}")
    else:
        print(f"Error al cargar {ruta_shapefile}")

# Recorrer cada carpeta dentro de la carpeta de destino
for carpeta in os.listdir(carpeta_destino):
    carpeta_path = os.path.join(carpeta_destino, carpeta)
    if os.path.isdir(carpeta_path):
        # Recorrer cada shapefile dentro de la carpeta
        for shapefile in os.listdir(carpeta_path):
            shapefile_path = os.path.join(carpeta_path, shapefile)
            if shapefile.endswith(".shp") and os.path.isfile(shapefile_path):
                # Obtener el tipo de shapefile (U_NOMENCLATURA_VIAL, U_CONSTRUCCION, etc.)
                tipo_shapefile = os.path.splitext(shapefile)[0]

                # Verificar si hay columnas para eliminar para este tipo de shapefile
                if tipo_shapefile in columnas_a_eliminar:
                    # Eliminar las columnas especificadas para este shapefile
                    eliminar_columnas_shapefile(shapefile_path, columnas_a_eliminar[tipo_shapefile])

# Finalizar QGIS
qgs.exitQgis()
print("Proceso completado")
