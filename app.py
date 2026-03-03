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
# TAB 2: DASBOR LINGKUNGAN (DATA REAL & GRAFIK)
# ==========================================
with tab2:
    st.markdown("### 📈 Dasbor Kinerja Lingkungan")
    
    colA, colB, colC = st.columns(3)
    colA.metric(label="Total Limbah Didaur Ulang", value="1,245 kg", delta="12% dari bulan lalu")
    colB.metric(label="Limbah Berbahaya (B3) Diamankan", value="34 kg", delta="-5% dari bulan lalu", delta_color="inverse")
    colC.metric(label="Pengurangan Jejak Karbon", value="450 kg CO2", delta="8% dari bulan lalu")
    
    st.divider()
    
    col_grafik1, col_grafik2 = st.columns(2)
    
    with col_grafik1:
        st.write("**Tren Pembuangan Limbah 7 Hari Terakhir (Kg)**")
        chart_data = pd.DataFrame(
            np.random.randint(10, 50, size=(7, 2)),
            columns=["Organik", "Anorganik"],
            index=(pd.date_range(end=datetime.today(), periods=7)).strftime("%d %b")
        )
        st.line_chart(chart_data)

    with col_grafik2:
        st.write("**Status Pelaporan Insiden (Real-Time)**")
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
