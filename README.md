# 🥛 LácteosPlur – Sistema de Gestión

Sistema de autenticación y gestión de ventas para empresa de productos lácteos.
Desarrollado con Flask, SQLite3, Bootstrap 5 y criptografía SHA-256 + Salt.

---

## 📁 Estructura del Proyecto

```
lacteos_app/
├── app.py                   # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias Python
├── lacteos.db               # Base de datos SQLite (se genera automáticamente)
│
├── models/
│   ├── __init__.py
│   └── database.py          # Conexión y esquema de la BD
│
├── routes/
│   ├── __init__.py
│   ├── auth.py              # Login, Registro, Recuperar contraseña
│   ├── dashboard.py         # Pantalla principal
│   ├── users.py             # Gestión de usuarios (solo Admin)
│   └── ventas.py            # Registro y listado de ventas
│
├── utils/
│   ├── __init__.py
│   └── crypto.py            # SHA-256 + Salt (hash y verificación)
│
├── templates/
│   ├── base.html            # Plantilla base con navbar
│   ├── login.html           # HU01 – Inicio de sesión
│   ├── register.html        # HU04 – Registro de usuario
│   ├── recover.html         # Recuperar contraseña
│   ├── dashboard.html       # HU03 – Pantalla principal / menú
│   ├── usuarios.html        # HU03 – Gestión de usuarios
│   ├── ventas.html          # HU03 – Listado de ventas
│   └── registrar_venta.html # HU03 – Formulario nueva venta
│
└── static/
    ├── css/                 # CSS adicional (opcional)
    ├── js/                  # JS adicional (opcional)
    └── images/              # ← AQUÍ VAN TUS IMÁGENES (ver sección abajo)
```

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python app.py
```

### 3. Abrir en el navegador
```
http://127.0.0.1:5000
```

---

## 🔐 Credenciales por Defecto

Al ejecutar por primera vez, se crea automáticamente un administrador:

| Campo    | Valor              |
|----------|--------------------|
| Usuario  | `admin`            |
| Contraseña | `Admin123!`      |
| Rol      | Administrador      |

> **Cambie la contraseña en su primer ingreso.**

---

## 🖼️ Dónde Poner las Imágenes

Coloque sus imágenes en la carpeta: **`static/images/`**

| Imagen sugerida       | Nombre de archivo recomendado | Usado en                    |
|-----------------------|-------------------------------|-----------------------------|
| Logo de la empresa    | `logo.png`                    | Login (panel izquierdo)     |
| Foto Kefir Plur 1000g | `kefir.jpg`                   | Login / Dashboard           |
| Foto Yogo yogo 900g   | `yogoyogo.jpg`                | Login / Dashboard           |
| Foto Yogurt 900g      | `yogurt.jpg`                  | Login / Dashboard           |
| Foto Avena 250g       | `avena.jpg`                   | Login / Dashboard           |
| Foto Yox 100g         | `yox.jpg`                     | Login / Dashboard           |
| Imagen de fondo       | `hero_bg.jpg`                 | Panel login (opcional)      |

### Cómo reemplazar los emojis con imágenes reales

En `templates/login.html`, busque los comentarios `<!-- IMAGEN: -->` y reemplácelos.

**Ejemplo logo:**
```html
<!-- Antes (emoji): -->
<div class="hero-logo">🥛</div>

<!-- Después (imagen real): -->
<div class="hero-logo">
    <img src="/static/images/logo.png" alt="Logo" style="width:80px;object-fit:contain">
</div>
```

**Ejemplo producto:**
```html
<!-- Antes: -->
<div class="product-img-wrap" title="Kefir Plur">🥛</div>

<!-- Después: -->
<img src="/static/images/kefir.jpg"
     style="width:70px;height:70px;object-fit:cover;border-radius:12px"
     alt="Kefir Plur">
```

---

## 🔒 Seguridad – Criptografía SHA-256 + Salt

El módulo `utils/crypto.py` implementa:

1. **`generate_salt()`** – Genera 32 bytes aleatorios seguros con `os.urandom()`.
2. **`hash_password(password, salt)`** – Concatena salt + contraseña y aplica SHA-256.
3. **`verify_password(password, stored_hash, salt)`** – Verifica sin exponer la contraseña.

```
Contraseña: "MiPass123"
Salt:       "a1b2c3d4e5..." (64 chars hex aleatorio)
Hash:       SHA256( salt + password ) → almacenado en BD
```

La contraseña **nunca se almacena en texto plano**.

---

## 👥 Roles y Permisos

| Funcionalidad          | Administrador | Auxiliar |
|------------------------|:---:|:---:|
| Inicio de sesión       | ✅  | ✅  |
| Ver Dashboard          | ✅  | ✅  |
| Gestión de Usuarios    | ✅  | ❌  |
| Registrar Ventas       | ✅  | ✅  |
| Ver Ventas             | ✅  | ✅  |
| Cerrar Sesión          | ✅  | ✅  |

---

## 📦 Tecnologías Usadas

- **Backend:** Python 3.10+ · Flask 3.x
- **Base de datos:** SQLite3 (nativo Python)
- **Criptografía:** hashlib SHA-256 + os.urandom (salt)
- **Frontend:** HTML5 · Bootstrap 5.3 · Bootstrap Icons
- **Fuentes:** Playfair Display · DM Sans (Google Fonts)
- **Comunicación:** HTTP (GET/POST) con Flask Blueprints

---

## 🗂️ Historias de Usuario Implementadas

| ID    | Historia               | Estado |
|-------|------------------------|--------|
| HU01  | Inicio de Sesión       | ✅ Implementada |
| HU03  | Pantalla Principal     | ✅ Implementada |
| HU04  | Registro de Usuario    | ✅ Implementada |
| –     | Recuperar Contraseña   | ✅ Implementada |
| –     | Gestión de Usuarios    | ✅ Implementada |
| –     | Registro de Ventas     | ✅ Implementada |
