"""
Configuración general del sistema
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "inspection_photos"
EXPORT_DIR = BASE_DIR / "exports"
LOG_DIR = BASE_DIR / "logs"

# Crear directorios si no existen
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


class Settings:
    """Configuración de la aplicación"""
    
    # Aplicación
    APP_NAME = os.getenv("APP_NAME", "Cecuamaq Inspection System")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV = os.getenv("APP_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    
    # Base de datos
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "cecuamaq_inspections")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    # Database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Rutas
    UPLOAD_PATH = str(UPLOAD_DIR)
    EXPORT_PATH = str(EXPORT_DIR)
    LOG_PATH = str(LOG_DIR)
    
    # Límites
    MAX_PHOTO_SIZE_MB = int(os.getenv("MAX_PHOTO_SIZE_MB", 5))
    MAX_PHOTOS_PER_INSPECTION = int(os.getenv("MAX_PHOTOS_PER_INSPECTION", 4))
    
    # Sesión
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", 480))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Paginación
    DEFAULT_PAGE_SIZE = 50
    
    # Formato de fechas
    DATE_FORMAT = "%d/%m/%Y"
    DATETIME_FORMAT = "%d/%m/%Y %H:%M"
    
    @classmethod
    def is_production(cls):
        return cls.APP_ENV == "production"
    
    @classmethod
    def is_development(cls):
        return cls.APP_ENV == "development"


settings = Settings()
