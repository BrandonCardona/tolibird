import streamlit as st
from keras.models import load_model
import os
import gdown

@st.cache_resource
def cargar_modelo():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model_VGG16_v2_os.keras")

    file_id = "1H8SWLSj4C8ubdRw2PMs4I_GRbswGfEAh"
    url = f"https://drive.google.com/uc?id={file_id}"

    if not os.path.exists(model_path):
        try:
            gdown.download(url, model_path, quiet=False)
        except Exception as e:
            st.error(f"❌ Error al descargar el modelo: {e}")
            return None

    try:
        return load_model(model_path)
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {e}")
        return None

modelo = cargar_modelo()
if modelo is None:
    st.stop()