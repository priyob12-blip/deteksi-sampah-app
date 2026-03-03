import streamlit as st
from PIL import Image, ImageDraw
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
        
        # Tombol deteksi dengan warna utama (primary) agar mencolok
        if st.button("Mulai Deteksi 🚀", type="primary", use_container_width=True):
            
            # Efek loading muter-muter biar kerasa "AI" banget
            with st.spinner('AI sedang memindai pola gambar... 🔍'):
                time.sleep(2) # Simulasi waktu proses 2 detik
            
            st.success("Analisis Selesai!")
            
            # --- MULAI SIMULASI BOUNDING BOX (KOTAK) ---
            annotated_image = image.copy()
            draw = ImageDraw.Draw(annotated_image)
            img_width, img_height = annotated_image.size
            
            # Gambar Kotak 1: Daun (Organik) - Warna Hijau
            # Koordinat [x1, y1, x2, y2] disimulasikan sesuai proporsi gambar
            kotak_organik = [img_width*0.1, img_height*0.2, img_width*0.4, img_height*0.4]
            draw.rectangle(kotak_organik, outline="#28a745", width=5)
            
            # Gambar Kotak 2: Plastik (Anorganik) - Warna Merah
            kotak_anorganik = [img_width*0.45, img_height*0.5, img_width*0.8, img_height*0.8]
            draw.rectangle(kotak_anorganik, outline="#dc3545", width=5)
            
            # Tampilkan gambar yang sudah "dikotakin"
            st.image(annotated_image, use_container_width=True, caption="Deteksi Objek (Kotak Hijau: Organik, Kotak Merah: Anorganik)")
            # --- SELESAI SIMULASI BOUNDING BOX ---

            st.write("🔍 **Ditemukan beberapa objek dalam gambar:**")
            
            # Objek 1: Organik (Misalnya Daun Kering)
            st.markdown("""
                <div style='background-color: #d4edda; padding: 15px; border-radius: 8px; border-left: 5px solid #28a745; margin-bottom: 10px;'>
                    <h4 style='color: #155724; margin:0;'>🌱 Daun Kering (ORGANIK)</h4>
                    <p style='color: #155724; margin:0;'>Tingkat Keyakinan AI: <strong>96.2%</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Objek 2: Anorganik (Misalnya Bungkus Plastik)
            st.markdown("""
                <div style='background-color: #f8d7da; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545; margin-bottom: 15px;'>
                    <h4 style='color: #721c24; margin:0;'>🧴 Bungkus Plastik (ANORGANIK)</h4>
                    <p style='color: #721c24; margin:0;'>Tingkat Keyakinan AI: <strong>92.8%</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Dropdown saran tindakan disesuaikan untuk banyak barang
            with st.expander("💡 Apa yang harus dilakukan dengan sampah-sampah ini?"):
                st.write("""
                Karena terdapat sampah campuran dalam satu foto, pastikan kamu memisahkannya terlebih dahulu:
                1. **Daun Kering:** Pisahkan dan buang ke tempat sampah **HIJAU** (Organik) agar bisa diolah menjadi kompos.
                2. **Bungkus Plastik:** Buang ke tempat sampah **KUNING** (Anorganik) untuk nantinya didaur ulang.
                """)
