# Guía de despliegue a producción

Arquitectura de despliegue según la ficha técnica del proyecto: backend en **Render** (contenedor Docker), frontend en **Streamlit Community Cloud** (conectado directo desde GitHub).

## 1. Backend en Render

### 1.1 Requisitos previos
- Cuenta en [render.com](https://render.com) (login con GitHub recomendado).
- El repositorio debe estar en GitHub (ya lo está: `iSotelo/invest-assistant-app`).
- Una API key de OpenAI válida (ver `docs/como-obtener-openai-api-key.md` si necesitas generar una — ese archivo es local, pídesela a quien la tenga).

### 1.2 Crear el servicio

**Opción A — con Blueprint (usa `render.yaml`, recomendado):**
1. En el dashboard de Render, click en "New" → "Blueprint".
2. Conecta el repositorio `invest-assistant-app`.
3. Render detecta automáticamente `render.yaml` en la raíz y propone crear el servicio `invest-assistant-api`.
4. Te pedirá el valor de `OPENAI_API_KEY` (está marcada como `sync: false` en el blueprint, así que nunca queda en el repo) — pégala ahí.
5. Click en "Apply" para crear el servicio.

**Opción B — manual (si prefieres no usar el blueprint):**
1. "New" → "Web Service" → conecta el repo.
2. Runtime: **Docker**. Dockerfile path: `./Dockerfile` (raíz del repo).
3. Plan: Free (suficiente para el MVP piloto).
4. Health Check Path: `/api/v1/health`.
5. Variables de entorno (pestaña "Environment"):
   - `OPENAI_API_KEY` = tu clave real
   - `OPENAI_MODEL` = `gpt-4o-mini`
   - `LLM_TIMEOUT_SECONDS` = `25`
6. Click "Create Web Service".

### 1.3 Verificar el despliegue

Una vez que Render termine el build (puede tardar 3-5 minutos la primera vez, porque instala spaCy y descarga el modelo en español), prueba:

```bash
curl https://<tu-servicio>.onrender.com/api/v1/health
# Esperado: {"status":"healthy"}

curl -X POST https://<tu-servicio>.onrender.com/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"story_text": "Como usuario registrado quiero restablecer mi contraseña para recuperar el acceso a mi cuenta."}'
```

**Nota sobre el plan gratuito de Render:** los servicios free "duermen" tras ~15 minutos de inactividad y tardan ~30-50 segundos en despertar con la primera petición. Es normal ver una respuesta lenta en la primera llamada tras un rato sin uso — no es un error de la app.

### 1.4 Ficha técnica de referencia
Esta configuración corresponde a lo especificado en la ficha técnica del proyecto: compilación de contenedor mediante Dockerfile optimizado (Python 3.12), CPU compartida, variables de entorno seguras inyectadas en memoria, HTTPS/SSL automático provisto por Render.

## 2. Frontend en Streamlit Community Cloud

### 2.1 Requisitos previos
- Cuenta en [share.streamlit.io](https://share.streamlit.io) (login con GitHub).
- El backend de Render ya desplegado y con su URL pública a mano (paso 1.3).

### 2.2 Desplegar la app

1. En Streamlit Community Cloud, click "New app".
2. Selecciona el repositorio `iSotelo/invest-assistant-app`, rama `main`.
3. Main file path: `frontend/app.py`.
4. Antes de desplegar, abre "Advanced settings" → "Secrets" y agrega:
   ```toml
   BACKEND_API_URL = "https://<tu-servicio>.onrender.com"
   ```
   (El código de `frontend/api_client.py` lee esta variable vía `st.secrets` automáticamente — no requiere cambios adicionales.)
5. Click "Deploy".

### 2.3 Verificar el despliegue

Abre la URL pública que Streamlit Cloud asigna (formato `https://<algo>.streamlit.app`), llena una historia de ejemplo y confirma que el análisis se completa correctamente contra el backend de Render.

## 3. Seguridad (ya aplicada, confirmar en cada entorno)

- `OPENAI_API_KEY` nunca se escribe en el código ni en el repositorio — se configura como variable de entorno/secreto en cada plataforma (`.env` local está en `.gitignore`; Render usa su panel de Environment; Streamlit Cloud usa Secrets).
- Ambas plataformas proveen HTTPS/SSL automático.
- El sistema no persiste datos: las historias se procesan en memoria y no se guardan en ninguna base de datos.

## 4. Actualizar el despliegue

Ambas plataformas están conectadas a la rama `main` del repositorio: cualquier push a `main` dispara un redeploy automático. Para actualizar producción, mergea la rama de trabajo a `main` y haz push — no se requiere ninguna acción manual adicional en Render o Streamlit Cloud.

## 5. Referencia de umbrales de éxito

Ver `docs/diagnostico-mvp.md` (documento local del equipo) para los indicadores esperados de latencia, calidad y proceso que se miden en la fase piloto una vez desplegado.
