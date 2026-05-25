"""
Modelo de Ubicación Técnica
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class TechnicalLocation(BaseModel):
    """
    Modelo de Ubicación Técnica
    Representa ubicaciones dentro de una planta
    """
    __tablename__ = "ubicaciones_tecnicas"
    
    planta_id = Column(Integer, ForeignKey('plantas.id', ondelete='CASCADE'), nullable=False, index=True)
    
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Organización
    area = Column(String(100))
    department = Column(String(100))
    responsible = Column(String(200))
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    plant = relationship("Plant", back_populates="technical_locations")
    equipment = relationship("Equipment", back_populates="technical_location", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="technical_location")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def full_code(self) -> str:
        """Código completo con planta y cliente"""
        if self.plant and self.plant.client:
            return f"{self.plant.client.code}-{self.plant.code}-{self.code}"
        return self.code
    
    @property
    def total_equipment(self) -> int:
        """Total de equipos"""
        return len(self.equipment) if self.equipment else 0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'planta_id': self.planta_id,
            'planta_name': self.plant.name if self.plant else None,
            'cliente_name': self.plant.client.name if self.plant and self.plant.client else None,
            'code': self.code,
            'full_code': self.full_code,
            'name': self.name,
            'description': self.description,
            'area': self.area,
            'department': self.department,
            'responsible': self.responsible,
            'notes': self.notes,
            'is_active': self.is_active,
            'total_equipment': self.total_equipment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<TechnicalLocation(id={self.id}, code='{self.code}', name='{self.name}')>"
