# CECUAMAQ - Sistema de Inspecciones Industriales

Sistema informático profesional para la gestión de inspecciones técnicas en plantas industriales.

## 🎯 Características Principales

- ✅ Gestión jerárquica de activos (Cliente → Planta → Ubicación → Equipo → Conjunto → Componente)
- ✅ Registro completo de inspecciones técnicas
- ✅ Parámetros de medición configurables (Temperatura, Vibración, Presión, etc.)
- ✅ Adjuntar hasta 4 fotografías por inspección
- ✅ Sistema de usuarios con roles y permisos
- ✅ Exportación a Excel
- ✅ Dashboard con indicadores KPI
- ✅ Interfaz responsive (PC, Tablet, Móvil)
- ✅ Base de datos PostgreSQL

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.10+
- **Framework UI**: Flet 0.24.1
- **Base de Datos**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Autenticación**: Passlib + Bcrypt
- **Exportación**: OpenPyXL, Pandas

## 📋 Requisitos Previos

### 1. PostgreSQL
Instalar PostgreSQL 14 o superior:
- **Windows**: Descargar desde [postgresql.org](https://www.postgresql.org/download/windows/)
- **Linux**: `sudo apt install postgresql postgresql-contrib`
- **macOS**: `brew install postgresql`

### 2. Python
Python 3.10 o superior:
- Descargar desde [python.org](https://www.python.org/downloads/)

## 🚀 Instalación

### Paso 1: Clonar el repositorio
```bash
git clone <url-repositorio>
cd cecuamaq-inspection-system
```

### Paso 2: Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Configurar base de datos

#### 4.1 Crear base de datos PostgreSQL
```bash
# Conectarse a PostgreSQL
psql -U postgres

# Ejecutar en psql:
CREATE DATABASE cecuamaq_inspections;
\q
```

#### 4.2 Ejecutar script de creación
```bash
psql -U postgres -d cecuamaq_inspections -f database_schema.sql
```

### Paso 5: Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=cecuamaq_inspections
# DB_USER=postgres
# DB_PASSWORD=tu_password
```

### Paso 6: Ejecutar la aplicación
```bash
python main.py
```

## 👤 Usuario por Defecto

Al iniciar la aplicación por primera vez, usar:
- **Usuario**: `admin`
- **Contraseña**: `Admin123!`

⚠️ **IMPORTANTE**: Cambiar esta contraseña en producción.

## 📁 Estructura del Proyecto

```
cecuamaq-inspection-system/
│
├── app/
│   ├── config/           # Configuración (BD, Settings)
│   ├── models/           # Modelos SQLAlchemy
│   ├── repositories/     # Capa de acceso a datos
│   ├── services/         # Lógica de negocio
│   ├── views/            # Vistas Flet
│   ├── components/       # Componentes reutilizables
│   └── utils/            # Utilidades
│
├── database/
│   └── init_schema.sql   # Script de creación de BD
│
├── uploads/              # Fotografías de inspecciones
├── exports/              # Archivos Excel exportados
├── logs/                 # Logs del sistema
│
├── main.py               # Archivo principal
├── requirements.txt      # Dependencias
├── .env.example          # Ejemplo de variables de entorno
└── README.md             # Este archivo
```

## 📊 Estructura de Base de Datos

### Jerarquía de Activos
```
Cliente
  └── Planta
      └── Ubicación Técnica
          └── Equipo
              └── Conjunto
                  └── Componente
```

### Tablas Principales
- `clientes` - Clientes de Cecuamaq
- `plantas` - Plantas industriales
- `ubicaciones_tecnicas` - Ubicaciones dentro de plantas
- `equipos` - Equipos industriales
- `conjuntos` - Conjuntos de equipos
- `componentes` - Componentes de conjuntos
- `inspecciones` - Inspecciones técnicas
- `parametros_inspeccion` - Catálogo de parámetros
- `inspeccion_parametros` - Valores medidos
- `inspeccion_fotos` - Fotografías adjuntas
- `usuarios` - Usuarios del sistema
- `roles` - Roles y permisos

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con Bcrypt
- ✅ Validación de sesiones
- ✅ Control de acceso basado en roles
- ✅ Validación de datos en backend
- ✅ Protección contra SQL injection (SQLAlchemy ORM)
- ✅ Logs de auditoría

## 📤 Exportación de Datos

El sistema permite exportar a Excel:
- Inspecciones por cliente/fecha/equipo
- Parámetros medidos
- Listado de equipos
- Reportes personalizados

## 🔧 Mantenimiento

### Backup de Base de Datos
```bash
pg_dump -U postgres cecuamaq_inspections > backup_$(date +%Y%m%d).sql
```

### Restaurar Base de Datos
```bash
psql -U postgres cecuamaq_inspections < backup_20240101.sql
```

### Ver Logs
```bash
# Logs del sistema
tail -f logs/cecuamaq_$(date +%Y%m%d).log
```

## 📱 Uso Multiplataforma

La aplicación funciona en:
- 💻 **Windows**: Ejecutar `main.py`
- 🐧 **Linux**: Ejecutar `python3 main.py`
- 🍎 **macOS**: Ejecutar `python3 main.py`
- 📱 **Android/iOS**: Compilar con `flet build`

## 🆘 Resolución de Problemas

### Error de conexión a PostgreSQL
```
Verificar:
1. PostgreSQL está corriendo: sudo service postgresql status
2. Credenciales en .env son correctas
3. Firewall permite conexión al puerto 5432
```

### Error al importar módulos
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### Error de permisos en carpetas
```bash
# Linux/macOS
chmod -R 755 uploads/ exports/ logs/

# Windows: Dar permisos de escritura a las carpetas
```

## 📞 Soporte

Para soporte técnico o reportar problemas:
- Email: soporte@cecuamaq.com
- Documentación: [docs.cecuamaq.com](http://docs.cecuamaq.com)

## 📄 Licencia

© 2024 Cecuamaq. Todos los derechos reservados.

## 🔄 Actualización del Sistema

```bash
# Obtener últimos cambios
git pull origin main

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Ejecutar migraciones (si las hay)
# alembic upgrade head
```

## 🎓 Capacitación

Se recomienda capacitación para:
1. **Administradores**: Gestión de usuarios y configuración
2. **Supervisores**: Creación de clientes y equipos
3. **Inspectores**: Registro de inspecciones
4. **Analistas**: Generación de reportes

---

**Versión**: 1.0.0  
**Última actualización**: Mayo 2024  
**Desarrollado por**: Cecuamaq Development Team
