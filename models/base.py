"""
Modelo base con funcionalidad compartida
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

from app.config.database import Base


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
        """
        Convertir modelo a diccionario
        
        Returns:
            dict: Diccionario con los datos del modelo
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update(self, **kwargs):
        """
        Actualizar campos del modelo
        
        Args:
            **kwargs: Campos a actualizar
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        """Representación del objeto"""
        return f"<{self.__class__.__name__}(id={self.id})>"
