import streamlit as st
from PIL import Image

st.set_page_config(page_title="Deteksi Sampah AI", page_icon="♻️")
st.title("♻️ Aplikasi Pendeteksi Sampah")
st.write("Silakan upload gambar sampah, dan sistem akan mendeteksi apakah itu **Organik** atau **Anorganik**.")

uploaded_file = st.file_uploader("Upload gambar (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_container_width=True)

    if st.button("Deteksi Sekarang"):
        st.info("Sedang memproses gambar... 🔍")
        st.success("Hasil Deteksi: **Organik** 🌱 (Ini masih simulasi)")
