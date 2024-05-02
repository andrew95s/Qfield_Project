import os
import shutil

#====== borar datos antiguos=====
directorio_base = os.path.join(os.path.dirname(__file__), "..", "qfield")

"""
# Función para borrar el contenido de las carpetas shp
def borrar_contenido_shp(directorio):
    for root, dirs, files in os.walk(directorio):
        for d in dirs:
            if d.lower() == "shp":
                dir_shp = os.path.join(root, d)
                for archivo in os.listdir(dir_shp):
                    archivo_path = os.path.join(dir_shp, archivo)
                    try:
                        if os.path.isfile(archivo_path):
                            os.unlink(archivo_path)
                    except Exception as e:
                        print(e)

# Iterar sobre cada carpeta dentro del directorio base
for root, dirs, files in os.walk(directorio_base):
    for d in dirs:
        # Ruta completa de la carpeta
        carpeta = os.path.join(root, d)
        # Borrar contenido de las carpetas shp dentro de esta carpeta
        borrar_contenido_shp(carpeta)
print("Datos antiguos borados con exit")
"""

carpeta_origen_relative_path = r'..\databases\shps_urbano'
carpeta_destino_relative_path = r'..\qfield'

# Directorio base del proyecto
base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual

# Rutas absolutas

# Carpetas
origen = os.path.abspath(os.path.join(base_directory, carpeta_origen_relative_path))
destino = os.path.abspath(os.path.join(base_directory, carpeta_destino_relative_path))

print(origen)
print(destino)

# Directorios de origen y destino
#origen = r"C:\Users\osori\Desktop\Qfield_Project\databases\shps_urbano"
#destino = r"C:\Users\osori\Desktop\Qfield_Project\qfield"

# Obtener lista de carpetas en el directorio de origen
carpetas_origen = [nombre for nombre in os.listdir(origen) if os.path.isdir(os.path.join(origen, nombre))]

# Obtener lista de carpetas en el directorio de destino
carpetas_destino = [nombre for nombre in os.listdir(destino) if os.path.isdir(os.path.join(destino, nombre))]

# Función para copiar el contenido de una carpeta de origen a una de destino
def copiar_contenido(origen_carpeta, destino_carpeta):
    contenido_origen = os.listdir(origen_carpeta)
    for item in contenido_origen:
        origen_item = os.path.join(origen_carpeta, item)
        destino_item = os.path.join(destino_carpeta, item)
        if os.path.isdir(origen_item):
            shutil.copytree(origen_item, destino_item)
        else:
            shutil.copy2(origen_item, destino_item)

# Iterar sobre las carpetas de origen
for carpeta in carpetas_origen:
    # Verificar si el nombre de la carpeta tiene exactamente 5 dígitos
    if carpeta.isdigit() and len(carpeta) == 5:
        # Iterar sobre las carpetas de destino
        for carpeta_destino in carpetas_destino:
            # Comparar los primeros 5 dígitos del nombre de la carpeta de origen con las de destino
            if carpeta[:5] == carpeta_destino[:5]:
                # Construir las rutas completas de origen y destino
                origen_carpeta = os.path.join(origen, carpeta)
                destino_carpeta = os.path.join(destino, carpeta_destino, "shp")
                # Copiar el contenido de la carpeta de origen a la carpeta de destino en qfield
                copiar_contenido(origen_carpeta, destino_carpeta)

print("Proceso completado.")
