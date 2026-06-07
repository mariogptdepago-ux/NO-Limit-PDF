import os
import io
import shutil
import tempfile
import subprocess

import streamlit as st
from pypdf import PdfWriter
from natsort import natsorted


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Unir PDF desde RAR",
    page_icon="📄",
    layout="centered"
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f7f9fc 0%, #eef3ff 100%);
    }

    .title-box {
        background: white;
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #e8ecf5;
    }

    .title-box h1 {
        color: #1f2937;
        font-size: 2.3rem;
        margin-bottom: 0.4rem;
    }

    .title-box p {
        color: #6b7280;
        font-size: 1.05rem;
    }

    .info-card {
        background: #ffffff;
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .success-card {
        background: #ecfdf5;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #a7f3d0;
        color: #065f46;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .error-card {
        background: #fef2f2;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #fecaca;
        color: #991b1b;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    div.stButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
    }

    div.stDownloadButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
        background-color: #2563eb;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES
# ============================================================

def extraer_rar(rar_path: str, extract_dir: str) -> None:
    """
    Extrae un archivo .rar usando unar.
    En Streamlit Cloud, unar se instala desde packages.txt.
    """

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
    """
    Busca recursivamente todos los PDF dentro de una carpeta.
    """

    pdfs = []

    for root, _, files in os.walk(carpeta):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, file))

    return natsorted(pdfs)


def unir_pdfs(pdf_files: list[str]) -> tuple[bytes, list[tuple[str, str]]]:
    """
    Une los PDF encontrados y devuelve el archivo final en memoria.
    También devuelve una lista de errores si algún PDF no se pudo unir.
    """

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
# INTERFAZ
# ============================================================

st.markdown(
    """
    <div class="title-box">
        <h1>📄 Unificador de PDF</h1>
        <p>Sube un archivo <strong>.rar</strong> con varios PDF y descarga un único documento unido.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
        <strong>Instrucciones:</strong><br>
        1. Comprime tus PDF en una carpeta <code>.rar</code>.<br>
        2. Sube el archivo desde tu computador.<br>
        3. Presiona <strong>Unir PDF</strong>.<br>
        4. Descarga el archivo final.
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Selecciona tu archivo .rar",
    type=["rar"],
    accept_multiple_files=False
)

nombre_salida = st.text_input(
    "Nombre del PDF final",
    value="PDF_UNIDO_FINAL.pdf"
)

if not nombre_salida.lower().endswith(".pdf"):
    nombre_salida += ".pdf"


if "pdf_final" not in st.session_state:
    st.session_state["pdf_final"] = None

if "nombre_salida" not in st.session_state:
    st.session_state["nombre_salida"] = nombre_salida

if "lista_pdfs" not in st.session_state:
    st.session_state["lista_pdfs"] = []


procesar = st.button("🚀 Unir PDF")


if procesar:
    if uploaded_file is None:
        st.error("Por favor sube un archivo .rar antes de continuar.")
    else:
        with st.spinner("Procesando archivo. Esto puede tardar según el tamaño del .rar..."):
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
                        raise ValueError(
                            "No se encontraron archivos PDF dentro del .rar."
                        )

                    pdf_final, errores = unir_pdfs(pdf_files)

                    st.session_state["pdf_final"] = pdf_final
                    st.session_state["nombre_salida"] = nombre_salida
                    st.session_state["lista_pdfs"] = [
                        os.path.relpath(pdf, extract_dir)
                        for pdf in pdf_files
                    ]
                    st.session_state["errores"] = errores

                st.markdown(
                    f"""
                    <div class="success-card">
                        ✅ PDF unido correctamente.<br>
                        Se procesaron <strong>{len(st.session_state["lista_pdfs"])}</strong> archivos PDF.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.session_state["pdf_final"] = None
                st.markdown(
                    f"""
                    <div class="error-card">
                        ❌ Ocurrió un error:<br><br>
                        {str(e)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


if st.session_state["pdf_final"] is not None:
    st.download_button(
        label="⬇️ Descargar PDF unido",
        data=st.session_state["pdf_final"],
        file_name=st.session_state["nombre_salida"],
        mime="application/pdf"
    )

    with st.expander("Ver archivos PDF unidos"):
        for i, pdf in enumerate(st.session_state["lista_pdfs"], start=1):
            st.write(f"{i}. {pdf}")

    errores = st.session_state.get("errores", [])

    if errores:
        with st.expander("Ver archivos que no se pudieron unir"):
            for pdf, error in errores:
                st.write(f"**{pdf}**")
                st.code(error)


st.markdown("---")
st.caption("Herramienta creada para unir múltiples PDF contenidos en un archivo .rar.")