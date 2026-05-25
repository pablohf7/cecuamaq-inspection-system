"""
Servicio de Autenticación
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import User, Role
from app.utils import logger, validate_username, validate_password
from passlib.hash import bcrypt


class AuthService:
    """Servicio de autenticación y gestión de sesiones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Autenticar usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            tuple: (exitoso, usuario, mensaje_error)
        """
        try:
            # Validar formato
            valid, error = validate_username(username)
            if not valid:
                return False, None, error
            
            # Buscar usuario
            user = self.db.query(User).filter(User.username == username).first()
            
            if not user:
                logger.warning(f"Intento de login con usuario inexistente: {username}")
                return False, None, "Usuario o contraseña incorrectos"
            
            # Verificar contraseña
            if not user.verify_password(password):
                logger.warning(f"Contraseña incorrecta para usuario: {username}")
                return False, None, "Usuario o contraseña incorrectos"
            
            # Verificar estado del usuario
            if not user.is_active:
                logger.warning(f"Intento de login con usuario inactivo: {username}")
                return False, None, "Usuario inactivo. Contacte al administrador"
            
            # Actualizar última fecha de login
            user.update_last_login()
            self.db.commit()
            
            logger.info(f"Login exitoso: {username}")
            return True, user, None
            
        except Exception as e:
            logger.error(f"Error en login: {e}")
            return False, None, "Error al procesar login"
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role_id: int,
        created_by_id: int,
        phone: Optional[str] = None
    ) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Crear nuevo usuario
        
        Args:
            username: Nombre de usuario
            email: Email
            password: Contraseña
            first_name: Nombre
            last_name: Apellido
            role_id: ID del rol
            created_by_id: ID del usuario creador
            phone: Teléfono (opcional)
            
        Returns:
            tuple: (exitoso, usuario, mensaje_error)
        """
        try:
            # Validar username
            valid, error = validate_username(username)
            if not valid:
                return False, None, error
            
            # Validar password
            valid, error = validate_password(password)
            if not valid:
                return False, None, error
            
            # Verificar que no exista el username
            if self.db.query(User).filter(User.username == username).first():
                return False, None, "El nombre de usuario ya existe"
            
            # Verificar que no exista el email
            if self.db.query(User).filter(User.email == email).first():
                return False, None, "El email ya está registrado"
            
            # Verificar que existe el rol
            role = self.db.query(Role).filter(Role.id == role_id).first()
            if not role:
                return False, None, "Rol inválido"
            
            # Crear usuario
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role_id=role_id,
                phone=phone,
                created_by=created_by_id
            )
            user.set_password(password)
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"Usuario creado: {username}")
            return True, user, None
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al crear usuario: {e}")
            return False, None, f"Error al crear usuario: {str(e)}"
    
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Cambiar contraseña de usuario
        
        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            tuple: (exitoso, mensaje_error)
        """
        try:
            # Buscar usuario
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "Usuario no encontrado"
            
            # Verificar contraseña actual
            if not user.verify_password(old_password):
                return False, "Contraseña actual incorrecta"
            
            # Validar nueva contraseña
            valid, error = validate_password(new_password)
            if not valid:
                return False, error
            
            # Cambiar contraseña
            user.set_password(new_password)
            self.db.commit()
            
            logger.info(f"Contraseña cambiada para usuario: {user.username}")
            return True, None
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al cambiar contraseña: {e}")
            return False, f"Error al cambiar contraseña: {str(e)}"
    
    def get_user_permissions(self, user_id: int) -> dict:
        """
        Obtener permisos del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            dict: Permisos del usuario
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.role:
                return {}
            
            return user.role.permissions or {}
            
        except Exception as e:
            logger.error(f"Error al obtener permisos: {e}")
            return {}
