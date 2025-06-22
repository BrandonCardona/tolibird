import streamlit as st
import numpy as np
import cv2
import os
import pandas as pd
from keras.applications.imagenet_utils import preprocess_input
from PIL import Image
from utils.modelo import cargar_modelo

def clasificar_ave():
    st.title("🖼️ Clasificación de aves según su imagen")
    
    names = ['Solitario Andino','Zorzal sp.','Zorzal Cara Gris', 'Zorzal Pico Naranja', 'Zorzal Sabiá','Zorzal Ventripálido', 
             'Zorzalito Sombrío','Zorzal de Anteojos', 'Zorzal Canelo','Mirlo Azulado', 'Matraca Tropical','Cucarachero Currucuchú', 
             'Cucarachero Ventrinegro','Saltapared Común', 'Chochín Montañés','Cucarachero Ruiseñor Sureño', 'Saltapared Sabanero',
             'Cucarachero Cabecigrís', 'Cucarachero Jaspeado','Cucarachero Bigotudo Montano']

    uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])
    model = cargar_modelo()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, "../base_datos/base_datos.xlsx")
    imagenes_base = os.path.join(base_dir, "../base_datos/imagenes_aves")
    df = pd.read_excel(excel_path)

    if uploaded_file is not None and model:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        st.session_state.imagen_original = image
        st.session_state.nombre_archivo_original = uploaded_file.name 
        image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        x = preprocess_input(np.expand_dims(image_resized, axis=0))

        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="📷 Imagen cargada", width=224)
        st.info("🔍 Realizando predicción...")

        try:
            preds = model.predict(x)
            top_indices = np.argsort(preds[0])[-3:][::-1]

            st.success("🕊️ **Top 3 predicciones:**")

            predicciones = []

            for rank, idx in enumerate(top_indices, start=1):
                row = df.iloc[idx]
                prob = preds[0][idx] * 100
                nombre_cientifico_url = row['nombre_cientifico'].replace(" ", "+")

                st.markdown(f"""
                    <div style="padding:15px; border-radius:10px; border:1px solid #d3d3d3; margin-bottom:15px;">
                        <h4 style="color:#d3d3d3;">#{rank} - {names[idx]} <span style="color:#d3d3d3;">({prob:.2f}%)</span></h4>
                        <p><strong>🧬 Nombre científico:</strong> <em>{row['nombre_cientifico']}</em></p>
                        <p><strong>🛡️ Estado de conservación:</strong> {row['estado_conservacion']}</p>
                        <p><a href="https://www.google.com/search?q={nombre_cientifico_url}" target="_blank" style="color:#1a73e8; text-decoration:none;">🔍 Buscar en Google</a></p>
                    </div>
                """, unsafe_allow_html=True)

                clase_dir = os.path.join(imagenes_base, f"clase{idx + 1}")
                imagenes = []
                if os.path.exists(clase_dir):
                    imagenes = sorted([
                        f for f in os.listdir(clase_dir)
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                    ])
                    if imagenes:
                        imagenes_mostrar = imagenes[:3]
                        cols = st.columns(len(imagenes_mostrar))
                        for col, nombre_imagen in zip(cols, imagenes_mostrar):
                            img_path = os.path.join(clase_dir, nombre_imagen)
                            col.image(Image.open(img_path).copy(), use_container_width=True, caption=nombre_imagen)
                    else:
                        st.warning("⚠️ No hay imágenes disponibles para esta clase.")
                else:
                    st.warning("⚠️ No se encontró la carpeta de imágenes.")

                predicciones.append({
                    "idx": idx,
                    "nombre": names[idx],
                    "nombre_cientifico": row["nombre_cientifico"],
                    "estado_conservacion": row["estado_conservacion"],
                    "imagenes": [
                        os.path.join(clase_dir, img) for img in imagenes[:3]
                    ] if os.path.exists(clase_dir) else []
                })

                st.markdown("---")

            st.session_state.predicciones = predicciones

            st.session_state.opcion_seleccionada = None
            st.session_state.coordenadas = None
            st.session_state.prediccion_registrada = None

            if st.button("✅ Registrar predicción", use_container_width=True):
                st.session_state.section = "RegistroPrediccion"
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error al predecir: {e}")
