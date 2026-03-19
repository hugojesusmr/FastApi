# 🎨 Guía: Aplicar Estilo Login al Dashboard

## 📋 Análisis del Estilo Login

### Características Visuales del Login

```
✨ Elementos Clave:
1. Blob animado de fondo
2. Glassmorphism (efecto cristal)
3. Efecto 3D con sombras
4. Brillo blanco
5. Iconos Lucide
6. Gradiente azul eléctrico
7. Animaciones suaves
8. Bordes redondeados
```

---

## PASO 1: Estructura HTML del Dashboard

### Paso 1.1: Crear base.html con mismo estilo

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dashboard{% endblock %}</title>
    
    <!-- Lucide Icons (mismo que login) -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/dashboard.css">
    {% block extra_css %}{% endblock %}
    
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();
        });
    </script>
</head>
<body>
    <!-- Blob animado (como en login) -->
    <div class="blob"></div>
    
    <!-- Contenedor principal -->
    <div class="dashboard-wrapper">
        {% include "components/topbar.html" %}
        
        <div class="container">
            {% include "components/sidebar.html" %}
            
            <main class="main-content">
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>

    <script src="/static/js/dashboard.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## PASO 2: CSS - Aplicar Glassmorphism

### Paso 2.1: Variables de Color (app/static/css/variables.css)

```css
:root {
    /* Colores del Login */
    --primary: #00d4ff;
    --primary-dark: #0099ff;
    --bg-light: #ffffff;
    --bg-dark: #0a0e27;
    
    /* Glassmorphism */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.5);
    --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
    
    /* Brillo */
    --glow-white: rgba(255, 255, 255, 0.8);
    --glow-blue: rgba(0, 212, 255, 0.3);
}
```

### Paso 2.2: Body y Blob (app/static/css/dashboard.css)

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    color: #1a202c;
    overflow-x: hidden;
}

/* Blob animado (como en login) */
.blob {
    position: fixed;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(30px, -30px); }
}

.dashboard-wrapper {
    position: relative;
    z-index: 1;
}
```

### Paso 2.3: Topbar con Glassmorphism

```css
.top-bar {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--glass-shadow),
                0 0 40px var(--glow-white);
    margin: 15px;
    border: 1px solid var(--glass-border);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
}

.top-bar:hover {
    box-shadow: var(--glass-shadow),
                0 0 60px var(--glow-white);
    background: rgba(255, 255, 255, 0.8);
}
```

### Paso 2.4: Sidebar con Glassmorphism

```css
.sidebar {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 30px 20px;
    width: 80px;
    transition: all 0.3s ease;
    overflow: hidden;
    box-shadow: var(--glass-shadow),
                0 0 40px var(--glow-white);
    border: 1px solid var(--glass-border);
    min-height: 800px;
    transform: translateZ(30px);
}

.sidebar:hover {
    box-shadow: var(--glass-shadow),
                0 0 60px var(--glow-white);
    background: rgba(255, 255, 255, 0.85);
    transform: translateZ(40px);
}

.sidebar.expanded {
    width: 250px;
}
```

### Paso 2.5: Cards con Glassmorphism

```css
.card {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
    border: 1px solid var(--glass-border);
    box-shadow: var(--glass-shadow),
                0 0 20px var(--glow-blue);
    transform: translateZ(20px);
}

.card:hover {
    border-color: var(--primary);
    box-shadow: var(--glass-shadow),
                0 0 40px var(--glow-blue);
    background: rgba(255, 255, 255, 0.9);
    transform: translateZ(30px) translateY(-5px);
}

.card-icon {
    font-size: 32px;
    margin-bottom: 12px;
    color: var(--primary);
}

