"""
Modelo de Inspección
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Text, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import BaseModel


class InspectionStatus(str, enum.Enum):
    """Estados de inspección"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Inspection(BaseModel):
    """
    Modelo de Inspección
    Representa inspecciones técnicas realizadas
    """
    __tablename__ = "inspecciones"
    
    inspection_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Referencias jerárquicas (permite inspección a cualquier nivel)
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    planta_id = Column(Integer, ForeignKey('plantas.id', ondelete='CASCADE'), index=True)
    ubicacion_tecnica_id = Column(Integer, ForeignKey('ubicaciones_tecnicas.id', ondelete='CASCADE'), index=True)
    equipo_id = Column(Integer, ForeignKey('equipos.id', ondelete='CASCADE'), index=True)
    conjunto_id = Column(Integer, ForeignKey('conjuntos.id', ondelete='CASCADE'), index=True)
    componente_id = Column(Integer, ForeignKey('componentes.id', ondelete='CASCADE'), index=True)
    
    # Inspector
    usuario_inspector_id = Column(
        Integer, 
        ForeignKey('usuarios.id', ondelete='SET NULL'), 
        nullable=False, 
        index=True
    )
    
    # Fechas
    fecha_hora_inicio = Column(DateTime, nullable=False, index=True)
    fecha_hora_fin = Column(DateTime)
    
    # Estado y observaciones
    estado = Column(
        SQLEnum(InspectionStatus, name='inspection_status'),
        default=InspectionStatus.PENDING,
        nullable=False,
        index=True
    )
    observaciones_generales = Column(Text)
    
    # Ubicación GPS (opcional)
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    client = relationship("Client", back_populates="inspections")
    plant = relationship("Plant", back_populates="inspections")
    technical_location = relationship("TechnicalLocation", back_populates="inspections")
    equipment = relationship("Equipment", back_populates="inspections")
    assembly = relationship("Assembly", back_populates="inspections")
    component = relationship("Component", back_populates="inspections")
    inspector = relationship("User", foreign_keys=[usuario_inspector_id], back_populates="inspections")
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    # Relaciones con parámetros y fotos
    parameters = relationship("InspectionParameter", back_populates="inspection", cascade="all, delete-orphan")
    photos = relationship("InspectionPhoto", back_populates="inspection", cascade="all, delete-orphan")
    
    @property
    def duration_minutes(self) -> int:
        """Duración de la inspección en minutos"""
        if self.fecha_hora_fin and self.fecha_hora_inicio:
            delta = self.fecha_hora_fin - self.fecha_hora_inicio
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def is_completed(self) -> bool:
        """Verificar si está completada"""
        return self.estado == InspectionStatus.COMPLETED
    
    @property
    def inspection_level(self) -> str:
        """Nivel de inspección"""
        if self.componente_id:
            return "Componente"
        elif self.conjunto_id:
            return "Conjunto"
        elif self.equipo_id:
            return "Equipo"
        elif self.ubicacion_tecnica_id:
            return "Ubicación Técnica"
        elif self.planta_id:
            return "Planta"
        else:
            return "Cliente"
    
    @property
    def inspected_item_name(self) -> str:
        """Nombre del elemento inspeccionado"""
        if self.component:
            return self.component.name
        elif self.assembly:
            return self.assembly.name
        elif self.equipment:
            return self.equipment.name
        elif self.technical_location:
            return self.technical_location.name
        elif self.plant:
            return self.plant.name
        elif self.client:
            return self.client.name
        return "N/A"
    
    @property
    def total_photos(self) -> int:
        """Total de fotos adjuntas"""
        return len(self.photos) if self.photos else 0
    
    @property
    def total_parameters(self) -> int:
        """Total de parámetros registrados"""
        return len(self.parameters) if self.parameters else 0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'inspection_number': self.inspection_number,
            'cliente_id': self.cliente_id,
            'cliente_name': self.client.name if self.client else None,
            'planta_id': self.planta_id,
            'planta_name': self.plant.name if self.plant else None,
            'equipo_id': self.equipo_id,
            'equipo_name': self.equipment.name if self.equipment else None,
            'equipo_tag': self.equipment.tag if self.equipment else None,
            'usuario_inspector_id': self.usuario_inspector_id,
            'inspector_name': self.inspector.full_name if self.inspector else None,
            'fecha_hora_inicio': self.fecha_hora_inicio.isoformat() if self.fecha_hora_inicio else None,
            'fecha_hora_fin': self.fecha_hora_fin.isoformat() if self.fecha_hora_fin else None,
            'duration_minutes': self.duration_minutes,
            'estado': self.estado.value if self.estado else None,
            'observaciones_generales': self.observaciones_generales,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'inspection_level': self.inspection_level,
            'inspected_item_name': self.inspected_item_name,
            'total_photos': self.total_photos,
            'total_parameters': self.total_parameters,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Inspection(id={self.id}, number='{self.inspection_number}', status='{self.estado}')>"
