"""
Constantes del sistema
"""

# Roles predefinidos
ROLES = {
    'ADMIN': 'Administrador',
    'SUPERVISOR': 'Supervisor',
    'INSPECTOR': 'Inspector',
    'VIEWER': 'Consulta'
}

# Estados de inspección
INSPECTION_STATES = {
    'PENDING': 'Pendiente',
    'IN_PROGRESS': 'En Progreso',
    'COMPLETED': 'Completada',
    'CANCELLED': 'Cancelada'
}

# Estados de usuario
USER_STATES = {
    'ACTIVE': 'Activo',
    'INACTIVE': 'Inactivo',
    'SUSPENDED': 'Suspendido'
}

# Tipos de equipos comunes
EQUIPMENT_TYPES = [
    'Bomba Centrífuga',
    'Bomba de Desplazamiento Positivo',
    'Motor Eléctrico',
    'Compresor',
    'Ventilador',
    'Turbina',
    'Generador',
    'Transformador',
    'Válvula',
    'Intercambiador de Calor',
    'Reactor',
    'Tanque',
    'Otro'
]

# Tipos de conjuntos
ASSEMBLY_TYPES = [
    'Motor Eléctrico',
    'Caja Reductora',
    'Acoplamiento',
    'Sistema de Lubricación',
    'Sistema de Enfriamiento',
    'Sistema de Sellado',
    'Rodamientos',
    'Impulsor',
    'Eje',
    'Otro'
]

# Tipos de componentes
COMPONENT_TYPES = [
    'Rodamiento',
    'Sello Mecánico',
    'Empaquetadura',
    'O-Ring',
    'Impulsor',
    'Difusor',
    'Eje',
    'Acoplamiento',
    'Engranaje',
    'Bobina',
    'Contacto Eléctrico',
    'Otro'
]

# Parámetros de inspección predefinidos
DEFAULT_PARAMETERS = [
    {'code': 'TEMP', 'name': 'Temperatura', 'unit': '°C', 'data_type': 'numeric'},
    {'code': 'VIB', 'name': 'Vibración', 'unit': 'mm/s', 'data_type': 'numeric'},
    {'code': 'PRES', 'name': 'Presión', 'unit': 'PSI', 'data_type': 'numeric'},
    {'code': 'COR', 'name': 'Corriente', 'unit': 'A', 'data_type': 'numeric'},
    {'code': 'VOLT', 'name': 'Voltaje', 'unit': 'V', 'data_type': 'numeric'},
    {'code': 'RPM', 'name': 'Revoluciones', 'unit': 'RPM', 'data_type': 'numeric'},
    {'code': 'ESP', 'name': 'Espesor', 'unit': 'mm', 'data_type': 'numeric'},
    {'code': 'NIV-ACE', 'name': 'Nivel de Aceite', 'unit': '%', 'data_type': 'numeric'},
    {'code': 'RUIDO', 'name': 'Ruido', 'unit': 'dB', 'data_type': 'numeric'},
    {'code': 'FUGA', 'name': 'Fuga', 'unit': '', 'data_type': 'boolean'},
]

# Colores de estado
STATUS_COLORS = {
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
    'default': '#9E9E9E'
}

# Tamaños de archivo permitidos
MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_PHOTOS_PER_INSPECTION = 4

# Formatos de imagen permitidos
ALLOWED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

# Paginación
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200

# Prefijos
INSPECTION_NUMBER_PREFIX = 'INS'
CLIENT_CODE_PREFIX = 'CLI'
PLANT_CODE_PREFIX = 'PLT'
