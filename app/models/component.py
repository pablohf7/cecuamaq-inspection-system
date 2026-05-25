"""
Modelo de Componente
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class Component(BaseModel):
    """
    Modelo de Componente
    Representa componentes dentro de un conjunto
    """
    __tablename__ = "componentes"
    
    conjunto_id = Column(Integer, ForeignKey('conjuntos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Clasificación
    component_type = Column(String(100))
    material = Column(String(100))
    part_number = Column(String(100))
    quantity = Column(Integer, default=1)
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    assembly = relationship("Assembly", back_populates="components")
    inspections = relationship("Inspection", back_populates="component")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def full_code(self) -> str:
        """Código completo con jerarquía"""
        if self.assembly:
            return f"{self.assembly.full_code}-{self.code}"
        return self.code
    
    @property
    def assembly_name(self) -> str:
        """Nombre del conjunto padre"""
        return self.assembly.name if self.assembly else ""
    
    @property
    def equipment_tag(self) -> str:
        """Tag del equipo"""
        if self.assembly and self.assembly.equipment:
            return self.assembly.equipment.tag
        return ""
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'conjunto_id': self.conjunto_id,
            'conjunto_name': self.assembly_name,
            'equipo_tag': self.equipment_tag,
            'code': self.code,
            'full_code': self.full_code,
            'name': self.name,
            'description': self.description,
            'component_type': self.component_type,
            'material': self.material,
            'part_number': self.part_number,
            'quantity': self.quantity,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Component(id={self.id}, code='{self.code}', name='{self.name}')>"
