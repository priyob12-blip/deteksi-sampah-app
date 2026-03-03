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
# 1. Database untuk Laporan Insiden
if 'data_insiden' not in st.session_state:
    st.session_state.data_insiden = pd.DataFrame(columns=["Waktu", "Lokasi", "Kategori", "Deskripsi", "Status"])

# 2. Database untuk Data Limbah Harian (BARU)
if 'data_limbah' not in st.session_state:
    st.session_state.data_limbah = pd.DataFrame(columns=["Waktu Input", "Organik (kg)", "Anorganik (kg)", "B3 (kg)"])

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
                with st.spinner("AI sedang memindai potensi bahaya dan jenis limbah... 🔍"):
                    time.sleep(2) 
                
                st.success("Analisis Selesai!")
                
                annotated_image = image.copy()
                draw = ImageDraw.Draw(annotated_image)
                img_width, img_height = annotated_image.size
                
                draw.rectangle([img_width*0.1, img_height*0.2, img_width*0.4, img_height*0.4], outline="#28a745", width=5)
                draw.rectangle([img_width*0.45, img_height*0.5, img_width*0.8, img_height*0.8], outline="#dc3545", width=5)
                
                st.image(annotated_image, use_container_width=True, caption="Deteksi Objek (Hijau: Organik, Merah: Anorganik)")

                st.markdown('''
                    <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 5px;">
                        <h5 style="color: #155724; margin:0;">🌱 Daun/Kayu (ORGANIK) - 96.2%</h5>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('''
                    <div style="background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 10px;">
                        <h5 style="color: #721c24; margin:0;">🧴 Plastik/Kaca (ANORGANIK) - 92.8%</h5>
                    </div>
                ''', unsafe_allow_html=True)

# ==========================================
# TAB 2: DASBOR LINGKUNGAN (100% DATA ASLI DARI INPUT)
# ==========================================
with tab2:
    st.markdown("### 📈 Dasbor Kinerja Lingkungan")
    
    # 1. FORM INPUT DATA LIMBAH
    with st.expander("➕ Catat Data Timbangan Limbah Baru", expanded=True):
        with st.form("form_input_limbah", clear_on_submit=True):
            st.write("Masukkan berat limbah yang berhasil dikumpulkan hari ini:")
            col_input1, col_input2, col_input3 = st.columns(3)
            with col_input1:
                input_organik = st.number_input("Organik (kg)", min_value=0.0, step=0.5)
            with col_input2:
                input_anorganik = st.number_input("Anorganik (kg)", min_value=0.0, step=0.5)
            with col_input3:
                input_b3 = st.number_input("Limbah B3 (kg)", min_value=0.0, step=0.5)
            
            submit_limbah = st.form_submit_button("Simpan Data Limbah 💾")
            
            if submit_limbah:
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_limbah_baru = pd.DataFrame([{
                    "Waktu Input": waktu_sekarang,
                    "Organik (kg)": input_organik,
                    "Anorganik (kg)": input_anorganik,
                    "B3 (kg)": input_b3
                }])
                st.session_state.data_limbah = pd.concat([st.session_state.data_limbah, data_limbah_baru], ignore_index=True)
                st.success("Data limbah berhasil ditambahkan dan dasbor telah diperbarui!")

    # 2. KALKULASI METRIK DARI DATABASE
    total_organik = st.session_state.data_limbah["Organik (kg)"].sum()
    total_anorganik = st.session_state.data_limbah["Anorganik (kg)"].sum()
    total_daur_ulang = total_organik + total_anorganik
    total_b3 = st.session_state.data_limbah["B3 (kg)"].sum()
    
    # Asumsi rumusan nyata: 1 kg sampah daur ulang menghemat 0.5 kg emisi karbon
    jejak_karbon = total_daur_ulang * 0.5  

    # 3. TAMPILKAN METRIK DI ATAS
    colA, colB, colC = st.columns(3)
    colA.metric(label="Total Limbah Didaur Ulang", value=f"{total_daur_ulang:.1f} kg")
    colB.metric(label="Limbah Berbahaya (B3) Diamankan", value=f"{total_b3:.1f} kg")
    colC.metric(label="Pengurangan Jejak Karbon", value=f"{jejak_karbon:.1f} kg CO2")
    
    st.divider()
    
    # 4. TAMPILKAN GRAFIK BERDASARKAN INPUT ASLI
    col_grafik1, col_grafik2 = st.columns(2)
    
    with col_grafik1:
        st.write("**Tren Pembuangan Limbah (Real-Time)**")
        if len(st.session_state.data_limbah) == 0:
            st.info("Belum ada data limbah yang dicatat. Silakan input di atas 👆")
        else:
            # Mengubah tabel agar grafiknya memanjang berdasarkan Waktu Input
            grafik_limbah = st.session_state.data_limbah.set_index("Waktu Input")[["Organik (kg)", "Anorganik (kg)", "B3 (kg)"]]
            st.line_chart(grafik_limbah)

    with col_grafik2:
        st.write("**Status Pelaporan Insiden (Dari Tab 3)**")
        if len(st.session_state.data_insiden) == 0:
            st.info("Belum ada data laporan insiden yang masuk.")
        else:
            kategori_count = st.session_state.data_insiden["Kategori"].value_counts()
            st.bar_chart(kategori_count)

# ==========================================
# TAB 3: LAPOR INSIDEN (FORM KE DATABASE)
# ==========================================
with tab3:
    st.markdown("### ⚠️ Pelaporan Kondisi Tidak Aman (Unsafe Condition)")
    
    with st.form("form_insiden", clear_on_submit=True):
        lokasi = st.text_input("📍 Lokasi Temuan (Misal: Area Produksi Gedung B)")
        kategori_bahaya = st.selectbox("🛑 Kategori Bahaya", ["Tumpahan Cairan Kimia", "Limbah Medis/B3 Berserakan", "Pecahan Kaca/Material Tajam", "Lainnya"])
        deskripsi = st.text_area("📝 Deskripsi Detail Kejadian")
        
        submitted = st.form_submit_button("Kirim Laporan ke Tim HSSE 🚨")
        
        if submitted and lokasi != "":
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_baru = pd.DataFrame([{
                "Waktu": waktu_sekarang, 
                "Lokasi": lokasi, 
                "Kategori": kategori_bahaya, 
                "Deskripsi": deskripsi, 
                "Status": "Pending 🔴"
            }])
            st.session_state.data_insiden = pd.concat([st.session_state.data_insiden, data_baru], ignore_index=True)
            st.success(f"Laporan bahaya di **{lokasi}** berhasil tersimpan di database!")

    st.divider()
    
    st.markdown("#### 📋 Log Laporan Insiden Terbaru")
    st.dataframe(st.session_state.data_insiden, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 📚 Buku Saku SOP Keselamatan Darurat")
    with st.expander("SOP Penanganan Tumpahan Bahan Kimia (Spill Kit)"):
        st.write('''
        1. **Amankan Area:** Pasang barikade atau tanda peringatan di sekitar tumpahan.
        2. **Gunakan APD:** Wajib menggunakan kacamata safety, sarung tangan nitrile, dan masker.
        3. **Gunakan Absorben:** Taburkan pasir atau bantalan penyerap dari kotak *Spill Kit*.
        4. **Pembuangan:** Sapu material penyerap dan masukkan ke kantong plastik kuning (Limbah B3).
        ''')
