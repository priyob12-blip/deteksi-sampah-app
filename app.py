import streamlit as st
from PIL import Image
import time

# Konfigurasi Halaman (Harus selalu di baris paling atas setelah import)
st.set_page_config(
    page_title="AI Pendeteksi Sampah",
    page_icon="♻️",
    layout="wide", # Membuat tampilan web melebar dan modern
    initial_sidebar_state="expanded"
)

# --- SIDEBAR (Menu Samping) ---
with st.sidebar:
    st.title("💡 Info Aplikasi")
    st.write("Aplikasi ini menggunakan simulasi teknologi *Computer Vision* untuk membedakan jenis sampah.")
    st.info("Kategori yang didukung:\n- 🌱 **Organik** (Sisa makanan, daun)\n- 🧴 **Anorganik** (Plastik, kaleng, kaca)")
    st.write("---")
    st.write("© 2026 - Dibuat untuk bumi yang lebih bersih. 🌍")

# --- HEADER UTAMA ---
st.title("♻️ AI Pendeteksi Sampah Pintar")
st.markdown("Mari jaga lingkungan dengan memilah sampah dengan benar. **Unggah foto sampahmu di bawah ini!** ⬇️")
st.write("---")

# --- AREA UPLOAD ---
uploaded_file = st.file_uploader("Pilih gambar sampah (Format: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# --- AREA HASIL ---
if uploaded_file is not None:
    # Membagi layar menjadi 2 kolom: Kiri untuk gambar, Kanan untuk hasil
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Gambar Kamu")
        image = Image.open(uploaded_file)
        # Menampilkan gambar dengan sudut melengkung (bawaan Streamlit)
        st.image(image, use_container_width=True, caption="Gambar siap dianalisis")

    with col2:
        st.subheader("🤖 Hasil Analisis AI")
        
        # Tombol deteksi dengan
