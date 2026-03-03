# ==========================================
# TAB 3: LAPOR INSIDEN (FORM & UPDATE STATUS)
# ==========================================
with tab3:
    st.markdown("### ⚠️ Pelaporan Kondisi Tidak Aman (Unsafe Condition)")
    
    # 1. FORM INPUT LAPORAN (UNTUK USER)
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
    
    # 2. TAMPILKAN TABEL LAPORAN
    st.markdown("#### 📋 Log Laporan Insiden Terbaru")
    st.dataframe(st.session_state.data_insiden, use_container_width=True, hide_index=True)

    # 3. FITUR UPDATE STATUS KHUSUS ADMIN (BARU)
    st.markdown("#### 🛠️ Panel Admin: Update Status Laporan")
    if len(st.session_state.data_insiden) == 0:
        st.info("Belum ada laporan yang perlu diurus.")
    else:
        # Bikin form kecil untuk update status
        col_admin1, col_admin2 = st.columns(2)
        with col_admin1:
            # Memilih laporan berdasarkan urutan (index)
            pilih_laporan = st.selectbox(
                "Pilih Laporan yang akan di-update:", 
                st.session_state.data_insiden.index, 
                format_func=lambda x: f"Laporan {x+1} - {st.session_state.data_insiden.loc[x, 'Lokasi']}"
            )
        with col_admin2:
            status_baru = st.selectbox(
                "Ubah Status Menjadi:", 
                ["Pending 🔴", "Sedang Ditangani 🟡", "Approved / Selesai 🟢"]
            )
            
        if st.button("Update Status Laporan 💾", type="primary"):
            st.session_state.data_insiden.loc[pilih_laporan, "Status"] = status_baru
            st.success("Status berhasil diperbarui! Silakan lihat perubahan di tabel atas.")
            time.sleep(1) # Jeda sedikit sebelum tabel otomatis ter-refresh
            st.rerun() # Perintah otomatis Streamlit untuk me-refresh halaman

    st.divider()
    
    # 4. BUKU SAKU SOP
    st.markdown("### 📚 Buku Saku SOP Keselamatan Darurat")
    with st.expander("SOP Penanganan Tumpahan Bahan Kimia (Spill Kit)"):
        st.write('''
        1. **Amankan Area:** Pasang barikade atau tanda peringatan di sekitar tumpahan.
        2. **Gunakan APD:** Wajib menggunakan kacamata safety, sarung tangan nitrile, dan masker.
        3. **Gunakan Absorben:** Taburkan pasir atau bantalan penyerap dari kotak *Spill Kit*.
        4. **Pembuangan:** Sapu material penyerap dan masukkan ke kantong plastik kuning (Limbah B3).
        ''')
