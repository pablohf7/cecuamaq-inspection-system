"""
Modelo de Equipo
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class Equipment(BaseModel):
    """
    Modelo de Equipo
    Representa equipos industriales en una ubicación técnica
    """
    __tablename__ = "equipos"
    
    ubicacion_tecnica_id = Column(
        Integer, 
        ForeignKey('ubicaciones_tecnicas.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    tag = Column(String(50), index=True)
    
    # Clasificación
    equipment_type = Column(String(100), index=True)
    
    # Información técnica
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    year_manufactured = Column(Integer)
    
    # Especificaciones
    capacity = Column(String(50))
    power_rating = Column(String(50))
    voltage = Column(String(50))
    current_rating = Column(String(50))
    rpm = Column(String(50))
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    technical_location = relationship("TechnicalLocation", back_populates="equipment")
    assemblies = relationship("Assembly", back_populates="equipment", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="equipment")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def full_code(self) -> str:
        """Código completo con jerarquía"""
        if self.technical_location:
            return f"{self.technical_location.full_code}-{self.code}"
        return self.code
    
    @property
    def full_tag(self) -> str:
        """Tag completo"""
        return self.tag if self.tag else self.code
    
    @property
    def total_assemblies(self) -> int:
        """Total de conjuntos"""
        return len(self.assemblies) if self.assemblies else 0
    
    @property
    def location_path(self) -> str:
        """Ruta de ubicación completa"""
        if not self.technical_location:
            return ""
        
        location = self.technical_location
        plant = location.plant if location else None
        client = plant.client if plant else None
        
        parts = []
        if client:
            parts.append(client.name)
        if plant:
            parts.append(plant.name)
        if location:
            parts.append(location.name)
        
        return " > ".join(parts)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'ubicacion_tecnica_id': self.ubicacion_tecnica_id,
            'ubicacion_name': self.technical_location.name if self.technical_location else None,
            'code': self.code,
            'full_code': self.full_code,
            'name': self.name,
            'tag': self.tag,
            'full_tag': self.full_tag,
            'equipment_type': self.equipment_type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial_number': self.serial_number,
            'year_manufactured': self.year_manufactured,
            'capacity': self.capacity,
            'power_rating': self.power_rating,
            'voltage': self.voltage,
            'current_rating': self.current_rating,
            'rpm': self.rpm,
            'notes': self.notes,
            'is_active': self.is_active,
            'total_assemblies': self.total_assemblies,
            'location_path': self.location_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Equipment(id={self.id}, tag='{self.tag}', name='{self.name}')>"
