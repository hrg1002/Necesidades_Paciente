import streamlit as st
import bcrypt
import json
import os
from gtts import gTTS
from io import BytesIO
from PIL import Image

# ---------- CONFIGURACIÓN DE PÁGINA Y ESTILO GLOBAL ----------
st.set_page_config(page_title="DiloConPics", layout="wide")

# Estilo global
st.markdown("""
    <style>
    .stApp {
        background-color: #EDE8D0;
    }
    input, textarea {
        border: 2px solid white !important;
        background-color: white !important;
        color: black !important;
    }
    .stTextInput > div > div > input {
        border: 2px solid white !important;
        background-color: white !important;
        color: black !important;
    }
    button {
        background-color: white !important;
        color: black !important;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, label {
        color: black !important;
    }
    .logo-container {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo siempre arriba a la derecha
logo = Image.open("logo.png")
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image(logo, width=80)
st.markdown('</div>', unsafe_allow_html=True)

# Función para centrar contenido
def centrar_contenido(contenido):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        contenido()

# --------------------- GESTIÓN DE USUARIOS ---------------------
USERS_FILE = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f)

def registrar_usuario(nombre_usuario, contraseña):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        return False
    hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
    usuarios[nombre_usuario] = hashed.decode()
    guardar_usuarios(usuarios)
    return True

def verificar_credenciales(nombre_usuario, contraseña):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        return bcrypt.checkpw(contraseña.encode(), usuarios[nombre_usuario].encode())
    return False

# --------------------- ESTADO DE LA APP ---------------------
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "auth"
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# --------------------- FUNCIONES DE PICTOGRAMAS ---------------------
def mostrar_pictogramas(palabras):
    cols = st.columns(4)
    for i, palabra in enumerate(palabras):
        with cols[i % 4]:
            ruta_imagen = os.path.join("datos", f"{palabra}.png")
            if os.path.exists(ruta_imagen):
                st.image(ruta_imagen, use_container_width=True)
                st.markdown(f"<p style='text-align: center; color: black; font-weight: bold;'>{palabra.capitalize()}</p>", unsafe_allow_html=True)
            else:
                st.warning(f"No se encontró la imagen para '{palabra}'")
            try:
                tts = gTTS(text=palabra, lang='es')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"No se pudo generar audio para '{palabra}': {e}")

# --------------------- INTERFAZ DE LOGIN ---------------------
if st.session_state.pantalla == "auth":
    def login_ui():
        st.title("DiloConPics")
        st.subheader("Iniciar sesión")
        usuario = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            if verificar_credenciales(usuario, password):
                st.success("¡Inicio de sesión exitoso!")
                st.session_state.usuario = usuario
                st.session_state.pantalla = "inicio"
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        if st.button("Registrarse"):
            st.session_state.pantalla = "registro"
            st.rerun()

    centrar_contenido(login_ui)

# --------------------- INTERFAZ DE REGISTRO ---------------------
elif st.session_state.pantalla == "registro":
    def registro_ui():
        st.title("Registrarse")
        nuevo_usuario = st.text_input("Nuevo usuario")
        nueva_contra = st.text_input("Nueva contraseña", type="password")

        if st.button("Crear cuenta"):
            if registrar_usuario(nuevo_usuario, nueva_contra):
                st.success("Usuario creado. Ahora puedes iniciar sesión.")
                st.session_state.pantalla = "auth"
                st.rerun()
            else:
                st.error("Ese usuario ya existe.")

        if st.button("Volver al inicio de sesión"):
            st.session_state.pantalla = "auth"
            st.rerun()

    centrar_contenido(registro_ui)

# --------------------- INTERFAZ PRINCIPAL ---------------------
elif st.session_state.pantalla == "inicio":
    st.markdown(f"### Bienvenido: {st.session_state.usuario}")
    if st.button("Cerrar sesión"):
        st.session_state.pantalla = "auth"
        st.session_state.usuario = None
        st.rerun()

    st.markdown("<h1 style='text-align: center;'>DiloConPics</h1>", unsafe_allow_html=True)

    if "pantalla_app" not in st.session_state:
        st.session_state.pantalla_app = "inicio"

    if st.session_state.pantalla_app == "inicio":
        st.subheader("Selecciona una categoría:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Yo"):
                st.session_state.pantalla_app = "yo"
        with col2:
            if st.button("Emociones"):
                st.session_state.pantalla_app = "emociones"
        with col3:
            if st.button("Casa"):
                st.session_state.pantalla_app = "casa"

        palabras = ["Izquierda","Sí","No","Derecha"]
        mostrar_pictogramas(palabras)

    elif st.session_state.pantalla_app == "yo":
        st.subheader("Categoría: Yo")
        palabras = ["yo", "niño", "niña", "persona", "tú", "mamá", "papá", "familia"]
        mostrar_pictogramas(palabras)
        if st.button("Volver"):
            st.session_state.pantalla_app = "inicio"

        palabras = ["Izquierda","Sí","No","Derecha"]
        mostrar_pictogramas(palabras)

    elif st.session_state.pantalla_app == "emociones":
        st.subheader("Categoría: Emociones")
        palabras = ["Miedo", "triste", "enfadada", "sorprendida", "cansada", "asustada", "aburrida", "contenta"]
        mostrar_pictogramas(palabras)
        if st.button("Volver"):
            st.session_state.pantalla_app = "inicio"
        palabras = ["Izquierda","Sí","No","Derecha"]
        mostrar_pictogramas(palabras)

    elif st.session_state.pantalla_app == "casa":
        st.subheader("Categoría: Casa")
        palabras = ["casa", "cama", "baño", "cocina", "comedor", "puerta", "ventana", "sofá"]
        mostrar_pictogramas(palabras)
        if st.button("Volver"):
            st.session_state.pantalla_app = "inicio"
        palabras = ["Izquierda","Sí","No","Derecha"]
        mostrar_pictogramas(palabras)


