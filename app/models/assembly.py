"""
Modelo de Conjunto (Assembly)
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class Assembly(BaseModel):
    """
    Modelo de Conjunto
    Representa conjuntos dentro de un equipo
    """
    __tablename__ = "conjuntos"
    
    equipo_id = Column(Integer, ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Clasificación
    assembly_type = Column(String(100))
    position = Column(String(50))
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    equipment = relationship("Equipment", back_populates="assemblies")
    components = relationship("Component", back_populates="assembly", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="assembly")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def full_code(self) -> str:
        """Código completo con jerarquía"""
        if self.equipment:
            return f"{self.equipment.full_code}-{self.code}"
        return self.code
    
    @property
    def total_components(self) -> int:
        """Total de componentes"""
        return len(self.components) if self.components else 0
    
    @property
    def equipment_tag(self) -> str:
        """Tag del equipo padre"""
        return self.equipment.tag if self.equipment else ""
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'equipo_id': self.equipo_id,
            'equipo_name': self.equipment.name if self.equipment else None,
            'equipo_tag': self.equipment_tag,
            'code': self.code,
            'full_code': self.full_code,
            'name': self.name,
            'description': self.description,
            'assembly_type': self.assembly_type,
            'position': self.position,
            'notes': self.notes,
            'is_active': self.is_active,
            'total_components': self.total_components,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Assembly(id={self.id}, code='{self.code}', name='{self.name}')>"
