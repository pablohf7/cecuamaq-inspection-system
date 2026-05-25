"""
Modelos de Parámetros de Inspección
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Boolean, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class ParameterDataType(str, enum.Enum):
    """Tipo de dato del parámetro"""
    NUMERIC = "numeric"
    TEXT = "text"
    BOOLEAN = "boolean"


class InspectionParameterCatalog(BaseModel):
    """
    Catálogo de parámetros de inspección
    Define los parámetros que se pueden medir
    """
    __tablename__ = "parametros_inspeccion"
    
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    unit = Column(String(20))
    
    data_type = Column(
        SQLEnum(ParameterDataType, name='parameter_data_type'),
        default=ParameterDataType.NUMERIC,
        nullable=False
    )
    
    # Límites (para valores numéricos)
    min_limit = Column(Numeric(15, 4))
    max_limit = Column(Numeric(15, 4))
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relación con valores
    parameter_values = relationship("InspectionParameter", back_populates="parameter_catalog")
    
    @property
    def has_limits(self) -> bool:
        """Verificar si tiene límites definidos"""
        return self.min_limit is not None or self.max_limit is not None
    
    def is_within_range(self, value: float) -> bool:
        """
        Verificar si un valor está dentro del rango
        
        Args:
            value: Valor a verificar
            
        Returns:
            bool: True si está dentro del rango
        """
        if not self.has_limits:
            return True
        
        if self.min_limit is not None and value < float(self.min_limit):
            return False
        
        if self.max_limit is not None and value > float(self.max_limit):
            return False
        
        return True
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'unit': self.unit,
            'data_type': self.data_type.value if self.data_type else None,
            'min_limit': float(self.min_limit) if self.min_limit else None,
            'max_limit': float(self.max_limit) if self.max_limit else None,
            'is_active': self.is_active,
            'has_limits': self.has_limits,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<InspectionParameterCatalog(id={self.id}, code='{self.code}', name='{self.name}')>"


class InspectionParameter(BaseModel):
    """
    Valores de parámetros por inspección
    Almacena las mediciones realizadas
    """
    __tablename__ = "inspeccion_parametros"
    
    inspeccion_id = Column(
        Integer, 
        ForeignKey('inspecciones.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    parametro_id = Column(
        Integer, 
        ForeignKey('parametros_inspeccion.id', ondelete='CASCADE'), 
        nullable=False
    )
    
    # Valores (solo uno será usado según el tipo)
    valor_numerico = Column(Numeric(15, 4))
    valor_texto = Column(Text)
    valor_booleano = Column(Boolean)
    
    # Evaluación
    dentro_rango = Column(Boolean)
    observaciones = Column(Text)
    
    # Relaciones
    inspection = relationship("Inspection", back_populates="parameters")
    parameter_catalog = relationship("InspectionParameterCatalog", back_populates="parameter_values")
    
    @property
    def formatted_value(self) -> str:
        """Valor formateado con unidad"""
        if self.parameter_catalog:
            if self.parameter_catalog.data_type == ParameterDataType.NUMERIC and self.valor_numerico is not None:
                val = float(self.valor_numerico)
                unit = self.parameter_catalog.unit or ""
                return f"{val:.2f} {unit}".strip()
            elif self.parameter_catalog.data_type == ParameterDataType.BOOLEAN:
                return "Sí" if self.valor_booleano else "No"
            elif self.valor_texto:
                return self.valor_texto
        
        return "N/A"
    
    @property
    def status_text(self) -> str:
        """Texto de estado del parámetro"""
        if self.dentro_rango is None:
            return "Sin evaluar"
        return "OK" if self.dentro_rango else "Fuera de rango"
    
    @property
    def status_color(self) -> str:
        """Color de estado"""
        if self.dentro_rango is None:
            return "gray"
        return "green" if self.dentro_rango else "red"
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'inspeccion_id': self.inspeccion_id,
            'parametro_id': self.parametro_id,
            'parametro_code': self.parameter_catalog.code if self.parameter_catalog else None,
            'parametro_name': self.parameter_catalog.name if self.parameter_catalog else None,
            'parametro_unit': self.parameter_catalog.unit if self.parameter_catalog else None,
            'valor_numerico': float(self.valor_numerico) if self.valor_numerico else None,
            'valor_texto': self.valor_texto,
            'valor_booleano': self.valor_booleano,
            'formatted_value': self.formatted_value,
            'dentro_rango': self.dentro_rango,
            'status_text': self.status_text,
            'status_color': self.status_color,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<InspectionParameter(id={self.id}, param='{self.parameter_catalog.name if self.parameter_catalog else 'N/A'}')>"
