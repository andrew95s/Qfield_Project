import os

# Lista de carpetas
carpetas = [
    '17001-MANIZALES',
    '17013-AGUADAS',
    '17042-ANSERMA',
    '17050-ARANZAZU',
    '17088-BELALCAZAR',
    '17174-CHINCHINA',
    '17272-FILADELFIA',
    '17380-LA DORADA',
    '17388-LA MERCED',
    '17433-MANZANARES',
    '17442-MARMATO',
    '17444-MARQUETALIA',
    '17446-MARULANDA',
    '17486-NEIRA',
    '17495-NORCASIA',
    '17513-PACORA',
    '17524-PALESTINA',
    '17541-PENSILVANIA',
    '17614-RIOSUCIO',
    '17616-RISARALDA',
    '17653-SALAMINA',
    '17662-SAMANA',
    '17665-SAN JOSE',
    '17777-SUPIA',
    '17867-VICTORIA',
    '17873-VILLAMARIA',
    '17877-VITERBO'
]

# Directorio base
directorio_base = r'C:\Users\osori\Desktop\Qfield_Project\qfield'

# Iterar sobre las carpetas
for carpeta_nombre in carpetas:
    carpeta_path = os.path.join(directorio_base, carpeta_nombre)
    # Verificar si la carpeta existe
    if os.path.exists(carpeta_path):
        # Crear carpeta shp
        """
        shp_path = os.path.join(carpeta_path, 'shp')
        os.makedirs(shp_path, exist_ok=True)
        # Crear carpeta ortofoto
        ortofoto_path = os.path.join(carpeta_path, 'ortofoto')
        os.makedirs(ortofoto_path, exist_ok=True)
        """
        ortofoto_path = os.path.join(carpeta_path, 'imagen_rural')
        os.makedirs(ortofoto_path, exist_ok=True)
