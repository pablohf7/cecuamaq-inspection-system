# 🚀 GUÍA DE INSTALACIÓN Y DESPLIEGUE
## Sistema CECUAMAQ - Inspecciones Industriales

---

## 📦 ARCHIVOS DESCARGADOS

Has descargado los siguientes archivos:

### 📄 Documentación (4 archivos)
1. `RESUMEN_PROYECTO.md` - Resumen ejecutivo del proyecto
2. `INDICE_ARCHIVOS.md` - Índice completo de archivos
3. `README.md` - Documentación principal
4. `ARQUITECTURA.md` - Arquitectura técnica detallada

### 🔧 Configuración (3 archivos)
5. `requirements.txt` - Dependencias Python
6. `.env.example` - Variables de entorno
7. `database_schema.sql` - Script de base de datos PostgreSQL

### 💻 Código (2 archivos)
8. `main.py` - Aplicación principal Flet
9. `cecuamaq_source_code.tar.gz` - Código fuente completo (carpeta app/)

---

## 🛠️ INSTALACIÓN PASO A PASO

### PASO 1: Preparar el Entorno

#### 1.1 Instalar PostgreSQL

**Windows:**
```bash
# Descargar desde: https://www.postgresql.org/download/windows/
# Instalar y recordar la contraseña de postgres
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### 1.2 Instalar Python 3.10+

**Windows:**
```bash
# Descargar desde: https://www.python.org/downloads/
# Marcar "Add Python to PATH"
```

**Linux:**
```bash
sudo apt install python3.10 python3.10-venv python3-pip
```

**macOS:**
```bash
brew install python@3.10
```

### PASO 2: Crear Estructura de Carpetas

```bash
# Crear carpeta del proyecto
mkdir cecuamaq-inspection-system
cd cecuamaq-inspection-system

# Crear subcarpetas
mkdir -p database uploads/inspection_photos exports logs

# Extraer código fuente
tar -xzf cecuamaq_source_code.tar.gz

# Copiar archivos
# Copiar main.py, requirements.txt, .env.example a la raíz
# Copiar database_schema.sql a database/
```

**Estructura final:**
```
cecuamaq-inspection-system/
├── app/                    (del tar.gz)
├── database/
│   └── init_schema.sql     (copiar database_schema.sql aquí)
├── uploads/
│   └── inspection_photos/
├── exports/
├── logs/
├── main.py
├── requirements.txt
└── .env.example
```

### PASO 3: Configurar Base de Datos

#### 3.1 Acceder a PostgreSQL

```bash
# Linux/macOS
sudo -u postgres psql

# Windows (en símbolo del sistema)
psql -U postgres
```

#### 3.2 Ejecutar Script de Creación

**Opción A - Desde psql:**
```sql
\i /ruta/completa/database/init_schema.sql
```

**Opción B - Desde línea de comandos:**
```bash
# Linux/macOS
psql -U postgres < database/init_schema.sql

# Windows
psql -U postgres -f database\init_schema.sql
```

#### 3.3 Verificar Creación

```sql
-- Conectarse a la base de datos
\c cecuamaq_inspections

-- Ver tablas creadas
\dt

-- Debería mostrar 13 tablas
```

### PASO 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env (usar nano, vim, notepad, etc.)
nano .env
```

**Configurar en .env:**
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cecuamaq_inspections
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD_AQUI  # ⚠️ CAMBIAR ESTO

APP_NAME=Cecuamaq Inspection System
SECRET_KEY=CAMBIAR_EN_PRODUCCION  # ⚠️ CAMBIAR ESTO
```

### PASO 5: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### PASO 6: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Esto instalará:
# - Flet (UI)
# - SQLAlchemy (ORM)
# - PostgreSQL driver
# - Bcrypt (seguridad)
# - OpenPyXL (Excel)
# - Pandas
# - Y más...
```

### PASO 7: Verificar Instalación

```bash
# Verificar Python
python --version  # Debe ser 3.10+

# Verificar PostgreSQL
psql --version

# Verificar paquetes instalados
pip list
```

### PASO 8: Ejecutar la Aplicación

```bash
# Desde la raíz del proyecto
python main.py
```

**Debería abrirse la ventana de la aplicación Flet** 🎉

### PASO 9: Primer Login

```
Usuario: admin
Contraseña: Admin123!
```

⚠️ **IMPORTANTE**: Cambiar esta contraseña en producción.

---

## 🔧 CONFIGURACIÓN ADICIONAL

### Crear Usuario Admin Personalizado

```sql
-- Conectarse a PostgreSQL
psql -U postgres -d cecuamaq_inspections

-- Crear nuevo usuario admin (ejemplo)
INSERT INTO usuarios (username, email, password_hash, first_name, last_name, role_id, status)
VALUES (
    'tu_usuario',
    'tu_email@empresa.com',
    crypt('TuContraseñaSegura123!', gen_salt('bf', 12)),
    'Tu Nombre',
    'Tu Apellido',
    1,
    'active'
);
```

