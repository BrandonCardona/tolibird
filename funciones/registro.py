import streamlit as st
from PIL import Image
from streamlit_folium import st_folium
import folium
import pandas as pd
from datetime import datetime
import os
import cv2

def registrar_prediccion():
    st.title("✅ Registrar predicción")

    if "predicciones" not in st.session_state:
        st.warning("No hay predicciones para registrar.")
        return

    opciones = st.session_state.predicciones

    st.subheader("Seleccione la especie correcta haciendo clic en el botón Seleccionar:")

    if "opcion_seleccionada" not in st.session_state:
        st.session_state.opcion_seleccionada = None

    cols = st.columns(3)

    for i, (col, opcion) in enumerate(zip(cols, opciones)):
        with col:
            st.image(Image.open(opcion["imagenes"][0]), use_container_width=True)
            st.markdown(f"<div style='text-align:center; font-weight:bold'>{opcion['nombre']}</div>", unsafe_allow_html=True)

            if st.session_state.opcion_seleccionada == i:
                st.markdown(
                    "<div style='text-align:center; color:green; font-weight:bold;'>✔ Seleccionado</div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button("Seleccionar", key=f"select_btn_{i}"):
                    st.session_state.opcion_seleccionada = i
                    st.rerun()

    if st.session_state.opcion_seleccionada is not None:
        seleccionada = opciones[st.session_state.opcion_seleccionada]
        st.markdown("---")
        st.success(f"Has seleccionado: {seleccionada['nombre']}")
        st.markdown(f"**🧬 Nombre científico:** *{seleccionada['nombre_cientifico']}*")
        st.markdown(f"**🛡️ Estado de conservación:** {seleccionada['estado_conservacion']}")
        st.session_state.prediccion_registrada = seleccionada

        st.markdown("---")
        st.subheader("📍 Selecciona la ubicación en el mapa")

        m = folium.Map(location=[4.5709, -74.2973], zoom_start=6)
        m.add_child(folium.LatLngPopup())
        map_data = st_folium(m, width=1000, height=500)

        if map_data and "last_clicked" in map_data and map_data["last_clicked"] is not None:
            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]
            st.success(f"Coordenadas seleccionadas: ({lat:.5f}, {lon:.5f})")
            st.session_state.coordenadas = {"lat": lat, "lon": lon}

        if "coordenadas" in st.session_state and st.session_state.coordenadas:
            st.markdown("---")
            if st.button("💾 Guardar Registro", use_container_width=True):
                try:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    excel_path = os.path.join(base_dir, "../base_datos/aves_registradas.xlsx")

                    if os.path.exists(excel_path):
                        df = pd.read_excel(excel_path)
                    else:
                        df = pd.DataFrame(columns=[
                            "id", "nombre_comun", "nombre_cientifico", "estado_conservacion",
                            "Latitud", "Longitud", "Fecha", "Hora", "Imagen"
                        ])

                    if df.empty or "id" not in df.columns:
                        nuevo_id = 1
                    else:
                        nuevo_id = int(df["id"].max()) + 1

                    now = datetime.now()
                    fecha = now.strftime("%Y-%m-%d")
                    hora = now.strftime("%H:%M:%S")

                    imagenes_dir = os.path.join(base_dir, "../base_datos/imagenes_registros")
                    os.makedirs(imagenes_dir, exist_ok=True)

                    nombre_comun = seleccionada["nombre"].replace(" ", "_")
                    timestamp = now.strftime("%Y%m%d_%H%M%S")
                    nombre_archivo = f"{nuevo_id}_{nombre_comun}_{timestamp}.jpg"
                    ruta_archivo = os.path.join(imagenes_dir, nombre_archivo)

                    if "imagen_original" in st.session_state:
                        imagen_bgr = st.session_state.imagen_original
                        imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
                        imagen_pil = Image.fromarray(imagen_rgb)
                        imagen_pil.save(ruta_archivo)
                        ruta_excel = f"imagenes_registros/{nombre_archivo}"
                    else:
                        ruta_excel = ""

                    nueva_fila = {
                        "id": nuevo_id,
                        "nombre_comun": seleccionada["nombre"],
                        "nombre_cientifico": seleccionada["nombre_cientifico"],
                        "estado_conservacion": seleccionada["estado_conservacion"],
                        "Latitud": st.session_state.coordenadas["lat"],
                        "Longitud": st.session_state.coordenadas["lon"],
                        "Fecha": fecha,
                        "Hora": hora,
                        "Imagen": ruta_excel
                    }

                    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                    df.to_excel(excel_path, index=False)

                    st.success("✅ Registro guardado exitosamente.")

                    st.session_state.opcion_seleccionada = None
                    st.session_state.coordenadas = None
                    st.session_state.prediccion_registrada = None
                    st.session_state.imagen_original = None

                except Exception as e:
                    st.error(f"❌ Error al guardar el registro: {e}")
