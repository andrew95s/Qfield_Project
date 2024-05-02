import os
import shutil

def limpiar_carpeta(carpeta):
    # Lista de elementos a no borrar
    elementos_a_no_borrar = ['ortofoto', 'shp']
    
    # Obtener el nombre de la carpeta consultada
    carpeta_nombre = os.path.basename(carpeta)
    elementos_a_no_borrar.append(carpeta_nombre)
    
    # Agregar el nombre del archivo que tiene el mismo nombre que la carpeta concatenado con "_Rural.qgs"
    archivo_rural = f'{carpeta_nombre}_Rural.qgs'
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
directorio_base = r'C:\Users\osori\Desktop\Qfield_Project\qfield'

# Iterar sobre las carpetas dentro del directorio base
for carpeta in os.listdir(directorio_base):
    carpeta_path = os.path.join(directorio_base, carpeta)
    # Verificar si es una carpeta
    if os.path.isdir(carpeta_path):
        # Limpiar la carpeta
        limpiar_carpeta(carpeta_path)
