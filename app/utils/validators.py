"""
Validadores para datos del sistema
"""
import re
from typing import Optional
from email_validator import validate_email as _validate_email, EmailNotValidError
import phonenumbers


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validar formato de email
    
    Args:
        email: Email a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not email:
        return False, "El email es requerido"
    
    try:
        _validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone(phone: str, country_code: str = "EC") -> tuple[bool, Optional[str]]:
    """
    Validar número telefónico
    
    Args:
        phone: Número a validar
        country_code: Código de país (default: Ecuador)
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not phone:
        return True, None  # Teléfono es opcional
    
    try:
        parsed = phonenumbers.parse(phone, country_code)
        if phonenumbers.is_valid_number(parsed):
            return True, None
        else:
            return False, "Número de teléfono inválido"
    except phonenumbers.NumberParseException:
        return False, "Formato de teléfono inválido"


def validate_ruc_ecuador(ruc: str) -> tuple[bool, Optional[str]]:
    """
    Validar RUC ecuatoriano
    
    Args:
        ruc: RUC a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not ruc:
        return True, None  # RUC es opcional
    
    # Remover espacios
    ruc = ruc.strip().replace(" ", "")
    
    # Debe tener 13 dígitos
    if not ruc.isdigit() or len(ruc) != 13:
        return False, "El RUC debe tener 13 dígitos"
    
    # Los 3 últimos dígitos deben ser 001
    if not ruc.endswith("001"):
        return False, "El RUC debe terminar en 001"
    
    return True, None


def validate_code(code: str, min_length: int = 1, max_length: int = 20) -> tuple[bool, Optional[str]]:
    """
    Validar código alfanumérico
    
    Args:
        code: Código a validar
        min_length: Longitud mínima
        max_length: Longitud máxima
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not code:
        return False, "El código es requerido"
    
    code = code.strip()
    
    if len(code) < min_length:
        return False, f"El código debe tener al menos {min_length} caracteres"
    
    if len(code) > max_length:
        return False, f"El código no puede exceder {max_length} caracteres"
    
    # Solo alfanuméricos, guiones y guiones bajos
    if not re.match(r'^[A-Za-z0-9_-]+$', code):
        return False, "El código solo puede contener letras, números, guiones y guiones bajos"
    
    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validar nombre de usuario
    
    Args:
        username: Usuario a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not username:
        return False, "El nombre de usuario es requerido"
    
    username = username.strip()
    
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if len(username) > 50:
        return False, "El nombre de usuario no puede exceder 50 caracteres"
    
    # Solo alfanuméricos y guiones bajos
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validar fortaleza de contraseña
    
    Args:
        password: Contraseña a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(password) > 100:
        return False, "La contraseña no puede exceder 100 caracteres"
    
    # Debe contener al menos una mayúscula
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    # Debe contener al menos una minúscula
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    # Debe contener al menos un número
    if not re.search(r'[0-9]', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, None


def validate_numeric_range(
    value: float, 
    min_value: Optional[float] = None, 
    max_value: Optional[float] = None
) -> tuple[bool, Optional[str]]:
    """
    Validar que un valor numérico esté en un rango
    
    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if min_value is not None and value < min_value:
        return False, f"El valor debe ser mayor o igual a {min_value}"
    
    if max_value is not None and value > max_value:
        return False, f"El valor debe ser menor o igual a {max_value}"
    
    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitizar nombre de archivo
    
    Args:
        filename: Nombre de archivo original
        
    Returns:
        str: Nombre de archivo sanitizado
    """
    # Remover caracteres no permitidos
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Reemplazar espacios con guiones bajos
    filename = re.sub(r'\s+', '_', filename)
    # Limitar longitud
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 100:
        name = name[:100]
    
    return f"{name}.{ext}" if ext else name
