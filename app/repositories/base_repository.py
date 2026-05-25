"""
Repositorio base con operaciones CRUD
"""
from typing import TypeVar, Generic, List, Optional, Type, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.config.base import BaseModel
from app.utils.logger import logger

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Repositorio base con operaciones CRUD genéricas
    """
    
    def __init__(self, model: Type[T], db: Session):
        """
        Constructor
        
        Args:
            model: Clase del modelo
            db: Sesión de base de datos
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtener por ID
        
        Args:
            id: ID del registro
            
        Returns:
            Optional[T]: Registro encontrado o None
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error al obtener {self.model.__name__} por ID {id}: {e}")
            return None
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """
        Obtener todos los registros
        
        Args:
            skip: Registros a saltar
            limit: Límite de registros
            filters: Filtros adicionales
            
        Returns:
            List[T]: Lista de registros
        """
        try:
            query = self.db.query(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key) and value is not None:
                        query = query.filter(getattr(self.model, key) == value)
            
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error al obtener {self.model.__name__}: {e}")
            return []
    
    def create(self, obj: T) -> Optional[T]:
        """
        Crear nuevo registro
        
        Args:
            obj: Objeto a crear
            
        Returns:
            Optional[T]: Objeto creado o None
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"{self.model.__name__} creado con ID {obj.id}")
            return obj
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al crear {self.model.__name__}: {e}")
            return None
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Actualizar registro
        
        Args:
            id: ID del registro
            data: Datos a actualizar
            
        Returns:
            Optional[T]: Objeto actualizado o None
        """
        try:
            obj = self.get_by_id(id)
            if not obj:
                return None
            
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"{self.model.__name__} actualizado con ID {id}")
            return obj
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al actualizar {self.model.__name__} ID {id}: {e}")
            return None
    
    def delete(self, id: int) -> bool:
        """
        Eliminar registro
        
        Args:
            id: ID del registro
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            obj = self.get_by_id(id)
            if not obj:
                return False
            
            self.db.delete(obj)
            self.db.commit()
            logger.info(f"{self.model.__name__} eliminado con ID {id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al eliminar {self.model.__name__} ID {id}: {e}")
            return False
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Contar registros
        
        Args:
            filters: Filtros opcionales
            
        Returns:
            int: Cantidad de registros
        """
        try:
            query = self.db.query(func.count(self.model.id))
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key) and value is not None:
                        query = query.filter(getattr(self.model, key) == value)
            
            return query.scalar()
        except Exception as e:
            logger.error(f"Error al contar {self.model.__name__}: {e}")
            return 0
    
    def search(self, search_term: str, search_fields: List[str], limit: int = 50) -> List[T]:
        """
        Buscar en múltiples campos
        
        Args:
            search_term: Término de búsqueda
            search_fields: Campos donde buscar
            limit: Límite de resultados
            
        Returns:
            List[T]: Resultados de la búsqueda
        """
        try:
            filters = []
            for field in search_fields:
                if hasattr(self.model, field):
                    filters.append(
                        getattr(self.model, field).ilike(f'%{search_term}%')
                    )
            
            if not filters:
                return []
            
            return self.db.query(self.model).filter(or_(*filters)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error en búsqueda de {self.model.__name__}: {e}")
            return []
    
    def exists(self, filters: Dict[str, Any]) -> bool:
        """
        Verificar si existe un registro
        
        Args:
            filters: Filtros de búsqueda
            
        Returns:
            bool: True si existe
        """
        try:
            query = self.db.query(self.model.id)
            
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
            
            return query.first() is not None
        except Exception as e:
            logger.error(f"Error al verificar existencia de {self.model.__name__}: {e}")
            return False
