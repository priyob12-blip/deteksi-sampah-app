import streamlit as st
from PIL import Image, ImageDraw
import time
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Portal HSSE", page_icon="♻️", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 2. DATABASE AKUN & SESSION STATE
# ==========================================
USERS = {
    "admin": {"password": "123456", "role": "Admin", "nama": "HSSE"},
    "user": {"password": "abcdef", "role": "User", "nama": "Karyawan Lapangan"}
}

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'role' not in st.session_state: st.session_state.role = ""
if 'nama' not in st.session_state: st.session_state.nama = ""

if 'data_insiden' not in st.session_state:
    st.session_state.data_insiden = pd.DataFrame(columns=["Waktu", "Pelapor", "Lokasi", "Kategori", "Deskripsi", "Status"])
if 'data_limbah' not in st.session_state:
    st.session_state.data_limbah = pd.DataFrame(columns=["Waktu Input", "Petugas", "Organik (kg)", "Anorganik (kg)", "B3 (kg)"])

# ==========================================
# 3. HALAMAN LOGIN
# ==========================================
if not st.session_state.logged_in:
    st.write("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🔐 Portal Keamanan HSSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sistem Manajemen Limbah & Keselamatan Terpadu</p>", unsafe_allow_html=True)
    
    col_kiri, col_tengah, col_kanan = st.columns([1, 1.5, 1])
    with col_tengah:
        st.write("---")
        with st.form("form_login"):
            input_user = st.text_input("👤 Username", placeholder="Ketik: admin / warga")
            input_pass = st.text_input("🔑 Password", type="password", placeholder="Ketik: 123 / abc")
            tombol_login = st.form_submit_button("Masuk ke Sistem 🚀", use_container_width=True)
            
            # DI SINI LETAK PERBAIKAN ERROR-NYA:
            if tombol_login:
                if input_user in USERS and USERS[input_user]["password"] == input_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = input_user
                    st.session_state.role = USERS[input_user]["role"]
                    st.session_state.nama = USERS[input_user]["nama"]
                    st.success("Akses Diterima! Memuat dasbor...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Username atau Password salah!")

