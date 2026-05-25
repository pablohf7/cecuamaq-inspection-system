-- =====================================================
-- SISTEMA DE INSPECCIONES INDUSTRIALES - CECUAMAQ
-- PostgreSQL Database Schema
-- Versión: 1.0
-- =====================================================

-- Eliminar base de datos si existe (solo para desarrollo)
DROP DATABASE IF EXISTS cecuamaq_inspections;
CREATE DATABASE cecuamaq_inspections
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_EC.UTF-8'
    LC_CTYPE = 'es_EC.UTF-8'
    TEMPLATE = template0;

\c cecuamaq_inspections;

-- =====================================================
-- EXTENSIONES
-- =====================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ENUMERADOS
-- =====================================================
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');
CREATE TYPE inspection_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');
CREATE TYPE parameter_data_type AS ENUM ('numeric', 'text', 'boolean');

-- =====================================================
-- TABLA: roles
-- =====================================================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: usuarios
-- =====================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    status user_status DEFAULT 'active',
    phone VARCHAR(20),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA: clientes
-- =====================================================
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    ruc VARCHAR(20) UNIQUE,
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Ecuador',
    phone VARCHAR(20),
    email VARCHAR(100),
    contact_person VARCHAR(200),
    contact_phone VARCHAR(20),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA: plantas
-- =====================================================
CREATE TABLE plantas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    manager VARCHAR(200),
    phone VARCHAR(20),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE (cliente_id, code)
);

-- =====================================================
-- TABLA: ubicaciones_tecnicas
-- =====================================================
CREATE TABLE ubicaciones_tecnicas (
    id SERIAL PRIMARY KEY,
    planta_id INTEGER NOT NULL REFERENCES plantas(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    area VARCHAR(100),
    department VARCHAR(100),
    responsible VARCHAR(200),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE (planta_id, code)
);

-- =====================================================
-- TABLA: equipos
-- =====================================================
CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    ubicacion_tecnica_id INTEGER NOT NULL REFERENCES ubicaciones_tecnicas(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    tag VARCHAR(50),
    equipment_type VARCHAR(100),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    year_manufactured INTEGER,
    capacity VARCHAR(50),
    power_rating VARCHAR(50),
    voltage VARCHAR(50),
    current_rating VARCHAR(50),
    rpm VARCHAR(50),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE (ubicacion_tecnica_id, code)
);

-- =====================================================
-- TABLA: conjuntos
-- =====================================================
CREATE TABLE conjuntos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    assembly_type VARCHAR(100),
    position VARCHAR(50),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE (equipo_id, code)
);

