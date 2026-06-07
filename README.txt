NO-LIMIT_PDF - RelaxLife-Apps

Aplicación Streamlit para subir un archivo .rar con varios PDF y descargar un único PDF unido.

ARCHIVOS NECESARIOS
- app.py
- requirements.txt
- packages.txt
- .streamlit/config.toml
- assets/no_limit_pdf.png
- assets/relaxlife_apps.png

DESPLIEGUE EN STREAMLIT CLOUD
1. Sube esta carpeta completa a un repositorio de GitHub.
2. En Streamlit Cloud selecciona el repositorio.
3. En Main file path escribe: app.py
4. Deploy.

IDIOMAS
La app detecta automáticamente el idioma del navegador:
- Español: es-*
- Portugués: pt-*
- Inglés: en-* o cualquier otro idioma por defecto

También puedes forzar el idioma en la URL:
?lang=es
?lang=pt
?lang=en

IMPORTANTE
GitHub Pages no ejecuta Python. El código debe ejecutarse en Streamlit Cloud, Hugging Face Spaces, Render, Railway u otro servicio con backend Python.
