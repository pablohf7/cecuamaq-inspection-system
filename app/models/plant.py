"""
Modelo de Planta
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text, Numeric
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class Plant(BaseModel):
    """
    Modelo de Planta
    Representa las plantas industriales de un cliente
    """
    __tablename__ = "plantas"
    
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    
    # Ubicación
    address = Column(Text)
    city = Column(String(100))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    
    # Responsable
    manager = Column(String(200))
    phone = Column(String(20))
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    client = relationship("Client", back_populates="plants")
    technical_locations = relationship("TechnicalLocation", back_populates="plant", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="plant")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def full_code(self) -> str:
        """Código completo con cliente"""
        if self.client:
            return f"{self.client.code}-{self.code}"
        return self.code
    
    @property
    def total_locations(self) -> int:
        """Total de ubicaciones técnicas"""
        return len(self.technical_locations) if self.technical_locations else 0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_name': self.client.name if self.client else None,
            'code': self.code,
            'full_code': self.full_code,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'manager': self.manager,
            'phone': self.phone,
            'notes': self.notes,
            'is_active': self.is_active,
            'total_locations': self.total_locations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Plant(id={self.id}, code='{self.code}', name='{self.name}')>"
