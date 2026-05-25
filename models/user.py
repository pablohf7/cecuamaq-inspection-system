"""
Modelos de Usuario y Rol
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from datetime import datetime
import enum

from app.models.base import BaseModel


class UserStatus(str, enum.Enum):
    """Estados del usuario"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Role(BaseModel):
    """
    Modelo de Rol
    Define los roles y permisos del sistema
    """
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    permissions = Column(JSON, default={})
    
    # Relaciones
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class User(BaseModel):
    """
    Modelo de Usuario
    Representa a los usuarios del sistema
    """
    __tablename__ = "usuarios"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    # Rol y estado
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'))
    status = Column(
        SQLEnum(UserStatus, name='user_status'),
        default=UserStatus.ACTIVE,
        nullable=False
    )
    
    # Información adicional
    phone = Column(String(20))
    last_login = Column(DateTime)
    
    # Auditoría
    created_by = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    role = relationship("Role", back_populates="users")
    created_by_user = relationship("User", remote_side="User.id", foreign_keys=[created_by])
    
    # Relaciones inversas
    inspections = relationship("Inspection", back_populates="inspector", foreign_keys="Inspection.usuario_inspector_id")
    
    def set_password(self, password: str):
        """
        Establecer contraseña (hash)
        
        Args:
            password: Contraseña en texto plano
        """
        self.password_hash = bcrypt.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """
        Verificar contraseña
        
        Args:
            password: Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return bcrypt.verify(password, self.password_hash)
    
    def update_last_login(self):
        """Actualizar última fecha de login"""
        self.last_login = datetime.utcnow()
    
    @property
    def full_name(self) -> str:
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self) -> bool:
        """Verificar si el usuario está activo"""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_admin(self) -> bool:
        """Verificar si el usuario es administrador"""
        return self.role and self.role.name == "Administrador"
    
    def has_permission(self, permission: str) -> bool:
        """
        Verificar si el usuario tiene un permiso específico
        
        Args:
            permission: Nombre del permiso
            
        Returns:
            bool: True si tiene el permiso
        """
        if not self.role or not self.role.permissions:
            return False
        
        # Administrador tiene todos los permisos
        if self.role.permissions.get('all') is True:
            return True
        
        return permission in self.role.permissions
    
    def to_dict(self, include_sensitive=False):
        """
        Convertir a diccionario
        
        Args:
            include_sensitive: Incluir datos sensibles
            
        Returns:
            dict: Datos del usuario
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'status': self.status.value if self.status else None,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'is_admin': self.is_admin
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
        
        return data
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.name if self.role else None}')>"
