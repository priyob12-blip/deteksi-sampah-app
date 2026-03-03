import streamlit as st
from PIL import Image, ImageDraw
import time
import pandas as pd
import numpy as np
from datetime import datetime

# Konfigurasi Halaman 
st.set_page_config(
    page_title="HSSE Waste System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIMULASI DATABASE (SESSION STATE) ---
# Ini agar data form yang dikirim benar-benar tersimpan selama web dibuka
if 'data_insiden' not in st.session_state:
    st.session_state.data_insiden = pd.DataFrame(columns=["Waktu", "Lokasi", "Kategori", "Deskripsi", "Status"])

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ HSSE Command Center")
    st.write("Sistem terintegrasi untuk mendeteksi limbah, memantau lingkungan, dan melaporkan bahaya.")
    st.info("Kategori AI:\n- 🌱 **Organik**\n- 🧴 **Anorganik**")
    st.write("---")
    st.write("© 2026 - Divisi HSSE & Keberlanjutan 🌍")

# --- HEADER UTAMA ---
st.title("♻️ Sistem Manajemen Limbah & Keselamatan (HSSE)")
st.write("Gunakan menu tab di bawah untuk bernavigasi antar fitur.")

# --- MEMBUAT 3 TAB ---
tab1, tab2, tab3 = st.tabs(["🔍 Deteksi AI", "📊 Dasbor Lingkungan", "⚠️ Lapor Insiden & SOP"])

# ==========================================
# TAB 1: DETEKSI AI
# ==========================================
with tab1:
    st.markdown("### 📷 Pemindai Limbah Cerdas")
    st.write("Unggah foto sampah/limbah yang ditemukan di area kerja.")
    st.caption("Catatan: Mode deteksi saat ini menggunakan kotak simulasi hingga model Machine Learning (AI) sesungguhnya diintegrasikan.")
    
    uploaded_file = st.file_uploader("Pilih gambar sampah (Format: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Laporan")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("🤖 Hasil Analisis AI")
            
            if st.button("Mulai Deteksi 🚀", type="primary", use_container_width=True):
                with st.spinner('AI sedang memindai potensi bahaya dan jenis limbah... 🔍'):
                    time.sleep(2) 
                
                st.success("Analisis Selesai!")
                
                # Bounding Box (Kotak Simulasi)
                annotated_image = image.copy()
                draw = ImageDraw.Draw(annotated_image)
                img_width, img_height = annotated_image.size
                
                kotak_organik = [img_width*0.1, img_height*0.2, img_width*0.4, img_height*0.4]
                draw.rectangle(kotak_organik, outline="#28a745", width=5)
                
                kotak_anorganik = [img_width*0.45, img_height*0.5, img_width*0.8, img_height*0.8]
                draw.rectangle(kotak_anorganik, outline="#dc3545", width=5)
                
                st.image(annotated_image, use_container_width=True, caption="Deteksi Objek (Hijau: Organik, Merah: Anorganik)")

                # Hasil Objek
                st.markdown("""
                    <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid
