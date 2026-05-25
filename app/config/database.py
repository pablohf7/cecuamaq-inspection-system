"""
Configuración de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine, event, text   # <-- agregar text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

from app.config.settings import settings
from app.config.base import Base   # <-- importar Base desde base.py

# Logger
logger = logging.getLogger(__name__)

# Engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=settings.is_development(),
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

ScopedSession = scoped_session(SessionLocal)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
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
    """Inicializar base de datos: crear todas las tablas"""
    try:
        # Importar modelos aquí (dentro de la función) para evitar circularidad
        from app.models import user   # y otros modelos que necesites
        # Si tienes más modelos, impórtalos también (assembly, client, etc.)
        from app.models import assembly, client, component, equipment, inspection, parameter, photo, plant, technical_location

        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar base de datos: {e}")
        raise

def check_db_connection():
    """Verificar conexión a base de datos"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))   # <-- usar text()
        logger.info("Conexión a base de datos exitosa")
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {e}")
        return False

# Event listeners (sin cambios)
if settings.is_development():
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        logger.debug(f"SQL: {statement}")
        logger.debug(f"Params: {params}")