### Configurar Roles Adicionales

```sql
-- Ver roles existentes
SELECT * FROM roles;

-- Crear nuevo rol (ejemplo)
INSERT INTO roles (name, description, permissions)
VALUES (
    'Técnico',
    'Técnico de mantenimiento',
    '{"inspections": "rw", "reports": "r"}'::jsonb
);
```

---

## 🐛 RESOLUCIÓN DE PROBLEMAS

### Error: "No module named 'flet'"

```bash
# Asegurarse de que el entorno virtual está activado
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "could not connect to server"

```bash
# Verificar que PostgreSQL está corriendo

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql

# Windows:
# Servicios > PostgreSQL > Iniciar

# macOS:
brew services list
brew services start postgresql
```

### Error: "FATAL: password authentication failed"

```bash
# Verificar credenciales en .env
# Verificar que el usuario postgres tiene la contraseña correcta

# Cambiar contraseña de postgres (si es necesario)
psql -U postgres
ALTER USER postgres WITH PASSWORD 'nueva_contraseña';
```

### Error: "relation does not exist"

```bash
# La base de datos no se creó correctamente
# Volver a ejecutar el script

psql -U postgres
DROP DATABASE IF EXISTS cecuamaq_inspections;
\i /ruta/database/init_schema.sql
```

### Error: "Permission denied" en carpetas

```bash
# Linux/macOS - Dar permisos
chmod -R 755 uploads/ exports/ logs/

# Windows - Clic derecho > Propiedades > Seguridad
# Dar permisos de escritura al usuario
```

---

## 📱 COMPILAR PARA MÓVIL (Opcional)

### Android
```bash
flet build apk
```

### iOS
```bash
flet build ipa
```

Requiere configuración adicional de Flet.

---

## 🔒 SEGURIDAD EN PRODUCCIÓN

### 1. Cambiar Contraseñas

```bash
# Editar .env
SECRET_KEY=generar-clave-aleatoria-segura-aqui
DB_PASSWORD=contraseña-segura-postgresql
```

### 2. Cambiar Password Admin

```sql
-- Desde psql
UPDATE usuarios
SET password_hash = crypt('NuevaContraseñaSegura123!', gen_salt('bf', 12))
WHERE username = 'admin';
```

### 3. Configurar Firewall

```bash
# Permitir solo PostgreSQL local
sudo ufw allow from 127.0.0.1 to any port 5432
```

### 4. Backup Automático

```bash
# Crear script de backup
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres cecuamaq_inspections > backup_$DATE.sql
```

```bash
chmod +x backup.sh

# Agregar a cron para backup diario
crontab -e
0 2 * * * /ruta/backup.sh
```

---

## 📊 MONITOREO

### Ver Logs

```bash
# Logs del sistema
tail -f logs/cecuamaq_YYYYMMDD.log

# Logs de PostgreSQL
# Linux: /var/log/postgresql/
# Windows: C:\Program Files\PostgreSQL\XX\data\log\
```

### Consultas Útiles

```sql
-- Total de usuarios
SELECT COUNT(*) FROM usuarios;

-- Total de inspecciones
SELECT COUNT(*) FROM inspecciones;

-- Inspecciones por estado
SELECT estado, COUNT(*) 
FROM inspecciones 
GROUP BY estado;

-- Últimas 10 inspecciones
SELECT inspection_number, fecha_hora_inicio, estado
FROM inspecciones
ORDER BY fecha_hora_inicio DESC
LIMIT 10;
```

---

## 🆘 SOPORTE

### Recursos
- **README.md**: Documentación completa
- **ARQUITECTURA.md**: Detalles técnicos
- **Código fuente**: Todos los archivos están comentados

### Contacto
- Email: soporte@cecuamaq.com
- Documentación online: docs.cecuamaq.com

---

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] PostgreSQL instalado y corriendo
- [ ] Python 3.10+ instalado
- [ ] Estructura de carpetas creada
- [ ] Código fuente extraído
- [ ] Base de datos creada (database_schema.sql ejecutado)
- [ ] Variables de entorno configuradas (.env)
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas (pip install -r requirements.txt)
- [ ] Aplicación ejecutada (python main.py)
- [ ] Login exitoso (admin/Admin123!)
- [ ] Dashboard visible
- [ ] Contraseña admin cambiada (en producción)

---

## 🎓 PRÓXIMOS PASOS

1. **Explorar la aplicación**
   - Navegar por el dashboard
   - Ver la estructura

2. **Leer documentación**
   - README.md para funcionalidades
   - ARQUITECTURA.md para entender el diseño

3. **Personalizar**
   - Agregar más vistas según necesidad
   - Implementar CRUDs faltantes
   - Añadir validaciones específicas

4. **Extender**
   - Agregar reportes personalizados
   - Implementar notificaciones
   - Agregar gráficos y dashboards

---

✨ **¡Sistema listo para usar!** ✨

**Versión**: 1.0.0  
**Última actualización**: Mayo 2024
