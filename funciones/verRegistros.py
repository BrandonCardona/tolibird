import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import os

def mostrar_registros_guardados():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, "../base_datos/aves_registradas.xlsx")
    imagenes_dir = os.path.join(base_dir, "../base_datos/imagenes_registros")

    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo de registros.")
        return
    except Exception as e:
        st.error(f"⚠️ Error al leer el archivo: {e}")
        return

    if df.empty:
        st.warning("No hay registros guardados.")
        return

    st.title("📍 Aves Registradas")

    mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df.iterrows():
        popup_info = f"""
        <b>{row['id']} - {row['nombre_comun']}</b><br>
        <i>{row['nombre_cientifico']}</i><br>
        Estado: {row['estado_conservacion']}<br>
        Fecha: {row['Fecha']}<br>
        Hora: {row['Hora']}
        """
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            popup=popup_info,
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(marker_cluster)

    st_folium(mapa, width=1000, height=500)

    st.subheader("📄 Registros Guardados")

    header_cols = st.columns([1, 2, 2, 2, 1.5, 1.5, 1.5, 1.5, 3])
    header_cols[0].markdown("**ID**")
    header_cols[1].markdown("**Nombre Común**")
    header_cols[2].markdown("**Nombre Científico**")
    header_cols[3].markdown("**Estado de Conservación**")
    header_cols[4].markdown("**Latitud**")
    header_cols[5].markdown("**Longitud**")
    header_cols[6].markdown("**Fecha**")
    header_cols[7].markdown("**Hora**")
    header_cols[8].markdown("**Imagen**")

    for _, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 1.5, 1.5, 1.5, 1.5, 3])
        cols[0].markdown(f"{row['id']}")
        cols[1].markdown(row['nombre_comun'])
        cols[2].markdown(row['nombre_cientifico'])
        cols[3].markdown(row['estado_conservacion'])
        cols[4].markdown(str(row['Latitud']))
        cols[5].markdown(str(row['Longitud']))
        cols[6].markdown(str(row['Fecha']))
        cols[7].markdown(str(row['Hora']))

        image_path = os.path.join(imagenes_dir, os.path.basename(row['Imagen']))
        if os.path.exists(image_path):
            cols[8].image(image_path, width=250)
        else:
            cols[8].markdown("*Imagen no encontrada*")