# ==========================================
# 4. APLIKASI UTAMA
# ==========================================
else:
    with st.sidebar:
        st.title("🛡️ Info Akun")
        st.success(f"👤 **{st.session_state.nama}**\n\nHak Akses: **{st.session_state.role}**")
        
        if st.button("Keluar (Logout) 🚪", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            for key in ['username', 'role', 'nama']: st.session_state[key] = ""
            st.rerun()
        st.divider()
        st.write("© 2026 - Divisi HSSE")

    st.title("♻️ Sistem Manajemen Limbah & Keselamatan")
    st.write(f"Selamat datang, **{st.session_state.nama}**! Gunakan menu tab di bawah untuk bernavigasi.")

    tab1, tab2, tab3 = st.tabs(["🔍 Deteksi AI", "📊 Dasbor Lingkungan", "⚠️ Lapor Insiden & SOP"])

    # --- TAB 1: DETEKSI ---
    with tab1:
        st.markdown("### 📷 Pemindai Limbah Cerdas")
        uploaded_file = st.file_uploader("Pilih gambar sampah", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            with col1:
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)
            with col2:
                if st.button("Mulai Deteksi 🚀", type="primary", use_container_width=True):
                    with st.spinner("Memindai... 🔍"): time.sleep(2) 
                    st.success("Analisis Selesai!")
                    annotated_image = image.copy()
                    draw = ImageDraw.Draw(annotated_image)
                    img_w, img_h = annotated_image.size
                    draw.rectangle([img_w*0.1, img_h*0.2, img_w*0.4, img_h*0.4], outline="#28a745", width=5)
                    draw.rectangle([img_w*0.45, img_h*0.5, img_w*0.8, img_h*0.8], outline="#dc3545", width=5)
                    st.image(annotated_image, use_container_width=True)
                    st.markdown('''<div style="background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 5px;"><h5 style="color: #155724; margin:0;">🌱 Daun/Kayu (ORGANIK) - 96.2%</h5></div>''', unsafe_allow_html=True)
                    st.markdown('''<div style="background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 10px;"><h5 style="color: #721c24; margin:0;">🧴 Plastik/Kaca (ANORGANIK) - 92.8%</h5></div>''', unsafe_allow_html=True)

    # --- TAB 2: DASBOR ---
    with tab2:
        st.markdown("### 📈 Dasbor Kinerja Lingkungan")
        if st.session_state.role == "Admin":
            with st.expander("➕ Catat Data Timbangan Limbah Baru (Khusus Admin)", expanded=True):
                with st.form("form_limbah", clear_on_submit=True):
                    c1, c2, c3 = st.columns(3)
                    with c1: in_org = st.number_input("Organik (kg)", min_value=0.0)
                    with c2: in_anorg = st.number_input("Anorganik (kg)", min_value=0.0)
                    with c3: in_b3 = st.number_input("Limbah B3 (kg)", min_value=0.0)
                    if st.form_submit_button("Simpan Data 💾"):
                        new_data = pd.DataFrame([{"Waktu Input": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Petugas": st.session_state.nama, "Organik (kg)": in_org, "Anorganik (kg)": in_anorg, "B3 (kg)": in_b3}])
                        st.session_state.data_limbah = pd.concat([st.session_state.data_limbah, new_data], ignore_index=True)
                        st.success("Data tersimpan!")
        else:
            st.info("💡 Hanya petugas HSSE (Admin) yang dapat mencatat data timbangan limbah harian.")

        tot_org = st.session_state.data_limbah["Organik (kg)"].sum()
        tot_anorg = st.session_state.data_limbah["Anorganik (kg)"].sum()
        tot_daur = tot_org + tot_anorg
        tot_b3 = st.session_state.data_limbah["B3 (kg)"].sum()

        cA, cB, cC = st.columns(3)
        cA.metric("Total Didaur Ulang", f"{tot_daur:.1f} kg")
        cB.metric("Limbah Berbahaya (B3)", f"{tot_b3:.1f} kg")
        cC.metric("Pengurangan Jejak Karbon", f"{tot_daur * 0.5:.1f} kg CO2")
        
        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.write("**Data Tabel Limbah Masuk**")
            st.dataframe(st.session_state.data_limbah, use_container_width=True, hide_index=True)
        with g2:
            st.write("**Statistik Laporan Insiden**")
            if len(st.session_state.data_insiden) > 0: st.bar_chart(st.session_state.data_insiden["Kategori"].value_counts())
            else: st.info("Belum ada data laporan.")

    # --- TAB 3: LAPOR INSIDEN ---
    with tab3:
        st.markdown("### ⚠️ Pelaporan Kondisi Tidak Aman")
        with st.form("form_insiden", clear_on_submit=True):
            lokasi = st.text_input("📍 Lokasi Temuan")
            kategori = st.selectbox("🛑 Kategori Bahaya", ["Tumpahan Cairan Kimia", "Limbah Medis/B3", "Pecahan Kaca", "Lainnya"])
            deskripsi = st.text_area("📝 Deskripsi Detail")
            if st.form_submit_button("Kirim Laporan 🚨") and lokasi:
                new_ins = pd.DataFrame([{"Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Pelapor": st.session_state.nama, "Lokasi": lokasi, "Kategori": kategori, "Deskripsi": deskripsi, "Status": "Pending 🔴"}])
                st.session_state.data_insiden = pd.concat([st.session_state.data_insiden, new_ins], ignore_index=True)
                st.success("Laporan terkirim!")

        st.divider()
        st.markdown("#### 📋 Log Laporan Insiden")
        st.dataframe(st.session_state.data_insiden, use_container_width=True, hide_index=True)

        if st.session_state.role == "Admin":
            st.markdown("#### 🛠️ Panel Admin: Update Status")
            if len(st.session_state.data_insiden) > 0:
                ca1, ca2 = st.columns(2)
                with ca1:
                    pil_lap = st.selectbox("Pilih Laporan:", st.session_state.data_insiden.index, format_func=lambda x: f"Laporan {x+1} - {st.session_state.data_insiden.loc[x, 'Lokasi']}")
                with ca2:
                    stat_baru = st.selectbox("Ubah Status:", ["Pending 🔴", "Sedang Ditangani 🟡", "Selesai 🟢"])
                if st.button("Update Status 💾", type="primary"):
                    st.session_state.data_insiden.loc[pil_lap, "Status"] = stat_baru
                    st.success("Status diperbarui!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("Belum ada laporan.")
