import os, sys
# Asegura que el directorio de la app está en el path
APP_DIR = os.path.dirname(__file__)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Importa 'application' desde app.py (debe existir esa variable)
from app import app as application  # 'application' es el entry point