.card-value {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

### Paso 2.6: Upload Card

```css
.upload-card {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 40px;
    border: 1px solid var(--glass-border);
    margin-bottom: 40px;
    box-shadow: var(--glass-shadow),
                0 0 40px var(--glow-white);
    transition: all 0.3s ease;
}

.upload-card:hover {
    box-shadow: var(--glass-shadow),
                0 0 60px var(--glow-white);
    background: rgba(255, 255, 255, 0.9);
}

.upload-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 30px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

---

## PASO 3: Componentes HTML

### Paso 3.1: Topbar (app/templates/components/topbar.html)

```html
<div class="top-bar">
    <div class="logo">
        <i data-lucide="rocket" style="color: var(--primary);"></i>
        <span>Dashboard</span>
    </div>
    
    <div class="user-section">
        <div class="user-info">
            <div class="user-avatar">
                <span id="userAvatar">U</span>
            </div>
            <span class="user-name" id="userName">Usuario</span>
        </div>
        <button class="logout-btn" onclick="logout()">
            <i data-lucide="log-out" style="width: 16px; height: 16px;"></i>
            Salir
        </button>
    </div>
</div>
```

### Paso 3.2: Sidebar (app/templates/components/sidebar.html)

```html
<aside class="sidebar" id="sidebar">
    <button class="hamburger" onclick="toggleSidebar()">
        <span></span>
        <span></span>
        <span></span>
    </button>
    
    <ul class="nav-menu">
        <li class="nav-item">
            <button class="nav-link active" onclick="switchTab('overview')">
                <i data-lucide="bar-chart-2"></i>
                <span>Resumen</span>
            </button>
        </li>
        <li class="nav-item">
            <button class="nav-link" onclick="switchTab('upload')">
                <i data-lucide="upload"></i>
                <span>Cargar</span>
            </button>
        </li>
        <li class="nav-item">
            <button class="nav-link" onclick="switchTab('regions')">
                <i data-lucide="map"></i>
                <span>Regiones</span>
            </button>
        </li>
        <li class="nav-item">
            <button class="nav-link" onclick="switchTab('settings')">
                <i data-lucide="settings"></i>
                <span>Configuración</span>
            </button>
        </li>
    </ul>
</aside>
```

---

## PASO 4: Dashboard HTML (app/templates/dashboard.html)

```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<!-- Overview Tab -->
<div id="overview-tab">
    <div class="cards-grid">
        <div class="card">
            <div class="card-icon">
                <i data-lucide="file-text"></i>
            </div>
            <div class="card-label">Total Archivos</div>
            <div class="card-value">24</div>
        </div>
        
        <div class="card">
            <div class="card-icon">
                <i data-lucide="check-circle"></i>
            </div>
            <div class="card-label">Procesados</div>
            <div class="card-value">18</div>
        </div>
        
        <div class="card">
            <div class="card-icon">
                <i data-lucide="clock"></i>
            </div>
            <div class="card-label">En Proceso</div>
            <div class="card-value">4</div>
        </div>
        
        <div class="card">
            <div class="card-icon">
                <i data-lucide="alert-circle"></i>
            </div>
            <div class="card-label">Errores</div>
            <div class="card-value">2</div>
        </div>
    </div>
</div>

<!-- Upload Tab -->
<div id="upload-tab" style="display: none;">
    <div class="upload-card">
        <h2 class="upload-title">
            <i data-lucide="upload-cloud"></i>
            Cargar Archivos
        </h2>
        <form action="/upload" class="dropzone" id="uploadForm">
            <div class="dz-message">
                <strong>Arrastra archivos aquí o haz clic para seleccionar</strong><br>
                <span>Soporta Excel, CSV y otros formatos</span>
            </div>
        </form>
    </div>
</div>

<!-- Settings Tab -->
<div id="settings-tab" style="display: none;">
    <div class="upload-card">
        <h2 class="upload-title">
            <i data-lucide="settings"></i>
            Configuración
        </h2>
        <div style="color: #7f8c8d;">
            <p>Tema: Claro</p>
            <p>Notificaciones: Activadas</p>
            <p>Idioma: Español</p>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="/static/css/variables.css">
{% endblock %}

{% block extra_js %}
<script src="/static/js/dashboard.js"></script>
{% endblock %}
```

---

## PASO 5: JavaScript (app/static/js/dashboard.js)

```javascript
function switchTab(tab) {
    // Ocultar todos los tabs
    document.querySelectorAll('[id$="-tab"]').forEach(el => {
        el.style.display = 'none';
    });
    
    // Mostrar tab seleccionado
    document.getElementById(tab + '-tab').style.display = 'block';
    
    // Actualizar nav activo
    document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active');
    });
    event.target.closest('.nav-link').classList.add('active');
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('expanded');
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

window.addEventListener('load', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
    }
    
    const username = localStorage.getItem('username') || 'Usuario';
    document.getElementById('userName').textContent = username;
    document.getElementById('userAvatar').textContent = username.charAt(0).toUpperCase();
});
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

- [ ] Paso 1: Crear base.html con blob
- [ ] Paso 2: Agregar CSS variables
- [ ] Paso 2: Aplicar glassmorphism a body
- [ ] Paso 2: Aplicar glassmorphism a topbar
- [ ] Paso 2: Aplicar glassmorphism a sidebar
- [ ] Paso 2: Aplicar glassmorphism a cards
- [ ] Paso 3: Crear topbar.html con iconos
- [ ] Paso 3: Crear sidebar.html con iconos
- [ ] Paso 4: Crear dashboard.html
- [ ] Paso 5: Agregar JavaScript
- [ ] Pruebas en navegador
- [ ] Ajustar colores si es necesario

---

## 🎨 Resultado Final

```
✨ Dashboard con mismo estilo que Login:
✓ Blob animado de fondo
✓ Glassmorphism en todos los elementos
✓ Efecto 3D con sombras
✓ Brillo blanco
✓ Iconos Lucide
✓ Gradiente azul eléctrico
✓ Animaciones suaves
✓ Responsive design
```

---

**Próximo paso**: Implementar paso a paso siguiendo esta guía
