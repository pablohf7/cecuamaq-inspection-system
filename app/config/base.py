# app/config/base.py
"""
Modelo base con funcionalidad compartida
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base

# Definición única de Base (clase base declarativa de SQLAlchemy)
Base = declarative_base()


class TimestampMixin:
    """Mixin para campos de timestamp"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseModel(Base, TimestampMixin):
    """
    Modelo base abstracto con funcionalidad común
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def to_dict(self):
        """Convertir modelo a diccionario"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update(self, **kwargs):
        """Actualizar campos del modelo"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"