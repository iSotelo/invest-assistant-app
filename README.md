# invest-assistant-app
Repositorio principal del MVP que contiene la aplicación web para el análisis y mejora de historias de usuario mediante criterios INVEST, incluyendo la interfaz, lógica de negocio e integración con los servicios de Inteligencia Artificial.

## Estructura del proyecto

```
backend/app/      API FastAPI (routers, services, models)
frontend/         Interfaz Streamlit
tests/            Pruebas unitarias (backend/, frontend/)
eval/             Scripts y datasets de validación experimental (Precision/Recall/F1)
```

## Configuración local

1. Crear entorno virtual e instalar dependencias:
   ```
   python -m venv .venv
   .venv\Scripts\activate       # Windows
   pip install -r requirements.txt
   python -m spacy download es_core_news_sm
   ```
2. Copiar `.env.example` a `.env` y completar `OPENAI_API_KEY`.
3. Levantar el backend:
   ```
   uvicorn app.main:app --reload --app-dir backend
   ```
4. Levantar el frontend (en otra terminal):
   ```
   streamlit run frontend/app.py
   ```
5. Correr las pruebas:
   ```
   pytest --cov=backend/app
   ```

## Convenciones de commits

Formato `[HU-ID] tipo: descripción`, vinculado al backlog del tablero ágil (ej. `[HU-02] fix: corregir regex de spaCy`).
