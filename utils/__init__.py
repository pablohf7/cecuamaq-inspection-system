"""
Utilidades del sistema
"""
from utils.validators import (
    validate_email,
    validate_phone,
    validate_ruc_ecuador,
    validate_code,
    validate_username,
    validate_password,
    validate_numeric_range,
    sanitize_filename
)

from utils.formatters import (
    format_date,
    format_datetime,
    format_currency,
    format_number,
    format_filesize,
    format_duration,
    format_phone,
    truncate_text,
    format_percentage,
    format_inspection_number
)

from utils.constants import (
    ROLES,
    INSPECTION_STATES,
    USER_STATES,
    EQUIPMENT_TYPES,
    ASSEMBLY_TYPES,
    COMPONENT_TYPES,
    DEFAULT_PARAMETERS,
    STATUS_COLORS,
    MAX_PHOTO_SIZE,
    MAX_PHOTOS_PER_INSPECTION,
    ALLOWED_IMAGE_FORMATS,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE
)

from utils.logger import logger, setup_logger

__all__ = [
    # Validators
    'validate_email',
    'validate_phone',
    'validate_ruc_ecuador',
    'validate_code',
    'validate_username',
    'validate_password',
    'validate_numeric_range',
    'sanitize_filename',
    # Formatters
    'format_date',
    'format_datetime',
    'format_currency',
    'format_number',
    'format_filesize',
    'format_duration',
    'format_phone',
    'truncate_text',
    'format_percentage',
    'format_inspection_number',
    # Constants
    'ROLES',
    'INSPECTION_STATES',
    'USER_STATES',
    'EQUIPMENT_TYPES',
    'ASSEMBLY_TYPES',
    'COMPONENT_TYPES',
    'DEFAULT_PARAMETERS',
    'STATUS_COLORS',
    'MAX_PHOTO_SIZE',
    'MAX_PHOTOS_PER_INSPECTION',
    'ALLOWED_IMAGE_FORMATS',
    'DEFAULT_PAGE_SIZE',
    'MAX_PAGE_SIZE',
    # Logger
    'logger',
    'setup_logger'
]
