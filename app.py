import os
import io
import base64
import tempfile
import subprocess
from textwrap import dedent

import streamlit as st
from pypdf import PdfWriter
from natsort import natsorted


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="No-Limit_PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# TRADUCCIONES
# ============================================================

LANGS = {
    "en": {
        "about": "About",
        "help": "Help",
        "tagline": "Unlimited PDF Merging",
        "description": "Merge multiple PDF files from a single .rar archive with a clean and simple flow.",
        "upload_title": "1. Upload your RAR file",
        "upload_desc": "Upload a .rar file containing the PDF files you want to merge.",
        "upload_label": "Upload your .rar file",
        "output_title": "2. Output file name",
        "output_desc": "Choose the name of the final merged PDF.",
        "output_label": "Output file name",
        "output_default": "merged.pdf",
        "merge_title": "3. Merge",
        "merge_desc": "Click the button to start merging your PDF files.",
        "merge_button": "Merge PDFs",
        "processing": "Processing your file...",
        "upload_error": "Please upload a .rar file before continuing.",
        "no_pdfs": "No PDF files were found inside the .rar file.",
        "success": "PDF merged successfully. {n} PDF files were processed.",
        "download": "Download merged PDF",
        "view_files": "View merged PDF files",
        "view_errors": "View files that could not be merged",
        "rar_error": "The .rar file could not be extracted. It may be damaged, password-protected, or unsupported.",
        "pdf_error": "No valid PDF could be merged. Please check that the files are not damaged or protected.",
        "step1_title": "Upload",
        "step1_text": "Upload a .rar file containing multiple PDF files.",
        "step2_title": "Merge",
        "step2_text": "We merge them in natural file-name order.",
        "step3_title": "Download",
        "step3_text": "Download your merged PDF instantly.",
        "fast_title": "Fast",
        "fast_text": "High-speed PDF merging directly from your uploaded file.",
        "private_title": "Private",
        "private_text": "Files are processed temporarily and are not kept permanently.",
        "unlimited_title": "Unlimited",
        "unlimited_text": "Merge many PDF files into one clean final document.",
        "footer_rights": "All rights reserved.",
        "privacy": "Privacy",
        "terms": "Terms",
        "contact": "Contact",
    },
    "es": {
        "about": "Acerca de",
        "help": "Ayuda",
        "tagline": "Unión ilimitada de PDF",
        "description": "Une múltiples archivos PDF desde un único archivo .rar con un flujo limpio y simple.",
        "upload_title": "1. Sube tu archivo RAR",
        "upload_desc": "Sube un archivo .rar que contenga los PDF que quieres unir.",
        "upload_label": "Sube tu archivo .rar",
        "output_title": "2. Nombre del archivo final",
        "output_desc": "Elige el nombre del PDF unido.",
        "output_label": "Nombre del archivo final",
        "output_default": "PDF_unido.pdf",
        "merge_title": "3. Unir",
        "merge_desc": "Haz clic en el botón para comenzar a unir tus PDF.",
        "merge_button": "Unir PDF",
        "processing": "Procesando tu archivo...",
        "upload_error": "Por favor sube un archivo .rar antes de continuar.",
        "no_pdfs": "No se encontraron archivos PDF dentro del .rar.",
        "success": "PDF unido correctamente. Se procesaron {n} archivos PDF.",
        "download": "Descargar PDF unido",
        "view_files": "Ver archivos PDF unidos",
        "view_errors": "Ver archivos que no se pudieron unir",
        "rar_error": "No se pudo extraer el archivo .rar. Puede estar dañado, protegido con contraseña o usar un formato no soportado.",
        "pdf_error": "No se pudo unir ningún PDF válido. Verifica que los archivos no estén dañados o protegidos.",
        "step1_title": "Subir",
        "step1_text": "Sube un archivo .rar con varios PDF.",
        "step2_title": "Unir",
        "step2_text": "Los unimos en orden natural por nombre.",
        "step3_title": "Descargar",
        "step3_text": "Descarga tu PDF unido al instante.",
        "fast_title": "Rápido",
        "fast_text": "Unión ágil de PDF directamente desde tu archivo cargado.",
        "private_title": "Privado",
        "private_text": "Los archivos se procesan temporalmente y no se guardan de forma permanente.",
        "unlimited_title": "Ilimitado",
        "unlimited_text": "Une muchos PDF en un único documento limpio.",
        "footer_rights": "Todos los derechos reservados.",
        "privacy": "Privacidad",
        "terms": "Términos",
        "contact": "Contacto",
    },
    "pt": {
        "about": "Sobre",
        "help": "Ajuda",
        "tagline": "Mesclagem ilimitada de PDFs",
        "description": "Mescle vários arquivos PDF a partir de um único arquivo .rar com um fluxo limpo e simples.",
        "upload_title": "1. Envie seu arquivo RAR",
        "upload_desc": "Envie um arquivo .rar contendo os PDFs que você deseja mesclar.",
        "upload_label": "Envie seu arquivo .rar",
        "output_title": "2. Nome do arquivo final",
        "output_desc": "Escolha o nome do PDF mesclado.",
        "output_label": "Nome do arquivo final",
        "output_default": "PDF_mesclado.pdf",
        "merge_title": "3. Mesclar",
        "merge_desc": "Clique no botão para começar a mesclar seus PDFs.",
        "merge_button": "Mesclar PDFs",
        "processing": "Processando seu arquivo...",
        "upload_error": "Por favor, envie um arquivo .rar antes de continuar.",
        "no_pdfs": "Nenhum arquivo PDF foi encontrado dentro do .rar.",
        "success": "PDF mesclado com sucesso. {n} arquivos PDF foram processados.",
        "download": "Baixar PDF mesclado",
        "view_files": "Ver PDFs mesclados",
        "view_errors": "Ver arquivos que não puderam ser mesclados",
        "rar_error": "Não foi possível extrair o arquivo .rar. Ele pode estar danificado, protegido por senha ou em formato não suportado.",
        "pdf_error": "Nenhum PDF válido pôde ser mesclado. Verifique se os arquivos não estão danificados ou protegidos.",
        "step1_title": "Enviar",
        "step1_text": "Envie um arquivo .rar contendo vários PDFs.",
        "step2_title": "Mesclar",
        "step2_text": "Mesclamos os arquivos em ordem natural pelo nome.",
        "step3_title": "Baixar",
        "step3_text": "Baixe seu PDF mesclado instantaneamente.",
        "fast_title": "Rápido",
        "fast_text": "Mesclagem rápida de PDFs diretamente a partir do arquivo enviado.",
        "private_title": "Privado",
        "private_text": "Os arquivos são processados temporariamente e não são armazenados permanentemente.",
        "unlimited_title": "Ilimitado",
        "unlimited_text": "Mescle muitos PDFs em um único documento limpo.",
        "footer_rights": "Todos os direitos reservados.",
        "privacy": "Privacidade",
        "terms": "Termos",
        "contact": "Contato",
    },
}


