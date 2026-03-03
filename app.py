import streamlit as st
from PIL import Image, ImageDraw
import time
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN (Wajib Paling Atas)
# ==========================================
st.set_page_config(
    page_title="Portal HSSE",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed" # Sembunyikan sidebar di awal
)

# ==========================================
# 2. DATABASE AKUN & SESSION STATE
# ==========================================
USERS = {
    "admin": {"password": "123", "role": "Admin", "nama": "Komandan HSSE"},
    "warga": {"password": "abc", "role": "Warga", "nama": "Karyawan Lapangan"}
}

# Menyimpan status login
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'role' not in st.session_state: st.session_state.role = ""
if 'nama' not in st.session_state: st.session_state.nama = ""

# Menyimpan data tabel
if 'data_insiden' not in st.session_state:
    st.session_state.data_insiden = pd.DataFrame(columns=["Waktu", "Pelapor", "Lokasi", "Kategori", "Deskripsi", "Status"])
if 'data_limbah' not in st.session_state:
    st.session_state.data_limbah = pd.DataFrame(columns=["Waktu Input", "Petugas", "Organik (kg)", "Anorganik (kg)", "B3 (kg)"])

# ==========================================
# 3. HALAMAN LOGIN (MUNCUL DI AWAL SAJA)
# ==========================================
if not st.session_state.logged_in:
    # Membuat jarak kosong dari atas agar kotak login ada di tengah layar
    st.write("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>🔐 Portal Keamanan HSSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sistem Manajemen Limbah & Keselamatan Terpadu</p>", unsafe_allow_html=True)
    
    # Membagi layar jadi 3 kolom agar form login ada di tengah (tidak terlalu lebar)
    col_kiri, col_tengah, col_kanan = st.columns([1, 1.5, 1])
    
    with col_tengah:
        st.write("---")
        with st.form("form_login"):
            input_user = st.text_input("👤 Username", placeholder="Ketik: admin / warga")
            input_pass = st.text_input("🔑 Password", type="password", placeholder="Ketik: 123 / abc")
            
            st.write("") # Spasi
            tombol_login = st.form_submit_button("Masuk ke Sistem 🚀", use_container_width=True)
            
            if tombol_login:
                if input_user in USERS and USERS[input_user]["password"]
