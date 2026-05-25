"""
Formateadores de datos
"""
from datetime import datetime
from typing import Optional
from app.config.settings import settings


def format_date(date: Optional[datetime], format_str: str = None) -> str:
    """
    Formatear fecha
    
    Args:
        date: Fecha a formatear
        format_str: Formato personalizado
        
    Returns:
        str: Fecha formateada
    """
    if not date:
        return ""
    
    if not format_str:
        format_str = settings.DATE_FORMAT
    
    return date.strftime(format_str)


def format_datetime(dt: Optional[datetime], format_str: str = None) -> str:
    """
    Formatear fecha y hora
    
    Args:
        dt: Datetime a formatear
        format_str: Formato personalizado
        
    Returns:
        str: Datetime formateado
    """
    if not dt:
        return ""
    
    if not format_str:
        format_str = settings.DATETIME_FORMAT
    
    return dt.strftime(format_str)


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Formatear moneda
    
    Args:
        amount: Monto
        currency: Moneda
        
    Returns:
        str: Monto formateado
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def format_number(number: float, decimals: int = 2) -> str:
    """
    Formatear número
    
    Args:
        number: Número a formatear
        decimals: Cantidad de decimales
        
    Returns:
        str: Número formateado
    """
    return f"{number:,.{decimals}f}"


def format_filesize(size_bytes: int) -> str:
    """
    Formatear tamaño de archivo
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        str: Tamaño formateado
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def format_duration(minutes: int) -> str:
    """
    Formatear duración en minutos a texto
    
    Args:
        minutes: Duración en minutos
        
    Returns:
        str: Duración formateada
    """
    if minutes < 60:
        return f"{minutes} min"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if mins == 0:
        return f"{hours} h"
    
    return f"{hours} h {mins} min"


def format_phone(phone: str) -> str:
    """
    Formatear número telefónico
    
    Args:
        phone: Número sin formato
        
    Returns:
        str: Número formateado
    """
    if not phone:
        return ""
    
    # Remover caracteres no numéricos
    digits = ''.join(filter(str.isdigit, phone))
    
    # Formatear según longitud
    if len(digits) == 10:  # Celular Ecuador
        return f"{digits[:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 9:  # Fijo Ecuador
        return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
    
    return phone


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncar texto
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo para texto truncado
        
    Returns:
        str: Texto truncado
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formatear porcentaje
    
    Args:
        value: Valor (0-100 o 0-1)
        decimals: Decimales
        
    Returns:
        str: Porcentaje formateado
    """
    if value <= 1:
        value *= 100
    
    return f"{value:.{decimals}f}%"


def format_inspection_number(prefix: str, sequential: int, year: int = None) -> str:
    """
    Formatear número de inspección
    
    Args:
        prefix: Prefijo (ej: INS)
        sequential: Número secuencial
        year: Año (opcional)
        
    Returns:
        str: Número de inspección formateado
    """
    if year:
        return f"{prefix}-{year}-{sequential:06d}"
    else:
        return f"{prefix}-{sequential:06d}"
