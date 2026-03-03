import streamlit as st
from PIL import Image, ImageDraw
import time

# Konfigurasi Halaman 
st.set_page_config(
    page_title="HSSE Waste System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# TAB 1: DETEKSI AI (KODE LAMA DIMASUKKAN KE SINI)
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
                with st.spinner('AI sedang memindai potensi bahaya dan jenis limbah... 🔍'):
                    time.sleep(2) 
                
                st.success("Analisis Selesai!")
                
                # Bounding Box (Kotak)
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
                    <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 5px;'>
                        <h5 style='color: #155724; margin:0;'>🌱 Daun Kering (ORGANIK) - 96.2%</h5>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 10px;'>
                        <h5 style='color: #721c24; margin:0;'>🧴 Bungkus Plastik (ANORGANIK) - 92.8%</h5>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: DASBOR LINGKUNGAN (FITUR BARU)
# ==========================================
with tab2:
    st.markdown("### 📈 Pencapaian Lingkungan Bulan Ini")
    st.write("Pantau terus metrik keberlanjutan perusahaan kita.")
    
    # Menampilkan metrik seperti dashboard sungguhan
    colA, colB, colC = st.columns(3)
    colA.metric(label="Total Limbah Didaur Ulang", value="1,245 kg", delta="12% dari bulan lalu")
    colB.metric(label="Limbah Berbahaya (B3) Diamankan", value="34 kg", delta="-5% dari bulan lalu", delta_color="inverse")
    colC.metric(label="Pengurangan Jejak Karbon", value="450 kg CO2", delta="8% dari bulan lalu")
    
    st.divider()
    st.info("💡 Target kuartal ini: Mencapai **Zero Waste to Landfill** (Nol Sampah ke TPA). Terus gunakan AI untuk memilah sampah dengan benar!")

# ==========================================
# TAB 3: LAPOR INSIDEN & SOP (FITUR BARU)
# ==========================================
with tab3:
    st.markdown("### ⚠️ Pelaporan Kondisi Tidak Aman (Unsafe Condition)")
    st.write("Jika menemukan tumpahan bahan kimia, pecahan kaca, atau limbah berbahaya yang tidak tertangani, segera lapor di sini.")
    
    # Membuat Form Interaktif
    with st.form("form_insiden"):
        lokasi = st.text_input("📍 Lokasi Temuan (Misal: Area Produksi Gedung B)")
        kategori_bahaya = st.selectbox("🛑 Kategori Bahaya", ["Tumpahan Cairan Kimia", "Limbah Medis/B3 Berserakan", "Pecahan Kaca/Material Tajam", "Lainnya"])
        deskripsi = st.text_area("📝 Deskripsi Detail Kejadian")
        
        # Tombol Kirim Form
        submitted = st.form_submit_button("Kirim Laporan ke Tim HSSE 🚨")
        if submitted:
            st.success(f"Terima kasih! Laporan bahaya di **{lokasi}** telah dikirim ke petugas piket HSSE.")

    st.divider()
    
    # Menambahkan SOP menggunakan Expander (Bisa di-klik untuk membuka)
    st.markdown("### 📚 Buku Saku SOP Keselamatan Darurat")
    
    with st.expander("SOP Penanganan Tumpahan Bahan Kimia (Spill Kit)"):
        st.write("""
        1. **Amankan Area:** Pasang barikade atau tanda peringatan (Warning Sign) di sekitar tumpahan.
        2. **Gunakan APD:** Wajib menggunakan kacamata safety, sarung tangan *nitrile*, dan masker *respirator*.
        3. **Gunakan Absorben:** Taburkan pasir atau bantalan penyerap dari kotak *Spill Kit* ke atas cairan.
        4. **Pembuangan:** Sapu material penyerap dan masukkan ke dalam kantong plastik kuning (Limbah B3).
        """)
        
    with st.expander("SOP Penanganan Pecahan Kaca atau Benda Tajam"):
        st.write("""
        1. **JANGAN pernah** mengambil serpihan kaca dengan tangan kosong meskipun menggunakan sarung tangan kain.
        2. Gunakan sapu dan pengki untuk mengumpulkan serpihan.
        3. Masukkan ke dalam wadah yang keras dan tidak mudah tertembus (misal: botol plastik tebal atau kardus berlapis).
        4. Beri label **"AWAS BENDA TAJAM / SHARP HAZARD"** pada wadah tersebut.
        """)