def normalize_language(value: str) -> str:
    if not value:
        return "en"
    value = str(value).lower()
    if value.startswith("es"):
        return "es"
    if value.startswith("pt"):
        return "pt"
    if value.startswith("en"):
        return "en"
    return "en"


def get_browser_locale() -> str:
    try:
        return st.context.locale or "en-US"
    except Exception:
        return "en-US"


url_lang = st.query_params.get("lang", None)
current_lang = normalize_language(url_lang or get_browser_locale())
T = LANGS[current_lang]

active_es = "active" if current_lang == "es" else ""
active_pt = "active" if current_lang == "pt" else ""
active_en = "active" if current_lang == "en" else ""


# ============================================================
# LOGOS Y HTML
# ============================================================

LOGO_MAIN = "assets/no_limit_pdf.png"
LOGO_COMPANY = "assets/relaxlife_apps.png"


def img_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def html(markup: str) -> None:
    """Renderiza HTML sin que Markdown lo convierta en bloque de código."""
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


logo_main_b64 = img_to_base64(LOGO_MAIN)
logo_company_b64 = img_to_base64(LOGO_COMPANY)

mini_logo = (
    f'<img src="data:image/png;base64,{logo_main_b64}" alt="No-Limit_PDF">'
    if logo_main_b64 else '<div class="brand-fallback">∞</div>'
)

company_logo = (
    f'<img src="data:image/png;base64,{logo_company_b64}" alt="RelaxLife-Apps">'
    if logo_company_b64 else '<div class="brand-fallback">R</div>'
)


# ============================================================
# CSS
# ============================================================

