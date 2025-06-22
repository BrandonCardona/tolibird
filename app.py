import streamlit as st
from funciones.prediccion import clasificar_ave
from funciones.especieAves import mostrar_especies
from funciones.presentacion import mostrar_inicio
from funciones.registro import registrar_prediccion
from funciones.verRegistros import mostrar_registros_guardados

st.set_page_config(page_title="Clasificador de Aves", page_icon="🦜", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "section" not in st.session_state:
    st.session_state.section = "Resumen"

with st.sidebar:
    st.markdown('<div class="sidebar-title">🦜 Clasificador de Aves</div>', unsafe_allow_html=True)
    if st.button("🏠 Inicio"):
        st.session_state.section = "Inicio"
    if st.button("📚 Especies Registradas"):
        st.session_state.section = "EspeciesRegistradas"
    if st.button("🖼️ Clasificación de aves"):
        st.session_state.section = "Predicciones"
    if st.button("📝 Registrar una predicción"):
        st.session_state.section = "RegistroPrediccion"
    if st.button("📂 Visualizar Registros"):
        st.session_state.section = "RegistrosGuardados"
    st.markdown("---")

if st.session_state.section == "EspeciesRegistradas":
    mostrar_especies()
elif st.session_state.section == "Predicciones":
    clasificar_ave()
elif st.session_state.section == "Inicio":
    mostrar_inicio()
elif st.session_state.section == "RegistroPrediccion":
    registrar_prediccion()
elif st.session_state.section == "RegistrosGuardados":
    mostrar_registros_guardados()
