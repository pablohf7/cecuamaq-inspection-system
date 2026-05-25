"""
Modelo de Cliente
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.base import BaseModel


class Client(BaseModel):
    """
    Modelo de Cliente
    Representa a los clientes de Cecuamaq
    """
    __tablename__ = "clientes"
    
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    ruc = Column(String(20), unique=True)
    
    # Dirección
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default='Ecuador')
    
    # Contacto
    phone = Column(String(20))
    email = Column(String(100))
    contact_person = Column(String(200))
    contact_phone = Column(String(20))
    
    # Información adicional
    notes = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    plants = relationship("Plant", back_populates="client", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="client")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    @property
    def total_plants(self) -> int:
        """Total de plantas del cliente"""
        return len(self.plants) if self.plants else 0
    
    @property
    def active_plants(self) -> int:
        """Total de plantas activas"""
        return len([p for p in self.plants if p.is_active]) if self.plants else 0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'ruc': self.ruc,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'phone': self.phone,
            'email': self.email,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'notes': self.notes,
            'is_active': self.is_active,
            'total_plants': self.total_plants,
            'active_plants': self.active_plants,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Client(id={self.id}, code='{self.code}', name='{self.name}')>"
