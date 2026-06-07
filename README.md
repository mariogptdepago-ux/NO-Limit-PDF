# No-Limit_PDF

Aplicación web minimalista para unir múltiples PDF contenidos dentro de un archivo `.rar`.

## Características

- Interfaz blanco/negro con tipografía Ubuntu.
- Logo principal `No-Limit_PDF`.
- Logo de empresa `RelaxLife-Apps`.
- Detección automática de idioma del navegador.
- Idiomas: español, portugués e inglés.
- Selector manual `ES / PT / EN`.
- Extracción de `.rar` con `unar`.
- Unión de PDF con `pypdf`.
- Orden natural de archivos con `natsort`.

## Estructura

```text
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
```

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

En Linux puede ser necesario instalar `unar`:

```bash
sudo apt-get install unar
```

## Despliegue en Streamlit Cloud

1. Sube esta carpeta a GitHub.
2. Entra a Streamlit Cloud.
3. Crea una app desde tu repositorio.
4. Usa `app.py` como archivo principal.
5. Deploy.

## Idioma

La app detecta automáticamente el idioma del navegador. También puedes forzarlo con:

```text
?lang=es
?lang=pt
?lang=en
```

## Nota

El texto que está dentro de los PNG de los logos no se traduce automáticamente. La interfaz sí.
