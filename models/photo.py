"""
Modelo de Fotografías de Inspección
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Text, CheckConstraint
from sqlalchemy.orm import relationship
from pathlib import Path

from app.models.base import BaseModel


class InspectionPhoto(BaseModel):
    """
    Modelo de Fotografía de Inspección
    Almacena hasta 4 fotografías por inspección
    """
    __tablename__ = "inspeccion_fotos"
    
    inspeccion_id = Column(
        Integer, 
        ForeignKey('inspecciones.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )
    
    # Archivo
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)  # en bytes
    
    # Información adicional
    description = Column(Text)
    photo_order = Column(Integer, default=1, nullable=False)
    
    # Usuario que subió
    uploaded_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Constraint: máximo 4 fotos
    __table_args__ = (
        CheckConstraint('photo_order >= 1 AND photo_order <= 4', name='check_photo_order'),
    )
    
    # Relaciones
    inspection = relationship("Inspection", back_populates="photos")
    uploader = relationship("User", foreign_keys=[uploaded_by])
    
    @property
    def file_size_mb(self) -> float:
        """Tamaño del archivo en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0
    
    @property
    def file_extension(self) -> str:
        """Extensión del archivo"""
        return Path(self.file_name).suffix.lower()
    
    @property
    def is_image(self) -> bool:
        """Verificar si es una imagen válida"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.file_extension in valid_extensions
    
    @property
    def full_path(self) -> str:
        """Ruta completa del archivo"""
        return self.file_path
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'inspeccion_id': self.inspeccion_id,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'file_extension': self.file_extension,
            'description': self.description,
            'photo_order': self.photo_order,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.full_name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<InspectionPhoto(id={self.id}, file='{self.file_name}', order={self.photo_order})>"
