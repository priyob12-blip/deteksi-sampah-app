import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="BundSafe Tank Analytics", 
    page_icon="⚡", 
    layout="wide"
)

# --- CUSTOM CSS UNTUK UI MODERN & DESIGN KOTAK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; padding: 4rem 2rem;
        border-radius: 20px; text-align: center; color: white; margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
    }
    .main-banner h1 { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #00f2ff; text-shadow: 0 0 15px rgba(0, 242, 255, 0.6); }
    .custom-card {
        background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px; padding: 20px; margin-bottom: 25px; position: relative; overflow: hidden;
    }
    .custom-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 10px; height: 40px;
        background: #007BFF; border-radius: 0 0 10px 0;
    }
    .section-title { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 800; color: #000000; margin-bottom: 20px; padding-left: 15px; }
    .status-comply { color: #00ff88; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
    .status-noncomply { color: #ff4b4b; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
    
    /* Tambahan CSS untuk Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px 5px 0px 0px;
        gap: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007BFF;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; border-radius: 5px;'>Standardized by NFPA 30 | HSSE SULAWESI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FUNGSI PEMBANTU SAFETY DISTANCE ---
def estimate_cap(dia):
    if dia <= 6.68: return 150
    elif dia <= 7.64: return 200
    elif dia <= 8.59: return 250
    elif dia <= 9.55: return 500
    elif dia <= 11.46: return 700
    elif dia <= 13.37: return 1500
    elif dia <= 15.28: return 2000
    elif dia <= 17.19: return 2500
    elif dia <= 19.10: return 5000
    elif dia <= 27.69: return 10000
    elif dia <= 30.56: return 12500
    elif dia <= 33.42: return 15000
    elif dia <= 40.11: return 20000
    elif dia <= 43.93: return 25000
    elif dia <= 48.70: return 30000
    else: return 50000

def get_nfpa_dist(cap):
    if cap <= 1.045: return 1.5, 1.5
    elif cap <= 2.85: return 3.0, 1.5
    elif cap <= 45.6: return 4.5, 1.5
    elif cap <= 114.0: return 6.0, 1.5
    elif cap <= 190.0: return 9.0, 3.0
    elif cap <= 380.0: return 15.0, 4.5
    elif cap <= 1900.0: return 24.0, 7.5
    elif cap <= 3800.0: return 30.0, 10.5
    elif cap <= 7600.0: return 40.5, 13.5
    elif cap <= 11400.0: return 49.5, 16.5
    else: return 52.5, 18.0

# --- PEMBUATAN TAB (MENU ATAS) ---
tab1, tab2 = st.tabs(["✅ MODE AUDIT (Evaluasi Desain)", "💡 MODE DESAIN (Rekomendasi Ukuran)"])

# ==============================================================================
# TAB 1: KODINGAN ASLI ANDA (MODE AUDIT)
# ==============================================================================
with tab1:
    # DEKLARASI VARIABEL DIJAMIN AMAN DI SINI
    d_atas_pond = [0.0] * 5
    d_bawah_pond = [0.0] * 5
    t_pondasis = [0.0] * 5
    d_tanks = [0.0] * 5

    col_shape, col_reset = st.columns([4, 1])
    with col_shape:
        shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
    with col_reset:
        if st.button("🔄 RESET SYSTEM", use_container_width=True):
            st.rerun()

    if shape == "Trapesium":
        st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Trapesium</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar")
        lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar")
        tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)
        lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0, key="lebar_atas")
        lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0, key="lebar_bawah")
        kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kapasitas")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
        for i in range(5):
            with st.expander(f"Tangki {i+1}"):
                ct1, ct2, ct3, ct4 = st.columns(4)
                d_atas_pond[i] = ct1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_tr_{i}")
                d_bawah_pond[i] = ct2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_tr_{i}")
                t_pondasis[i] = ct3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_tr_{i}")
                d_tanks[i] = ct4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_tr_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>Sistem Containment</div>", unsafe_allow_html=True)
        cont1, cont2 = st.columns(2)
        containment_type = cont1.selectbox("Metode Containment:", ["Open Diking", "Remote Impounding"], key="cont_tr")
        tipe_atap = cont2.selectbox("Tipe Atap Tangki:", ["Fixed Roof", "Floating Roof"], key="atap_tr")
        st.markdown("</div>", unsafe_allow_html=True)

        if tipe_atap == "Floating Roof":
            opsi_proteksi = ["Protection for Exposures (Sprinkler/Hydrant)", "Non Proteksi (None)"]
        else:
            opsi_proteksi = ["Protection for Exposures (Sprinkler/Hydrant)", "Approved Foam System", "Non Proteksi (None)"]

        st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
        cs1, cs2, cs3, cs4 = st.columns(4)
        produk = cs1.selectbox("Jenis BBM:", ["Pertalite", "Pertamax", "Solar", "Avtur", "MFO"], key="prod_tr")
        jenis_proteksi = cs2.selectbox("Sistem Proteksi:", opsi_proteksi, key="prot_tr")
        d_safety_1 = cs3.number_input("Diameter Tangki pembanding 1 (m)", min_value=0.0, key="sd_d1_tr")
        d_safety_2 = cs4.number_input("Diameter Tangki Pembanding 2 (m)", min_value=0.0, key="sd_d2_tr")
        st.markdown("</div>", unsafe_allow_html=True)

    else:  # Persegi
        st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Persegi</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        panjang = col1.number_input("Panjang (m)", min_value=0.0, key="p_per")
        lebar = col2.number_input("Lebar (m)", min_value=0.0, key="l_per")
        tinggi_dinding = panjang 
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
        col4, col6 = st.columns(2)
        lebar_dinding = col4.number_input("Lebar Dinding (m)", min_value=0.0, key="ld1_per")
        panjang_tebal_dinding = lebar_dinding 
        kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kap_per")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
        for i in range(5):
            with st.expander(f"Tangki {i+1}"):
                cp1, cp2, cp3, cp4 = st.columns(4)
                d_atas_pond[i] = cp1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_pr_{i}")
                d_bawah_pond[i] = cp2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_pr_{i}")
                t_pondasis[i] = cp3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_pr_{i}")
                d_tanks[i] = cp4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_pr_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='custom-card'><div class='section-title'>Sistem Containment</div>", unsafe_allow_html=True)
        cont1, cont2 = st.columns(2)
        containment_type = cont1.selectbox("Metode Containment:", ["Open Diking", "Remote Impounding"], key="cont_per")
        tipe_atap = cont2.selectbox("Tipe Atap Tangki:", ["Fixed Roof", "Floating Roof"], key="atap_per")
        st.markdown("</div>", unsafe_allow_html=True)

        if tipe_atap == "Floating Roof":
            opsi_proteksi = ["Protection for Exposures (Sprinkler/Hydrant)", "Non Proteksi (None)"]
        else:
            opsi_proteksi = ["Protection for Exposures (Sprinkler/Hydrant)", "Approved Foam System", "Non Proteksi (None)"]

        st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
        cs1, cs2, cs3, cs4 = st.columns(4)
        produk = cs1.selectbox("Jenis BBM:", ["Pertalite", "Pertamax", "Solar", "Avtur", "MFO"], key="prod_per")
        jenis_proteksi = cs2.selectbox("Sistem Proteksi:", opsi_proteksi, key="prot_per")
        d_safety_1 = cs3.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_pr")
        d_safety_2 = cs4.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_pr")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 HITUNG SEKARANG", type="primary", use_container_width=True, key="btn_audit"):
        if shape == "Trapesium":
            s_val = (lebar_bawah - lebar_atas) / 2
            t1_a = panjang_luar - (2 * lebar_bawah)            
            t1_b = panjang_luar - (2 * (lebar_atas + s_val))   
            l_eff = lebar_luar - (2 * lebar_bawah)             
            term1 = ((t1_a + t1_b) / 2) * tinggi_dinding * l_eff
            term2 = ((tinggi_dinding * s_val) / 2) * t1_b * 2
            vol_bruto = term1 + term2
        else:
            vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal_dinding)

        vol_pond_tank = 0
        for i in range(5):
            r_atas, r_bawah = d_atas_pond[i] / 2, d_bawah_pond[i] / 2
            v_pondasi = (1/3) * math.pi * t_pondasis[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
            v_tank = math.pi * (d_tanks[i]/2)**2 * max(0, tinggi_dinding - t_pondasis[i])
            vol_pond_tank += (v_pondasi + v_tank)
        
        vol_efektif_bund = vol_bruto - vol_pond_tank
        vol_min = kapasitas_tank_besar * 1.0

        est_kapasitas = estimate_cap(d_safety_1)
        dist_fac, dist_road = get_nfpa_dist(est_kapasitas) 
        
        if tipe_atap == "Floating Roof":
            if jenis_proteksi == "Non Proteksi (None)":
                tank_to_prop = min(d_safety_1 * 1.0, 52.5) 
                tank_to_road = (1/6) * d_safety_1
            else: 
                tank_to_prop = 0.5 * d_safety_1
                tank_to_road = (1/6) * d_safety_1
        else:  
            if jenis_proteksi == "Approved Foam System":
                mult_prop = 0.5
                mult_build = 0.5
            elif jenis_proteksi == "Non Proteksi (None)":
                mult_prop = 2.0  
                mult_build = 1.0 
            else: 
                mult_prop = 1.0
                mult_build = 1.0
                
            tank_to_road = dist_road * mult_build 
            tank_to_prop = dist_fac * mult_prop   

        if produk in ["Pertalite", "Pertamax"]:
            kelas_bbm_calc = "Class I"
        elif produk in ["Solar", "Avtur"]:
            kelas_bbm_calc = "Class II"
        else:
            kelas_bbm_calc = "Class IIIA"

        max_d_s = max(d_safety_1, d_safety_2)
        sum_d_s = d_safety_1 + d_safety_2
        
        if max_d_s <= 45:
            shell_to_shell = (1/6) * sum_d_s
        else:
            if containment_type == "Remote Impounding":
                if tipe_atap == "Floating Roof":
                    shell_to_shell = (1/6) * sum_d_s
                else: 
                    if kelas_bbm_calc in ["Class I", "Class II"]:
                        shell_to_shell = (1/4) * sum_d_s
                    else: 
                        shell_to_shell = (1/6) * sum_d_s
            else: 
                if tipe_atap == "Floating Roof":
                    shell_to_shell = (1/4) * sum_d_s
                else: 
                    if kelas_bbm_calc in ["Class I", "Class II"]:
                        shell_to_shell = (1/3) * sum_d_s
                    else: 
                        shell_to_shell = (1/4) * sum_d_s
        
        is_comply = vol_efektif_bund > kapasitas_tank_besar * 1 and tinggi_dinding <= 1.8
        status_class = "status-comply" if is_comply else "status-noncomply"
        status_text = "✓ COMPLY - AMAN" if is_comply else "✗ NON COMPLY"

        st.markdown(f"### 📈 HASIL ANALISIS")
        res1, res2, res3, res4 = st.columns(4)
        res1.metric("Volume Bruto", f"{vol_bruto:.2f} m³")
        res1.metric("Vol. Pond+Tank", f"{vol_pond_tank:.2f} m³")
        res2.metric("Vol. Efektif Bund", f"{vol_efektif_bund:.2f} m³")
        res2.metric("Volume Minimum", f"{vol_min:.2f} m³")
        with res3:
            st.write("Status Safety:")
            st.markdown(f"<div class='{status_class}'>{status_text}</div>", unsafe_allow_html=True)
        
        if d_safety_1 > 0:
            st.markdown("---")
            st.write(f"**Safety Distance Minimum (NFPA 30 - {produk}):**")
            sd_col1, sd_col2, sd_col3 = st.columns(3)
            sd_col1.metric("Shell to Shell", f"{shell_to_shell:.2f} m")
            sd_col2.metric("Shell to Building", f"{tank_to_road:.2f} m") 
            sd_col3.metric("Shell to Property", f"{tank_to_prop:.2f} m") 
            
            if produk in ["Pertalite", "Pertamax"]:
                kelas_bbm = "Class I"
            elif produk in ["Solar", "Avtur"]: 
                kelas_bbm = "Class II"
            else: 
                kelas_bbm = "Class IIIA"
                
            caption_text = f"Klasifikasi: {kelas_bbm} (Tabel Utama NFPA 30)."
            st.caption(caption_text)

        if not is_comply:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("💡 LIHAT REKOMENDASI "):
                st.markdown("### Rekomendasi Teknis HSSE")
                kekurangan = vol_min - vol_efektif_bund
                
                rec_col1, rec_col2 = st.columns(2)
                
                with rec_col1:
                    st.info("**Opsi Rekayasa Fisik**")
                    luas_estimasi = vol_bruto / tinggi_dinding if tinggi_dinding > 0 else 1
                    tambah_h = kekurangan / luas_estimasi
                    target_h = tinggi_dinding + tambah_h
                    
                    if target_h <= 1.8:
                        st.write(f"1. **Peninggian Dinding:** Target tinggi dinding baru adalah **{target_h:.2f} m** (Sesuai batas NFPA < 1.8m).")
                    else:
                        st.write(f"1. **Perluasan Area:** Peninggian dinding hingga 1.8m tidak cukup. Diperlukan perluasan panjang/lebar area.")
                    
                    st.write("2. **Remote Impounding:** Integrasikan antar bundwall untuk atasi keterbatasan volume. Gunakan sistem Remote Impounding dengan saluran peluap ke kolam sekunder")

                with rec_col2:
                    st.info("**Opsi Administratif & Operasional**")
                    aman_kl = vol_efektif_bund / 1.0
                    st.write(f"1. **Downgrading Kapasitas:** Batasi pengisian tangki terbesar maksimal hingga **{aman_kl:.2f} KL**.")
                    st.write("2. **Adjustment HLA:** Atur ulang sensor *High Level Alarm* (HLA) sesuai kapasitas bundwall saat ini.")
                    
                st.warning("⚠️ Perubahan fisik wajib melalui kajian teknis sipil dan pemastian jarak aman (Safety Distance) tetap terjaga.")


# ==============================================================================
# TAB 2: FITUR BARU (MODE PERENCANAAN / DESIGN GENERATOR)
# ==============================================================================
with tab2:
    # DEKLARASI VARIABEL DIJAMIN AMAN DI SINI
    d_atas_pond_d = [0.0] * 5
    d_bawah_pond_d = [0.0] * 5
    t_pondasis_d = [0.0] * 5
    d_tanks_d = [0.0] * 5

    st.markdown("<div class='custom-card'><div class='section-title'>⚙️ Mode Desain Generatif (Reverse Engineering)</div>", unsafe_allow_html=True)
    st.write("Mode ini digunakan untuk **Perencanaan Proyek Baru**. Algoritma akan menghitung mundur dimensi dinding yang ideal dengan **memperhitungkan volume pondasi & badan tangki** (Displacement) agar 100% presisi.")
    
    st.markdown("---")
    
    # Input Parameter Dinding
    st.markdown("#### 1. Dimensi Tangki & Dinding Rencana")
    col_d1, col_d2, col_d3 = st.columns(3)
    target_kapasitas_desain = col_d1.number_input("Kapasitas Tangki Terbesar (m³)", min_value=1.0, value=1000.0, key="cap_desain")
    lebar_atas_desain = col_d2.number_input("Lebar Atas Dinding (m)", min_value=0.1, value=0.3, key="la_desain")
    lebar_bawah_desain = col_d3.number_input("Lebar Bawah Dinding (m)", min_value=0.1, value=1.0, key="lb_desain")
    
    # Input Data Tangki untuk Displacement
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 2. Estimasi Data Tangki (Displacement Area)")
    
    for i in range(5):
        with st.expander(f"Data Rencana Tangki {i+1}"):
            cd1, cd2, cd3, cd4 = st.columns(4)
            d_atas_pond_d[i] = cd1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_des_{i}")
            d_bawah_pond_d[i] = cd2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_des_{i}")
            t_pondasis_d[i] = cd3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_des_{i}")
            d_tanks_d[i] = cd4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_des_{i}")

    st.markdown("---")
    
    # Pilihan Strategi Desain
    st.markdown("#### 3. Strategi Penguncian Lahan:")
    mode_desain = st.radio(
        "Pilih batasan dimensi yang mengunci desain Anda:",
        ["Kunci Luas Lahan (Sistem akan mencari Tinggi Dinding yang tepat)", 
         "Kunci Tinggi Dinding (Sistem akan mencari Luas Lahan yang tepat)"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if mode_desain == "Kunci Luas Lahan (Sistem akan mencari Tinggi Dinding yang tepat)":
        st.info("Lahan sudah dipatok (tidak bisa diperluas). Masukkan ukuran batas terluar tanah.")
        cd_l1, cd_l2 = st.columns(2)
        p_lahan = cd_l1.number_input("Batas Panjang Luar Lahan (m)", min_value=1.0, value=30.0, key="pl_desain")
        l_lahan = cd_l2.number_input("Batas Lebar Luar Lahan (m)", min_value=1.0, value=30.0, key="ll_desain")
        
        if st.button("🏗️ GENERATE TINGGI DINDING", type="primary", use_container_width=True, key="btn_gen_h"):
            # Cek Dimensi Ruang Dalam
            s_val = (lebar_bawah_desain - lebar_atas_desain) / 2
            t1_a = p_lahan - (2 * lebar_bawah_desain)            
            t1_b = p_lahan - (2 * (lebar_atas_desain + s_val))   
            l_eff = l_lahan - (2 * lebar_bawah_desain)             
            
            if t1_a <= 0 or l_eff <= 0:
                st.error("❌ Lahan terlalu sempit untuk dinding dengan tebal bawah tersebut! Ruang dalam menjadi minus.")
            else:
                # Koefisien Area Dinding (Mewakili Luas Penampang Efektif)
                term1_coeff = ((t1_a + t1_b) / 2) * l_eff
                term2_coeff = s_val * t1_b
                total_coeff_area = term1_coeff + term2_coeff
                
                # Hitung Total Displacement Tangki (Pondasi + Jejak Silinder Tangki)
                sum_v_pondasi = 0
                sum_area_tank = 0
                sum_area_tank_x_hpond = 0
                
                for i in range(5):
                    r_atas = d_atas_pond_d[i] / 2
                    r_bawah = d_bawah_pond_d[i] / 2
                    v_pond = (1/3) * math.pi * t_pondasis_d[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
                    sum_v_pondasi += v_pond
                    
                    area_tank = math.pi * ((d_tanks_d[i]/2)**2)
                    sum_area_tank += area_tank
                    sum_area_tank_x_hpond += (area_tank * t_pondasis_d[i])
                
                # Aljabar Reverse Engineering mencari Tinggi (H)
                penyebut = total_coeff_area - sum_area_tank
                
                if penyebut <= 0:
                    st.error("❌ Area tangki & pondasi memakan tempat lebih besar daripada luas tanah dalam tanggul! Silakan lebarkan tanah Anda.")
                else:
                    pembilang = target_kapasitas_desain + sum_v_pondasi - sum_area_tank_x_hpond
                    tinggi_req = pembilang / penyebut
                    
                    st.markdown("### 📊 Hasil Rekomendasi Desain:")
                    if tinggi_req <= 1.8 and tinggi_req > 0:
                        st.success(f"✅ Untuk menampung volume bersih **{target_kapasitas_desain} m³** beserta struktur tangki di dalamnya, Anda harus membangun dinding setinggi: **{tinggi_req:.2f} meter**.")
                        st.write("Desain ini **Aman dan Comply** dengan batas tinggi maksimal NFPA 30 (< 1.8 m).")
                    elif tinggi_req <= 0:
                         st.error("Dimensi yang dimasukkan tidak logis (Tangki lebih besar dari lahan).")
                    else:
                        st.error(f"❌ Diperlukan dinding setinggi: **{tinggi_req:.2f} meter**.")
                        st.warning("⚠️ **Peringatan NFPA 30:** Tinggi ini melebihi batas toleransi keselamatan (1.8m). Dinding terlalu tinggi akan memicu risiko akumulasi gas (H2S/HC) dan menyulitkan evakuasi saat kebakaran. Solusi: Perluas ukuran lahan luar Anda.")
                    
    else:
        st.info("Anda menetapkan batas tinggi dinding maksimal, dan ingin tahu berapa batas tanah luar (Persegi) minimum yang dibutuhkan.")
        t_dinding_plan = st.number_input("Rencana Tinggi Dinding (m)", min_value=0.1, max_value=1.8, value=1.5, help="Maksimal 1.8m sesuai NFPA", key="h_plan")
        
        if st.button("📐 GENERATE LUAS LAHAN", type="primary", use_container_width=True, key="btn_gen_l"):
            # Hitung Volume Displacement PASTI (karena Tinggi H sudah diketahui)
            vol_pond_tank_d = 0
            for i in range(5):
                r_atas = d_atas_pond_d[i] / 2
                r_bawah = d_bawah_pond_d[i] / 2
                v_pond = (1/3) * math.pi * t_pondasis_d[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
                v_tank = math.pi * (d_tanks_d[i]/2)**2 * max(0, t_dinding_plan - t_pondasis_d[i])
                vol_pond_tank_d += (v_pond + v_tank)
                
            # Total Kapasitas Kotor (Bruto) yang harus dicapai
            V_bruto_target = target_kapasitas_desain + vol_pond_tank_d
            
            # Reverse Math Kuadratik untuk mencari Luas Dalam
            h = t_dinding_plan
            s = (lebar_bawah_desain - lebar_atas_desain) / 2
            
            # Diskriminan untuk Geometri Trapesium
            A = h
            B = 2 * h * s
            C = (2 * h * (s**2)) - V_bruto_target
            
            D = (B**2) - (4 * A * C)
            
            if D < 0:
                st.error("❌ Dimensi tidak memungkinkan untuk membentuk geometri tanggul.")
            else:
                # W1 adalah Lebar/Panjang Dalam dasar
                W1 = (-B + math.sqrt(D)) / (2 * A)
                
                # Ukuran Lahan Luar = Panjang Dalam + 2x Ketebalan Bawah
                panjang_luar_req = W1 + (2 * lebar_bawah_desain)
                
                st.markdown("### 📊 Hasil Rekomendasi Desain:")
                st.success(f"✅ Untuk membuat dinding setinggi **{t_dinding_plan} m**, Anda harus menyiapkan Lahan Terluar berukuran:")
                st.markdown(f"#### **{panjang_luar_req:.2f} m x {panjang_luar_req:.2f} m**")
                
                st.write(f"**Validasi Data:**")
                st.write(f"- Ruang murni untuk fluida: **{target_kapasitas_desain} m³**")
                st.write(f"- Ruang tersita oleh badan tangki & pondasi: **{vol_pond_tank_d:.2f} m³**")
                st.write(f"- Total Kapasitas Bruto yang akan terbangun: **{V_bruto_target:.2f} m³**")
