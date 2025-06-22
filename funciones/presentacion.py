import streamlit as st
import os

def mostrar_inicio():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    imagen_path = os.path.join(base_dir, "../img/inicio.jpeg")
    col1, col2 = st.columns([2, 3])

    with col1:
        st.image(imagen_path, use_container_width=True)

    with col2:
        st.markdown("## 🐦 **Bienvenido a Tolibird**")
        st.markdown(
            "#### Sistema de identificación aviar basado en inteligencia artificial"
        )

        st.markdown("### ¿Cómo usar el sistema?")
        st.markdown("""
1. Selecciona **Clasificación de Aves** en el menú lateral  
2. Sube una imagen clara del ave a identificar  
3. Revisa las predicciones generadas por el modelo  
4. Explora la información detallada de cada especie  
        """)

        st.markdown("### Características principales:")
        st.markdown("""
- Identificación de 20 especies de aves del Tolima  
- Información científica actualizada  
- Modelo de **Deep Learning** optimizado  
- Interfaz intuitiva y accesible  
        """)

    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; font-size: 12px; color: gray;'>Desarrollado por Brandon Cardona y David Acosta</p>",
        unsafe_allow_html=True
    )