import streamlit as st

# Inicializamos la variable de estado si no existe
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

st.set_page_config(page_title="App de Pictogramas", layout="centered")

st.title("Aplicación de Pictogramas")

# CSS para cambiar el fondo
page_bg_color = """
     <style>
     .stApp {
         background-color: #FFA500; /* Cambia a azul cielo */
     }
     </style>
 """
st.markdown(page_bg_color, unsafe_allow_html=True)

# Lógica de navegación
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

# Pantalla: Yo
elif st.session_state.pantalla == "yo":
    st.subheader("Categoría: Yo")
    st.write("Aquí irían los pictogramas relacionados con la persona.")
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"

# Pantalla: Emociones
elif st.session_state.pantalla == "emociones":
    st.subheader("Categoría: Emociones")
    st.write("Aquí irían los pictogramas de emociones.")
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"

# Pantalla: Casa
elif st.session_state.pantalla == "casa":
    st.subheader("Categoría: Casa")
    st.write("Aquí irían los pictogramas relacionados con el hogar.")
    if st.button("Volver"):
        st.session_state.pantalla = "inicio"