-- =====================================================
-- TABLA: componentes
-- =====================================================
CREATE TABLE componentes (
    id SERIAL PRIMARY KEY,
    conjunto_id INTEGER NOT NULL REFERENCES conjuntos(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    component_type VARCHAR(100),
    material VARCHAR(100),
    part_number VARCHAR(100),
    quantity INTEGER DEFAULT 1,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE (conjunto_id, code)
);

-- =====================================================
-- TABLA: inspecciones
-- =====================================================
CREATE TABLE inspecciones (
    id SERIAL PRIMARY KEY,
    inspection_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Referencias jerárquicas (NULL permite inspección a cualquier nivel)
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    planta_id INTEGER REFERENCES plantas(id) ON DELETE CASCADE,
    ubicacion_tecnica_id INTEGER REFERENCES ubicaciones_tecnicas(id) ON DELETE CASCADE,
    equipo_id INTEGER REFERENCES equipos(id) ON DELETE CASCADE,
    conjunto_id INTEGER REFERENCES conjuntos(id) ON DELETE CASCADE,
    componente_id INTEGER REFERENCES componentes(id) ON DELETE CASCADE,
    
    -- Información de la inspección
    usuario_inspector_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE SET NULL,
    fecha_hora_inicio TIMESTAMP NOT NULL,
    fecha_hora_fin TIMESTAMP,
    
    -- Estado y observaciones
    estado inspection_status DEFAULT 'pending',
    observaciones_generales TEXT,
    
    -- Ubicación GPS (opcional)
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    
    -- Auditoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA: parametros_inspeccion (Catálogo)
-- =====================================================
CREATE TABLE parametros_inspeccion (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    unit VARCHAR(20),
    data_type parameter_data_type DEFAULT 'numeric',
    min_limit DECIMAL(15, 4),
    max_limit DECIMAL(15, 4),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: inspeccion_parametros (Valores medidos)
-- =====================================================
CREATE TABLE inspeccion_parametros (
    id SERIAL PRIMARY KEY,
    inspeccion_id INTEGER NOT NULL REFERENCES inspecciones(id) ON DELETE CASCADE,
    parametro_id INTEGER NOT NULL REFERENCES parametros_inspeccion(id) ON DELETE CASCADE,
    
    -- Valores
    valor_numerico DECIMAL(15, 4),
    valor_texto TEXT,
    valor_booleano BOOLEAN,
    
    -- Evaluación
    dentro_rango BOOLEAN,
    observaciones TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: inspeccion_fotos
-- =====================================================
CREATE TABLE inspeccion_fotos (
    id SERIAL PRIMARY KEY,
    inspeccion_id INTEGER NOT NULL REFERENCES inspecciones(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    description TEXT,
    photo_order INTEGER DEFAULT 1,
    uploaded_by INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (photo_order BETWEEN 1 AND 4)
);

-- =====================================================
-- TABLA: audit_log (Registro de auditoría)
-- =====================================================
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ÍNDICES
-- =====================================================

-- Usuarios
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_role ON usuarios(role_id);
CREATE INDEX idx_usuarios_status ON usuarios(status);

-- Clientes
CREATE INDEX idx_clientes_code ON clientes(code);
CREATE INDEX idx_clientes_ruc ON clientes(ruc);
CREATE INDEX idx_clientes_active ON clientes(is_active);

-- Plantas
CREATE INDEX idx_plantas_cliente ON plantas(cliente_id);
CREATE INDEX idx_plantas_code ON plantas(code);
CREATE INDEX idx_plantas_active ON plantas(is_active);

-- Ubicaciones Técnicas
CREATE INDEX idx_ubicaciones_planta ON ubicaciones_tecnicas(planta_id);
CREATE INDEX idx_ubicaciones_code ON ubicaciones_tecnicas(code);

-- Equipos
CREATE INDEX idx_equipos_ubicacion ON equipos(ubicacion_tecnica_id);
CREATE INDEX idx_equipos_tag ON equipos(tag);
CREATE INDEX idx_equipos_type ON equipos(equipment_type);

-- Conjuntos
CREATE INDEX idx_conjuntos_equipo ON conjuntos(equipo_id);

-- Componentes
CREATE INDEX idx_componentes_conjunto ON componentes(conjunto_id);

-- Inspecciones
CREATE INDEX idx_inspecciones_numero ON inspecciones(inspection_number);
CREATE INDEX idx_inspecciones_cliente ON inspecciones(cliente_id);
CREATE INDEX idx_inspecciones_planta ON inspecciones(planta_id);
CREATE INDEX idx_inspecciones_equipo ON inspecciones(equipo_id);
CREATE INDEX idx_inspecciones_inspector ON inspecciones(usuario_inspector_id);
CREATE INDEX idx_inspecciones_estado ON inspecciones(estado);
CREATE INDEX idx_inspecciones_fecha_inicio ON inspecciones(fecha_hora_inicio);

-- Parámetros
CREATE INDEX idx_parametros_code ON parametros_inspeccion(code);
CREATE INDEX idx_inspeccion_parametros_inspeccion ON inspeccion_parametros(inspeccion_id);

-- Fotos
CREATE INDEX idx_fotos_inspeccion ON inspeccion_fotos(inspeccion_id);

-- Audit
CREATE INDEX idx_audit_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_user ON audit_log(user_id);

-- =====================================================
-- FUNCIONES Y TRIGGERS
-- =====================================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas
CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plantas_updated_at BEFORE UPDATE ON plantas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ubicaciones_updated_at BEFORE UPDATE ON ubicaciones_tecnicas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_equipos_updated_at BEFORE UPDATE ON equipos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conjuntos_updated_at BEFORE UPDATE ON conjuntos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_componentes_updated_at BEFORE UPDATE ON componentes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_inspecciones_updated_at BEFORE UPDATE ON inspecciones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Roles
INSERT INTO roles (name, description, permissions) VALUES
('Administrador', 'Acceso total al sistema', '{"all": true}'),
('Supervisor', 'Gestión de inspecciones y reportes', '{"inspections": "rw", "reports": "r"}'),
('Inspector', 'Realización de inspecciones', '{"inspections": "rw"}'),
('Consulta', 'Solo lectura', '{"all": "r"}');

-- Usuario administrador por defecto
-- Password: Admin123! (debe cambiarse en producción)
INSERT INTO usuarios (username, email, password_hash, first_name, last_name, role_id, status)
VALUES (
    'admin',
    'admin@cecuamaq.com',
    crypt('Admin123!', gen_salt('bf', 12)),
    'Administrador',
    'Sistema',
    1,
    'active'
);

-- Parámetros de inspección comunes
INSERT INTO parametros_inspeccion (code, name, description, unit, data_type, min_limit, max_limit) VALUES
('TEMP', 'Temperatura', 'Temperatura de operación', '°C', 'numeric', 0, 150),
('VIB', 'Vibración', 'Nivel de vibración', 'mm/s', 'numeric', 0, 10),
('PRES', 'Presión', 'Presión de operación', 'PSI', 'numeric', 0, 500),
('COR', 'Corriente', 'Corriente eléctrica', 'A', 'numeric', 0, 1000),
('VOLT', 'Voltaje', 'Voltaje eléctrico', 'V', 'numeric', 0, 600),
('RPM', 'Revoluciones', 'Revoluciones por minuto', 'RPM', 'numeric', 0, 5000),
('ESP', 'Espesor', 'Espesor de material', 'mm', 'numeric', 0, 100),
('NIV-ACE', 'Nivel de Aceite', 'Nivel de aceite lubricante', '%', 'numeric', 0, 100),
('RUIDO', 'Ruido', 'Nivel de ruido', 'dB', 'numeric', 0, 120),
('FUGA', 'Fuga', 'Presencia de fugas', '', 'boolean', NULL, NULL);

-- =====================================================
-- CLIENTE Y ESTRUCTURA DE EJEMPLO
-- =====================================================

-- Cliente de ejemplo
INSERT INTO clientes (code, name, ruc, address, city, phone, email, contact_person, created_by)
VALUES (
    'CLI001',
    'Empresa Industrial S.A.',
    '0992345678001',
    'Av. Principal 123',
    'Guayaquil',
    '04-2345678',
    'contacto@empresa.com',
    'Juan Pérez',
    1
);

-- Planta de ejemplo
INSERT INTO plantas (cliente_id, code, name, address, city, manager, created_by)
VALUES (
    1,
    'PLT001',
    'Planta Norte',
    'Km 15 vía Daule',
    'Guayaquil',
    'María González',
    1
);

-- Ubicación técnica de ejemplo
INSERT INTO ubicaciones_tecnicas (planta_id, code, name, area, department, created_by)
VALUES (
    1,
    'UT001',
    'Zona de Bombeo',
    'Producción',
    'Mantenimiento',
    1
);

-- Equipo de ejemplo
INSERT INTO equipos (ubicacion_tecnica_id, code, name, tag, equipment_type, manufacturer, model, created_by)
VALUES (
    1,
    'EQ001',
    'Bomba Centrífuga Principal',
    'BCP-001',
    'Bomba Centrífuga',
    'Goulds',
    '3196',
    1
);

-- Conjunto de ejemplo
INSERT INTO conjuntos (equipo_id, code, name, assembly_type, created_by)
VALUES (
    1,
    'CJ001',
    'Motor Eléctrico',
    'Motor Trifásico',
    1
);

-- Componente de ejemplo
INSERT INTO componentes (conjunto_id, code, name, component_type, created_by)
VALUES (
    1,
    'CP001',
    'Rodamiento Lado Acople',
    'Rodamiento',
    1
);

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista de jerarquía completa
CREATE OR REPLACE VIEW v_jerarquia_completa AS
SELECT 
    cl.id as cliente_id,
    cl.name as cliente_nombre,
    pl.id as planta_id,
    pl.name as planta_nombre,
    ut.id as ubicacion_tecnica_id,
    ut.name as ubicacion_nombre,
    eq.id as equipo_id,
    eq.name as equipo_nombre,
    eq.tag as equipo_tag,
    cj.id as conjunto_id,
    cj.name as conjunto_nombre,
    cp.id as componente_id,
    cp.name as componente_nombre
FROM clientes cl
LEFT JOIN plantas pl ON pl.cliente_id = cl.id
LEFT JOIN ubicaciones_tecnicas ut ON ut.planta_id = pl.id
LEFT JOIN equipos eq ON eq.ubicacion_tecnica_id = ut.id
LEFT JOIN conjuntos cj ON cj.equipo_id = eq.id
LEFT JOIN componentes cp ON cp.conjunto_id = cj.id;

-- Vista de inspecciones con detalles
CREATE OR REPLACE VIEW v_inspecciones_detalle AS
SELECT 
    i.id,
    i.inspection_number,
    i.fecha_hora_inicio,
    i.fecha_hora_fin,
    i.estado,
    cl.name as cliente_nombre,
    pl.name as planta_nombre,
    eq.name as equipo_nombre,
    u.username as inspector,
    u.first_name || ' ' || u.last_name as inspector_nombre,
    COUNT(DISTINCT ip.id) as total_parametros,
    COUNT(DISTINCT if.id) as total_fotos
FROM inspecciones i
INNER JOIN clientes cl ON cl.id = i.cliente_id
LEFT JOIN plantas pl ON pl.id = i.planta_id
LEFT JOIN equipos eq ON eq.id = i.equipo_id
INNER JOIN usuarios u ON u.id = i.usuario_inspector_id
LEFT JOIN inspeccion_parametros ip ON ip.inspeccion_id = i.id
LEFT JOIN inspeccion_fotos if ON if.inspeccion_id = i.id
GROUP BY i.id, cl.name, pl.name, eq.name, u.username, u.first_name, u.last_name;

-- =====================================================
-- COMENTARIOS EN TABLAS
-- =====================================================

COMMENT ON TABLE clientes IS 'Registro de clientes de Cecuamaq';
COMMENT ON TABLE plantas IS 'Plantas industriales por cliente';
COMMENT ON TABLE ubicaciones_tecnicas IS 'Ubicaciones técnicas dentro de plantas';
COMMENT ON TABLE equipos IS 'Equipos industriales';
COMMENT ON TABLE conjuntos IS 'Conjuntos de equipos';
COMMENT ON TABLE componentes IS 'Componentes de conjuntos';
COMMENT ON TABLE inspecciones IS 'Inspecciones técnicas realizadas';
COMMENT ON TABLE parametros_inspeccion IS 'Catálogo de parámetros medibles';
COMMENT ON TABLE inspeccion_parametros IS 'Valores de parámetros por inspección';
COMMENT ON TABLE inspeccion_fotos IS 'Fotografías adjuntas a inspecciones';

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================

-- Verificación
SELECT 'Base de datos creada exitosamente' as status;
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
