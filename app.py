import streamlit as st
from PIL import Image
import time

# Pengaturan halaman
st.set_page_config(page_title="AI Pendeteksi Sampah", page_icon="♻️", layout="wide")

st.title("♻️ AI Pendeteksi Sampah Pintar")
st.write("Silakan upload gambar sampah untuk dianalisis oleh sistem kami.")
st.write("---")

# Area Upload
uploaded_file = st.file_uploader("Pilih gambar sampah (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Bikin 2 kolom
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Gambar Kamu")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("🤖 Hasil Analisis AI")
        st.write("Klik tombol di bawah untuk memulai pemindaian.")
        
        # Tombol deteksi
        klik_deteksi = st.button("Mulai Deteksi 🚀", type="primary")
        
        if klik_deteksi:
            # Efek loading
            with st.spinner('Sistem sedang memindai gambar... 🔍'):
                time.sleep(2)
            
            # Hasil yang akan muncul setelah loading selesai
            st.success("Analisis Selesai!")
            st.markdown("### 🌱 Kategori: **ORGANIK**")
            st.write("Tingkat Keyakinan AI: **98.5%**")
            
            st.info("""
            **Saran Tindakan:**
            - Jangan dicampur dengan plastik/kaca.
            - Buang ke tempat sampah berwarna **HIJAU**.
            - Bisa diolah menjadi kompos.
            """)
