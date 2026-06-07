import os
import io
import base64
import tempfile
import subprocess

import streamlit as st
from pypdf import PdfWriter
from natsort import natsorted


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="No-Limit_PDF",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# RUTAS DE LOGOS
# ============================================================

LOGO_MAIN = "assets/no_limit_pdf.png"
LOGO_COMPANY = "assets/relaxlife_apps.png"


def img_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()


logo_main_b64 = img_to_base64(LOGO_MAIN)
logo_company_b64 = img_to_base64(LOGO_COMPANY)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Ubuntu', sans-serif !important;
    }

    .stApp {
        background-color: #ffffff;
        color: #000000;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1180px;
    }

    .topbar {
        width: 100%;
        border-bottom: 1px solid #e5e5e5;
        padding: 0.8rem 0 1rem 0;
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
        font-size: 1.2rem;
        color: #000000;
    }

    .brand-mini img {
        height: 42px;
        object-fit: contain;
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 1.8rem;
        font-size: 0.95rem;
        color: #000000;
    }

    .hero {
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.8rem;
    }

    .hero img {
        width: 360px;
        max-width: 88%;
        object-fit: contain;
        margin-bottom: 0.3rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -1px;
        margin-top: -0.5rem;
        color: #000000;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #000000;
        margin-top: 0.1rem;
    }

    .main-card {
        background: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 18px;
        padding: 2rem 2rem;
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
        margin: 0 auto 2rem auto;
        max-width: 980px;
    }

    .section-row {
        display: grid;
        grid-template-columns: 1fr 1.6fr;
        gap: 2rem;
        align-items: center;
        padding: 1.1rem 0;
        border-bottom: 1px solid #e6e6e6;
    }

    .section-row:last-child {
        border-bottom: none;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 0.4rem;
    }

    .section-text {
        font-size: 0.92rem;
        line-height: 1.45;
        color: #111111;
    }

    div[data-testid="stFileUploader"] {
        border: 2px dashed #000000;
        border-radius: 16px;
        padding: 1.1rem;
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

    div.stButton > button {
        width: 100%;
        height: 3.2rem;
        background: #000000;
        color: #ffffff;
        border: 1px solid #000000;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        background: #ffffff;
        color: #000000;
        border: 1px solid #000000;
    }

    div.stDownloadButton > button {
        width: 100%;
        height: 3.2rem;
        background: #000000;
        color: #ffffff;
        border: 1px solid #000000;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
    }

    div.stDownloadButton > button:hover {
        background: #ffffff;
        color: #000000;
        border: 1px solid #000000;
    }

    .steps {
        max-width: 980px;
        margin: 1.8rem auto;
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

    .step-title {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    .step-text {
        font-size: 0.88rem;
        line-height: 1.35;
    }

    .features {
        max-width: 980px;
        margin: 1.8rem auto;
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
    }

    .feature-title {
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .feature-text {
        font-size: 0.88rem;
        line-height: 1.35;
    }

    .result-card {
        max-width: 980px;
        margin: 1.5rem auto;
        border: 1px solid #000000;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        background: #ffffff;
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
        height: 48px;
        object-fit: contain;
    }

    .footer-center {
        text-align: center;
    }

    .footer-links {
        text-align: right;
    }

    .footer-links span {
        margin-left: 1rem;
    }

    @media (max-width: 850px) {
        .section-row {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .steps,
        .features,
        .footer-custom {
            grid-template-columns: 1fr;
        }

        .step-card {
            border-right: none;
            border-bottom: 1px solid #d9d9d9;
        }

        .footer-center,
        .footer-links {
            text-align: left;
        }

        .nav-links {
            display: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DEL PROCESAMIENTO
# ============================================================

def extraer_rar(rar_path: str, extract_dir: str) -> None:
    comando = [
        "unar",
        "-quiet",
        "-force-overwrite",
        "-output-directory",
        extract_dir,
        rar_path
    ]

    resultado = subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            "No se pudo extraer el archivo .rar. "
            "Puede estar dañado, protegido con contraseña o usar un formato no soportado.\n\n"
            f"Detalle técnico:\n{resultado.stderr}"
        )


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
        raise RuntimeError(
            "No se pudo unir ningún PDF válido. "
            "Verifica que los archivos no estén dañados o protegidos."
        )

    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)

    return buffer.getvalue(), errores


# ============================================================
# ESTADO DE LA APP
# ============================================================

if "pdf_final" not in st.session_state:
    st.session_state["pdf_final"] = None

if "nombre_salida" not in st.session_state:
    st.session_state["nombre_salida"] = "merged.pdf"

if "lista_pdfs" not in st.session_state:
    st.session_state["lista_pdfs"] = []

if "errores" not in st.session_state:
    st.session_state["errores"] = []


# ============================================================
# INTERFAZ SUPERIOR
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <div class="brand-mini">
            <img src="data:image/png;base64,{logo_main_b64}">
            <span>No-Limit_PDF</span>
        </div>
        <div class="nav-links">
            <span>ⓘ About</span>
            <span>?</span>
            <span>Help</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="hero">
        <img src="data:image/png;base64,{logo_main_b64}">
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TARJETA PRINCIPAL
# ============================================================

st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-row">
        <div>
            <div class="section-title">1. Upload your RAR file</div>
            <div class="section-text">
                Upload a <strong>.rar</strong> file containing the PDF files you want to merge.
            </div>
        </div>
        <div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drag & drop your .rar file here or click to browse",
    type=["rar"],
    accept_multiple_files=False,
    label_visibility="collapsed"
)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-row">
        <div>
            <div class="section-title">2. Output file name</div>
            <div class="section-text">
                Choose the name of the final merged PDF.
            </div>
        </div>
        <div>
    """,
    unsafe_allow_html=True
)

nombre_salida = st.text_input(
    "Output file name",
    value="merged.pdf",
    label_visibility="collapsed"
)

if not nombre_salida.lower().endswith(".pdf"):
    nombre_salida += ".pdf"

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-row">
        <div>
            <div class="section-title">3. Merge</div>
            <div class="section-text">
                Click the button to start merging your PDF files.
            </div>
        </div>
        <div>
    """,
    unsafe_allow_html=True
)

procesar = st.button("Merge PDFs")

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PROCESAMIENTO
# ============================================================

if procesar:
    if uploaded_file is None:
        st.error("Please upload a .rar file before continuing.")
    else:
        with st.spinner("Processing your file..."):
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
                        raise ValueError("No PDF files were found inside the .rar file.")

                    pdf_final, errores = unir_pdfs(pdf_files)

                    st.session_state["pdf_final"] = pdf_final
                    st.session_state["nombre_salida"] = nombre_salida
                    st.session_state["lista_pdfs"] = [
                        os.path.relpath(pdf, extract_dir)
                        for pdf in pdf_files
                    ]
                    st.session_state["errores"] = errores

                st.success(
                    f"PDF merged successfully. {len(st.session_state['lista_pdfs'])} PDF files were processed."
                )

            except Exception as e:
                st.session_state["pdf_final"] = None
                st.error(str(e))


# ============================================================
# RESULTADOS
# ============================================================

if st.session_state["pdf_final"] is not None:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    st.download_button(
        label="Download merged PDF",
        data=st.session_state["pdf_final"],
        file_name=st.session_state["nombre_salida"],
        mime="application/pdf"
    )

    with st.expander("View merged PDF files"):
        for i, pdf in enumerate(st.session_state["lista_pdfs"], start=1):
            st.write(f"{i}. {pdf}")

    if st.session_state["errores"]:
        with st.expander("View files that could not be merged"):
            for pdf, error in st.session_state["errores"]:
                st.write(f"**{pdf}**")
                st.code(error)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PASOS
# ============================================================

st.markdown(
    """
    <div class="steps">
        <div class="step-card">
            <div class="step-number">1</div>
            <div>
                <div class="step-title">Upload</div>
                <div class="step-text">Upload a .rar file containing multiple PDF files.</div>
            </div>
        </div>

        <div class="step-card">
            <div class="step-number">2</div>
            <div>
                <div class="step-title">Merge</div>
                <div class="step-text">We merge them in natural file-name order.</div>
            </div>
        </div>

        <div class="step-card">
            <div class="step-number">3</div>
            <div>
                <div class="step-title">Download</div>
                <div class="step-text">Download your merged PDF instantly.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARACTERÍSTICAS
# ============================================================

st.markdown(
    """
    <div class="features">
        <div class="feature">
            <div class="feature-icon">↯</div>
            <div>
                <div class="feature-title">Fast</div>
                <div class="feature-text">High-speed PDF merging directly from your uploaded file.</div>
            </div>
        </div>

        <div class="feature">
            <div class="feature-icon">◉</div>
            <div>
                <div class="feature-title">Private</div>
                <div class="feature-text">Files are processed temporarily and are not kept permanently.</div>
            </div>
        </div>

        <div class="feature">
            <div class="feature-icon">∞</div>
            <div>
                <div class="feature-title">Unlimited</div>
                <div class="feature-text">Merge many PDF files into one clean final document.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer-custom">
        <div class="footer-brand">
            <img src="data:image/png;base64,{logo_company_b64}">
            <span>RelaxLife-Apps</span>
        </div>

        <div class="footer-center">
            © 2025 RelaxLife-Apps. All rights reserved.
        </div>

        <div class="footer-links">
            <span>Privacy</span>
            <span>Terms</span>
            <span>Contact</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