html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Ubuntu', sans-serif !important;
}

.stApp {
    background-color: #ffffff;
    color: #000000;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1180px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.topbar {
    width: 100%;
    border-bottom: 1px solid #e5e5e5;
    padding: 0.75rem 0 0.9rem 0;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand-mini {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-weight: 700;
    font-size: 1.15rem;
    color: #000000;
}

.brand-mini img {
    height: 46px;
    max-width: 150px;
    object-fit: contain;
}

.brand-fallback {
    width: 42px;
    height: 42px;
    border: 2px solid #000000;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 700;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.95rem;
    color: #000000;
}

.nav-links a {
    text-decoration: none;
    color: #000000;
}

.lang-pill {
    border: 1px solid #000000;
    border-radius: 999px;
    padding: 0.25rem 0.65rem;
    font-weight: 700;
    font-size: 0.82rem;
    line-height: 1.2;
}

.lang-pill.active {
    background: #000000;
    color: #ffffff;
}

.hero {
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 1.8rem;
}

.hero img {
    width: 390px;
    max-width: 88%;
    object-fit: contain;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -1.2px;
    color: #000000;
    margin: 0;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 400;
    color: #000000;
    margin-top: 0.15rem;
}

.hero-description {
    font-size: 1rem;
    color: #000000;
    margin-top: 0.7rem;
}

.card-shell {
    max-width: 980px;
    margin: 0 auto 2rem auto;
}

section[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #d9d9d9 !important;
    border-radius: 20px !important;
    box-shadow: 0 12px 35px rgba(0,0,0,0.08) !important;
    background: #ffffff !important;
}

.section-title {
    font-size: 1.07rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 0.4rem;
}

.section-text {
    font-size: 0.92rem;
    line-height: 1.45;
    color: #111111;
}

.hr-soft {
    border-top: 1px solid #e6e6e6;
    margin: 0.6rem 0 0.8rem 0;
}

div[data-testid="stFileUploader"] {
    border: 2px dashed #000000;
    border-radius: 16px;
    padding: 1rem 1rem 0.7rem 1rem;
    background: #ffffff;
}

div[data-testid="stFileUploader"] section {
    border: none !important;
    padding: 0 !important;
}

div[data-testid="stFileUploader"] button {
    background: #000000 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #000000 !important;
    font-weight: 700 !important;
    font-family: 'Ubuntu', sans-serif !important;
}

div[data-testid="stFileUploader"] small {
    color: #000000 !important;
}

div[data-testid="stTextInput"] input {
    border: 1.5px solid #000000;
    border-radius: 10px;
    padding: 0.75rem;
    color: #000000;
    background: #ffffff;
    font-family: 'Ubuntu', sans-serif !important;
}

div[data-testid="stTextInput"] label {
    color: #000000 !important;
    font-family: 'Ubuntu', sans-serif !important;
}

div.stButton > button,
div.stDownloadButton > button {
    width: 100%;
    height: 3.2rem;
    background: #000000;
    color: #ffffff;
    border: 1px solid #000000;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    font-family: 'Ubuntu', sans-serif !important;
    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: #ffffff;
    color: #000000;
    border: 1px solid #000000;
}

.result-card {
    max-width: 980px;
    margin: 1.5rem auto;
    border: 1px solid #000000;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    background: #ffffff;
}

.steps {
    max-width: 980px;
    margin: 2rem auto 1.6rem auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
}

.step-card {
    border-right: 1px solid #d9d9d9;
    padding: 0.6rem 1.4rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.step-card:last-child {
    border-right: none;
}

.step-number {
    min-width: 32px;
    min-height: 32px;
    border-radius: 50%;
    background: #000000;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}

.step-title, .feature-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.25rem;
}

.step-text, .feature-text {
    font-size: 0.88rem;
    line-height: 1.35;
}

.features {
    max-width: 980px;
    margin: 1.6rem auto 1.8rem auto;
    border-top: 1px solid #d9d9d9;
    padding-top: 1.4rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}

.feature {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 0.5rem 1rem;
}

.feature-icon {
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}

.footer-custom {
    margin-top: 2.5rem;
    padding: 1.2rem 0 0.5rem 0;
    border-top: 1px solid #e5e5e5;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    gap: 1rem;
    font-size: 0.9rem;
    color: #000000;
}

.footer-brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    font-weight: 700;
    font-size: 1.05rem;
}

.footer-brand img {
    height: 52px;
    max-width: 170px;
    object-fit: contain;
}

.footer-center { text-align: center; }
.footer-links { text-align: right; }
.footer-links span { margin-left: 1rem; }

@media (max-width: 850px) {
    .topbar { align-items: flex-start; gap: 1rem; }
    .brand-mini span { font-size: 1rem; }
    .nav-links { gap: 0.45rem; flex-wrap: wrap; justify-content: flex-end; }
    .nav-links span { display: none; }
    .hero img { width: 300px; }
    .hero-title { font-size: 2.25rem; }
    .steps, .features, .footer-custom { grid-template-columns: 1fr; }
    .step-card { border-right: none; border-bottom: 1px solid #d9d9d9; }
    .step-card:last-child { border-bottom: none; }
    .footer-center, .footer-links { text-align: left; }
    .footer-links span { margin-left: 0; margin-right: 1rem; }
}
</style>
""")


# ============================================================
# FUNCIONES DE PROCESAMIENTO
# ============================================================

def extraer_rar(rar_path: str, extract_dir: str) -> None:
    comando = [
        "unar",
        "-quiet",
        "-force-overwrite",
        "-output-directory",
        extract_dir,
        rar_path,
    ]
    resultado = subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if resultado.returncode != 0:
        detalle = resultado.stderr.strip() or resultado.stdout.strip()
        raise RuntimeError(f"{T['rar_error']}\n\n{detalle}")


def buscar_pdfs(carpeta: str) -> list[str]:
    pdfs = []
    for root, _, files in os.walk(carpeta):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, file))
    return natsorted(pdfs)


def unir_pdfs(pdf_files: list[str]) -> tuple[bytes, list[tuple[str, str]]]:
    writer = PdfWriter()
    errores = []
    for pdf in pdf_files:
        try:
            writer.append(pdf)
        except Exception as e:
            errores.append((pdf, str(e)))

    if len(writer.pages) == 0:
        raise RuntimeError(T["pdf_error"])

    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer.getvalue(), errores


# ============================================================
# ESTADO
# ============================================================

if "pdf_final" not in st.session_state:
    st.session_state["pdf_final"] = None
if "nombre_salida" not in st.session_state:
    st.session_state["nombre_salida"] = T["output_default"]
if "lista_pdfs" not in st.session_state:
    st.session_state["lista_pdfs"] = []
if "errores" not in st.session_state:
    st.session_state["errores"] = []


# ============================================================
# INTERFAZ
# ============================================================

html(f"""
<div class="topbar">
    <div class="brand-mini">
        {mini_logo}
        <span>No-Limit_PDF</span>
    </div>
    <div class="nav-links">
        <span>{T['about']}</span>
        <span>{T['help']}</span>
        <a class="lang-pill {active_es}" href="?lang=es">ES</a>
        <a class="lang-pill {active_pt}" href="?lang=pt">PT</a>
        <a class="lang-pill {active_en}" href="?lang=en">EN</a>
    </div>
</div>
""")

if logo_main_b64:
    html(f"""
    <div class="hero">
        <img src="data:image/png;base64,{logo_main_b64}" alt="No-Limit_PDF">
        <div class="hero-description">{T['description']}</div>
    </div>
    """)
else:
    html(f"""
    <div class="hero">
        <h1 class="hero-title">No-Limit_PDF</h1>
        <div class="hero-subtitle">{T['tagline']}</div>
        <div class="hero-description">{T['description']}</div>
    </div>
    """)


# Tarjeta principal nativa de Streamlit: evita el bug del cuadro vacío.
_, main_col, _ = st.columns([0.08, 0.84, 0.08])

with main_col:
    with st.container(border=True):
        c1, c2 = st.columns([1, 1.6])
        with c1:
            html(f"""
            <div class="section-title">{T['upload_title']}</div>
            <div class="section-text">{T['upload_desc']}</div>
            """)
        with c2:
            uploaded_file = st.file_uploader(
                T["upload_label"],
                type=["rar"],
                accept_multiple_files=False,
            )

        html('<div class="hr-soft"></div>')

        c1, c2 = st.columns([1, 1.6])
        with c1:
            html(f"""
            <div class="section-title">{T['output_title']}</div>
            <div class="section-text">{T['output_desc']}</div>
            """)
        with c2:
            nombre_salida = st.text_input(
                T["output_label"],
                value=T["output_default"],
                label_visibility="collapsed",
            )
            if not nombre_salida.lower().endswith(".pdf"):
                nombre_salida += ".pdf"

        html('<div class="hr-soft"></div>')

        c1, c2 = st.columns([1, 1.6])
        with c1:
            html(f"""
            <div class="section-title">{T['merge_title']}</div>
            <div class="section-text">{T['merge_desc']}</div>
            """)
        with c2:
            procesar = st.button(T["merge_button"])


# ============================================================
# PROCESAMIENTO
# ============================================================

if procesar:
    if uploaded_file is None:
        st.error(T["upload_error"])
    else:
        with st.spinner(T["processing"]):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    rar_path = os.path.join(tmpdir, uploaded_file.name)
                    extract_dir = os.path.join(tmpdir, "extraido")
                    os.makedirs(extract_dir, exist_ok=True)

                    with open(rar_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    extraer_rar(rar_path, extract_dir)
                    pdf_files = buscar_pdfs(extract_dir)

                    if len(pdf_files) == 0:
                        raise ValueError(T["no_pdfs"])

                    pdf_final, errores = unir_pdfs(pdf_files)

                    st.session_state["pdf_final"] = pdf_final
                    st.session_state["nombre_salida"] = nombre_salida
                    st.session_state["lista_pdfs"] = [
                        os.path.relpath(pdf, extract_dir) for pdf in pdf_files
                    ]
                    st.session_state["errores"] = errores

                st.success(T["success"].format(n=len(st.session_state["lista_pdfs"])))

            except Exception as e:
                st.session_state["pdf_final"] = None
                st.error(str(e))


# ============================================================
# RESULTADOS
# ============================================================

if st.session_state["pdf_final"] is not None:
    html('<div class="result-card">')
    st.download_button(
        label=T["download"],
        data=st.session_state["pdf_final"],
        file_name=st.session_state["nombre_salida"],
        mime="application/pdf",
    )

    with st.expander(T["view_files"]):
        for i, pdf in enumerate(st.session_state["lista_pdfs"], start=1):
            st.write(f"{i}. {pdf}")

    if st.session_state["errores"]:
        with st.expander(T["view_errors"]):
            for pdf, error in st.session_state["errores"]:
                st.write(f"**{pdf}**")
                st.code(error)
    html('</div>')


# ============================================================
# PASOS Y CARACTERÍSTICAS
# ============================================================

html(f"""
<div class="steps">
    <div class="step-card">
        <div class="step-number">1</div>
        <div>
            <div class="step-title">{T['step1_title']}</div>
            <div class="step-text">{T['step1_text']}</div>
        </div>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div>
            <div class="step-title">{T['step2_title']}</div>
            <div class="step-text">{T['step2_text']}</div>
        </div>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div>
            <div class="step-title">{T['step3_title']}</div>
            <div class="step-text">{T['step3_text']}</div>
        </div>
    </div>
</div>
""")

html(f"""
<div class="features">
    <div class="feature">
        <div class="feature-icon">↯</div>
        <div>
            <div class="feature-title">{T['fast_title']}</div>
            <div class="feature-text">{T['fast_text']}</div>
        </div>
    </div>
    <div class="feature">
        <div class="feature-icon">◉</div>
        <div>
            <div class="feature-title">{T['private_title']}</div>
            <div class="feature-text">{T['private_text']}</div>
        </div>
    </div>
    <div class="feature">
        <div class="feature-icon">∞</div>
        <div>
            <div class="feature-title">{T['unlimited_title']}</div>
            <div class="feature-text">{T['unlimited_text']}</div>
        </div>
    </div>
</div>
""")


# ============================================================
# FOOTER
# ============================================================

html(f"""
<div class="footer-custom">
    <div class="footer-brand">
        {company_logo}
        <span>RelaxLife-Apps</span>
    </div>
    <div class="footer-center">
        © 2025 RelaxLife-Apps. {T['footer_rights']}
    </div>
    <div class="footer-links">
        <span>{T['privacy']}</span>
        <span>{T['terms']}</span>
        <span>{T['contact']}</span>
    </div>
</div>
""")
