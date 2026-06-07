NO-LIMIT_PDF - RELAXLIFE-APPS
================================

Aplicación web en Streamlit para subir un archivo .rar con varios PDF,
unirlos en un único PDF y descargar el resultado.

CARACTERÍSTICAS
---------------
- Interfaz limpia, minimalista y en blanco/negro.
- Tipografía Ubuntu mediante CSS.
- Logo principal No-Limit_PDF.
- Logo de empresa RelaxLife-Apps.
- Soporte automático de idioma según navegador: español, portugués e inglés.
- Selector manual de idioma: ES / PT / EN.
- Carga de archivo .rar desde el computador.
- Búsqueda recursiva de PDF dentro del .rar, incluso en subcarpetas.
- Unión de PDF en orden natural por nombre.
- Descarga directa del PDF final.

ESTRUCTURA DEL PROYECTO
-----------------------
no_limit_pdf_app/
│
├── app.py
├── requirements.txt
├── packages.txt
├── README.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── assets/
    ├── no_limit_pdf.png
    └── relaxlife_apps.png

ARCHIVOS IMPORTANTES
--------------------
app.py
    Código principal de la aplicación Streamlit.

requirements.txt
    Dependencias Python requeridas por Streamlit Cloud.

packages.txt
    Dependencias del sistema. Incluye unar para extraer archivos .rar.

.streamlit/config.toml
    Configuración visual y de tamaño máximo de carga.

assets/no_limit_pdf.png
    Logo principal de la aplicación.

assets/relaxlife_apps.png
    Logo de la empresa.

CÓMO EJECUTAR LOCALMENTE
------------------------
1. Instala Python 3.10 o superior.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Instala dependencias:

   pip install -r requirements.txt

4. Asegúrate de tener instalado unar en el sistema.

   En Ubuntu/Debian:
   sudo apt-get install unar

5. Ejecuta la app:

   streamlit run app.py

CÓMO SUBIR A GITHUB
-------------------
1. Crea un repositorio en GitHub, por ejemplo:
   no-limit-pdf

2. Sube todos los archivos y carpetas de este proyecto.

3. Verifica que queden subidos:
   - app.py
   - requirements.txt
   - packages.txt
   - .streamlit/config.toml
   - assets/no_limit_pdf.png
   - assets/relaxlife_apps.png

CÓMO DESPLEGAR EN STREAMLIT CLOUD
---------------------------------
1. Entra a:
   https://streamlit.io/cloud

2. Inicia sesión con GitHub.

3. Crea una nueva app.

4. Selecciona tu repositorio.

5. En Main file path coloca:
   app.py

6. Clic en Deploy.

IDIOMAS
-------
La app intenta detectar el idioma del navegador del usuario:

- es-CO, es-ES, etc. -> Español
- pt-BR, pt-PT, etc. -> Portugués
- en-US, en-GB, etc. -> Inglés
- otro idioma -> Inglés por defecto

También puedes forzar el idioma desde la URL:

?lang=es
?lang=pt
?lang=en

Ejemplo:
https://tu-app.streamlit.app/?lang=es

NOTA SOBRE EL LOGO
------------------
El texto que está dentro del archivo PNG del logo no se puede traducir dinámicamente.
La interfaz sí se traduce. Para una traducción perfecta del eslogan, conviene usar
un logo solo con el ícono y escribir el nombre/eslogan como texto HTML dentro de la app.

SEGURIDAD Y PRIVACIDAD
----------------------
La app procesa los archivos temporalmente usando carpetas temporales del servidor.
Los archivos no se guardan permanentemente desde el código de la app.

Sin embargo, recuerda que si usas Streamlit Cloud, los archivos se suben al entorno
remoto de ejecución mientras se procesan.
