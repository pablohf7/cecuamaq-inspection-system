# ARQUITECTURA DEL SISTEMA CECUAMAQ

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│                         (Flet UI)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Login   │  │Dashboard │  │ Clientes │  │  CRUD    │   │
│  │  View    │  │  View    │  │  View    │  │  Views   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│               CAPA DE LÓGICA DE NEGOCIO                      │
│                      (Services)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │  Client  │  │Inspection│  │  Export  │   │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│             CAPA DE ACCESO A DATOS                           │
│                   (Repositories)                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Base   │  │   User   │  │  Client  │  │Inspection│   │
│  │   Repo   │  │   Repo   │  │   Repo   │  │   Repo   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                  CAPA DE MODELOS                             │
│                   (SQLAlchemy ORM)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   User   │  │  Client  │  │  Plant   │  │Equipment │   │
│  │  Model   │  │  Model   │  │  Model   │  │  Model   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                BASE DE DATOS PostgreSQL                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tablas: usuarios, roles, clientes, plantas,         │  │
│  │  equipos, inspecciones, parametros, fotos            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## 🏛️ Patrones de Diseño

### 1. MVC (Model-View-Controller)
- **Models**: Definición de entidades y lógica de dominio
- **Views**: Interfaces de usuario en Flet
- **Controllers**: Servicios que coordinan vistas y modelos

### 2. Repository Pattern
- Abstracción de acceso a datos
- CRUD genérico en BaseRepository
- Repositorios específicos para cada entidad

### 3. Service Layer
- Lógica de negocio centralizada
- Validaciones y reglas de negocio
- Orquestación de operaciones complejas

### 4. Dependency Injection
- Inyección de sesiones de BD
- Facilita testing y mantenibilidad

## 📊 Modelo Entidad-Relación

```
┌────────────┐
│  usuarios  │
└─────┬──────┘
      │ 1:N
      │
┌─────┴──────────┐
│  inspecciones  │
└─────┬──────────┘
      │ 1:N
      ├──────────┐
      │          │
┌─────┴────┐  ┌─┴────────┐
│parametros│  │  fotos   │
└──────────┘  └──────────┘

┌──────────┐
│ clientes │
└─────┬────┘
      │ 1:N
┌─────┴────┐
│ plantas  │
└─────┬────┘
      │ 1:N
┌─────┴──────────────┐
│ubicaciones_tecnicas│
└─────┬──────────────┘
      │ 1:N
┌─────┴────┐
│ equipos  │
└─────┬────┘
      │ 1:N
┌─────┴────┐
│conjuntos │
└─────┬────┘
      │ 1:N
┌─────┴──────┐
│componentes │
└────────────┘
```

## 🔐 Seguridad

### Autenticación
- Hash de contraseñas con Bcrypt (factor 12)
- Validación de credenciales en AuthService
- Sesión de usuario en memoria

### Autorización
- Sistema de roles (Admin, Supervisor, Inspector, Consulta)
- Permisos basados en JSON
- Control de acceso en servicios

### Validación de Datos
- Validaciones en capa de servicios
- Validadores específicos (email, teléfono, RUC)
- Sanitización de entradas

## 📁 Flujo de Datos

### Crear Inspección
```
1. Usuario → InspectionView.create()
2. InspectionView → InspectionService.create_inspection()
3. InspectionService → Validar datos
4. InspectionService → InspectionRepository.create()
5. InspectionRepository → DB.insert()
6. DB → Return inspection_id
7. Return → InspectionView (actualizar UI)
```

### Exportar a Excel
```
1. Usuario → ReportView.export()
2. ReportView → ExportService.export_inspections()
3. ExportService → InspectionRepository.get_all(filters)
4. Repository → DB.query()
5. ExportService → Generate Excel (openpyxl)
6. ExportService → Save file
7. Return → ReportView (mostrar confirmación)
```

## 🗄️ Gestión de Datos

### Base de Datos
- **Motor**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Pool**: QueuePool (size=10, max_overflow=20)
- **Migraciones**: Alembic (opcional)

### Transacciones
- Commit automático en operaciones exitosas
- Rollback en excepciones
- Context managers para transacciones complejas

### Índices
- Claves primarias (id)
- Claves foráneas
- Índices en campos de búsqueda frecuente
- Índices únicos en códigos

## 📦 Módulos Principales

### app/config
- `settings.py`: Configuración global
- `database.py`: Conexión y sesiones de BD

### app/models
- Modelos SQLAlchemy
- Relaciones entre entidades
- Propiedades calculadas

### app/repositories
- `base_repository.py`: CRUD genérico
- Repositorios específicos por entidad

### app/services
- `auth_service.py`: Autenticación
- `inspection_service.py`: Lógica de inspecciones
- `export_service.py`: Exportación de datos

### app/views
- Vistas Flet para cada módulo
- Componentes de UI reutilizables

### app/utils
- `validators.py`: Validadores
- `formatters.py`: Formateadores
- `logger.py`: Sistema de logging

## 🚀 Escalabilidad

### Vertical
- Pool de conexiones a BD
- Caché de consultas frecuentes
- Índices optimizados

### Horizontal
- Arquitectura modular
- Servicios separables
- API REST (futura implementación)

## 🔄 Ciclo de Vida de Desarrollo

```
1. Análisis → Diseño de BD y modelos
2. Desarrollo → Implementación de capas
3. Testing → Pruebas unitarias y de integración
4. Deployment → Instalación en cliente
5. Mantenimiento → Correcciones y mejoras
```

## 📈 Monitoreo

### Logs
- Nivel: INFO en producción, DEBUG en desarrollo
- Formato: Timestamp + Level + Module + Message
- Archivo diario rotativo

### Auditoría
- Tabla `audit_log` para cambios críticos
- Registro de usuario, acción y datos
- Consulta para reportes de auditoría

## 🔧 Mantenibilidad

### Código
- PEP 8 (estilo de código Python)
- Type hints para mejor documentación
- Docstrings en funciones públicas

### Base de Datos
- Migraciones versionadas (Alembic)
- Scripts de backup automatizados
- Constraints para integridad referencial

### Testing
- Unit tests para servicios
- Integration tests para BD
- E2E tests para flujos críticos

## 🌐 Deployment

### Entornos
1. **Desarrollo**: BD local, logs DEBUG
2. **Staging**: BD de pruebas, logs INFO
3. **Producción**: BD producción, logs WARNING

### Checklist de Deployment
- [ ] Variables de entorno configuradas
- [ ] BD creada y migrada
- [ ] Permisos de carpetas correctos
- [ ] Firewall configurado
- [ ] Backup inicial realizado
- [ ] Usuario admin creado
- [ ] SSL/TLS configurado (si aplica)

---

**Última actualización**: Mayo 2024
