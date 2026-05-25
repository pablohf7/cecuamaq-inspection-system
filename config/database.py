"""
Configuración de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

from app.config.settings import settings

# Logger
logger = logging.getLogger(__name__)

# Base para modelos
Base = declarative_base()

# Engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    echo=settings.is_development(),  # Log SQL en desarrollo
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Scoped session para thread-safety
ScopedSession = scoped_session(SessionLocal)


def get_db():
    """
    Obtener sesión de base de datos
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager para sesión de base de datos
    
    Usage:
        with get_db_context() as db:
            # usar db
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error en transacción de base de datos: {e}")
        raise
    finally:
        db.close()


def init_db():
    """
    Inicializar base de datos
    Crear todas las tablas definidas en los modelos
    """
    try:
        # Importar todos los modelos para que se registren
        from app.models import (
            user, client, plant, technical_location,
            equipment, assembly, component, inspection,
            parameter, photo
        )
        
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"Error al inicializar base de datos: {e}")
        raise


def check_db_connection():
    """
    Verificar conexión a base de datos
    
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Conexión a base de datos exitosa")
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {e}")
        return False


# Event listeners para logging (desarrollo)
if settings.is_development():
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        logger.debug(f"SQL: {statement}")
        logger.debug(f"Params: {params}")
