import streamlit as st
from gtts import gTTS
import requests
from io import BytesIO

import streamlit as st

# Inicializamos la variable de estado si no existe
# Inicializamos la variable de estado si no existe
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

st.set_page_config(page_title="DiloConPics", layout="wide")



# CSS personalizado
st.markdown("""
    <style>
    .stApp {
        background-color: #EDE8D0;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, label, .css-10trblm, .css-1v0mbdj, .css-qbe2hs {
        color: black !important;
    }
    .stAlert, .css-ffhzg2, .css-1xarl3l, .stException, .stMarkdown p {
        color: black !important;
    }
    figcaption {
        color: black !important;
        opacity: 1 !important;
        font-weight: bold;
    }
    button {
        background-color: white !important;
        color: black !important;
    }
    .logo-right {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 100;
    }
    </style>
    <div class="logo-right">
        <img src="logo.png" width="80">
    </div>
""", unsafe_allow_html=True)



# Contenedor del logo
with st.container():
    st.markdown('<div class="logo-right">', unsafe_allow_html=True)
    st.image("logo.png", width=80)
    st.markdown('</div>', unsafe_allow_html=True)

# Título centrado
st.markdown(
    """
    <h1 style='text-align: center;'>
        DiloConPics
    </h1>
    """,
    unsafe_allow_html=True
)


import os
import streamlit as st
from gtts import gTTS
from io import BytesIO

def mostrar_pictogramas(palabras):
    cols = st.columns(4)  # 4 columnas

    for i, palabra in enumerate(palabras):
        with cols[i % 4]:
            # Cargar imagen desde carpeta "datos"
            ruta_imagen = os.path.join("datos", f"{palabra}.png")
            if os.path.exists(ruta_imagen):
                st.image(ruta_imagen, caption=palabra.capitalize(), use_container_width=True)
            else:
                st.warning(f"No se encontró la imagen para '{palabra}'")

            # Generar y reproducir audio
            try:
                tts = gTTS(text=palabra, lang='es')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"No se pudo generar audio para '{palabra}': {e}")



# Página de inicio
if st.session_state.pantalla == "inicio":
    st.subheader("Selecciona una categoría:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Yo"):
            st.session_state.pantalla = "yo"
    with col2:
        if st.button("Emociones"):
            st.session_state.pantalla = "emociones"
    with col3:
        if st.button("Casa"):
            st.session_state.pantalla = "casa"

# Pantallas de pictogramas
elif st.session_state.pantalla == "yo":
    st.subheader("Categoría: Yo")
    palabras = ["yo", "niño", "niña", "persona", "tú", "mamá", "papá", "familia"]
    mostrar_pictogramas(palabras)
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"

elif st.session_state.pantalla == "emociones":
    st.subheader("Categoría: Emociones")
    palabras = ["Miedo", "triste", "enfadada", "sorprendida", "cansada", "asustada", "aburrida", "contenta"]
    mostrar_pictogramas(palabras)
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"

elif st.session_state.pantalla == "casa":
    st.subheader("Categoría: Casa")
    palabras = ["casa", "cama", "baño", "cocina", "comedor", "puerta", "ventana", "sofá"]
    mostrar_pictogramas(palabras)
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"
