import heapq
import random
import streamlit as st

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="Smart Kiosk PT KAI", page_icon="🚂", layout="centered")

class NavigasiKeretaApi:
    """Aplikasi Sistem Manajemen dan Navigasi Kereta Api Modern menggunakan Dijkstra"""
    def __init__(self):
        self.jaringan_rel = {}
        
    def tambah_jalur_rel(self, stasiun1, stasiun2, jarak):
        if stasiun1 not in self.jaringan_rel:
            self.jaringan_rel[stasiun1] = []
        if stasiun2 not in self.jaringan_rel:
            self.jaringan_rel[stasiun2] = []
        self.jaringan_rel[stasiun1].append((stasiun2, jarak))
        self.jaringan_rel[stasiun2].append((stasiun1, jarak))

    def dapatkan_semua_stasiun(self):
        return sorted(list(self.jaringan_rel.keys()))

    def cari_rute_terpendek(self, asal, tujuan):
        if asal not in self.jaringan_rel or tujuan not in self.jaringan_rel:
            return None, float('inf')

        jarak_terpendek = {stasiun: float('inf') for stasiun in self.jaringan_rel}
        jarak_terpendek[asal] = 0
        stasiun_sebelumnya = {stasiun: None for stasiun in self.jaringan_rel}
        
        pq = [(0, asal)]
        stasiun_terbuka = set()

        while pq:
            jarak_sekarang, stasiun_sekarang = heapq.heappop(pq)
            if stasiun_sekarang in stasiun_terbuka:
                continue
            stasiun_terbuka.add(stasiun_sekarang)
            
            if stasiun_sekarang == tujuan:
                break
                
            for tetangga, bobot_jarak in self.jaringan_rel[stasiun_sekarang]:
                total_jarak = jarak_sekarang + bobot_jarak
                if total_jarak < jarak_terpendek[tetangga]:
                    jarak_terpendek[tetangga] = total_jarak
                    stasiun_sebelumnya[tetangga] = stasiun_sekarang
                    heapq.heappush(pq, (total_jarak, tetangga))

        if jarak_terpendek[tujuan] == float('inf'):
            return None, float('inf')
            
        rute = []
        stasiun_aktif = tujuan
        while stasiun_aktif is not None:
            rute.append(stasiun_aktif)
            stasiun_aktif = stasiun_sebelumnya[stasiun_aktif]
        rute.reverse()
        
        return rute, jarak_terpendek[tujuan]

    def tentukan_nama_kereta(self, asal, tujuan, kelas):
        rute_kereta = {
            ('Gambir', 'Bandung'): {'EKSEKUTIF': 'Argo Parahyangan', 'EKONOMI': 'Parahyangan Ekonomi'},
            ('Gambir', 'Semarang Tawang'): {'EKSEKUTIF': 'Argo Sindoro', 'EKONOMI': 'Menoreh'},
            ('Gambir', 'Surabaya Pasar Turi'): {'EKSEKUTIF': 'Argo Bromo Anggrek', 'EKONOMI': 'Kertajaya'},
            ('Bandung', 'Surabaya Gubeng'): {'EKSEKUTIF': 'Argo Wilis', 'EKONOMI': 'Pasundan'},
            ('Bandung', 'Yogyakarta Lempuyangan'): {'EKSEKUTIF': 'Lodaya', 'EKONOMI': 'Malabar Ekonomi'},
            ('Yogyakarta Lempuyangan', 'Surabaya Gubeng'): {'EKSEKUTIF': 'Sancaka', 'EKONOMI': 'Sri Tanjung'},
            ('Surabaya Gubeng', 'Banyuwangi Ketapang'): {'EKSEKUTIF': 'Blambangan Ekspres', 'EKONOMI': 'Probowangi'},
        }
        if (asal, tujuan) in rute_kereta:
            return rute_kereta[(asal, tujuan)][kelas]
        elif (tujuan, asal) in rute_kereta:
            return rute_kereta[(tujuan, asal)][kelas]
        return "Gajayana Luxury" if kelas == "EKSEKUTIF" else "Matarmaja"

    def cetak_boarding_pass_streamlit(self, data):
        """Template visual Boarding Pass asli KAI versi Streamlit"""
        st.success("🎫 Tiket Berhasil Dicetak / Ditemukan!")
        pass_html = f"""
        <div style="border: 2px dashed #ff5e00; padding: 20px; background-color: #fcfcfc; border-radius: 10px; font-family: monospace; color: #333;">
            <h3 style="text-align: center; color: #ff5e00; margin-bottom: 0;">BOARDING PASS KERETA API</h3>
            <p style="text-align: center; font-size: 12px; margin-top: 5px;">PT KERETA API INDONESIA</p>
            <hr style="border-top: 1px solid #ccc;">
            <table style="width:100%; font-size: 14px;">
                <tr><td><b>KODE BOOKING</b></td><td>: <span style="font-size:18px; color:#ff5e00;"><b>{data['kode']}</b></span></td><td><b>KERETA</b></td><td>: {data['kereta']}</td></tr>
                <tr><td><b>KELAS</b></td><td>: {data['kelas']}</td><td><b>KURSI</b></td><td>: {data['kursi']}</td></tr>
            </table>
            <hr style="border-top: 1px dashed #ccc;">
            <p style="margin: 5px 0;"><b>PENUMPANG :</b> {data['nama']} ({data['nik']})</p>
            <hr style="border-top: 1px dashed #ccc;">
            <p style="margin: 5px 0;"><b>STASIUN ASAL 🗺️ :</b> STASIUN {data['asal'].upper()}</p>
            <p style="margin: 5px 0;"><b>STASIUN TUJUAN 🏁 :</b> STASIUN {data['tujuan'].upper()}</p>
            <p style="margin: 5px 0;"><b>JARAK TEMPUH :</b> {data['jarak']} km | <b>ESTIMASI :</b> {data['waktu']}</p>
            <hr style="border-top: 1px dashed #ccc;">
            <p style="margin: 5px 0; font-size:12px;"><b>RUTE TRANSIT :</b> {' ➔ '.join(data['rute'])}</p>
            <hr style="border-top: 1px solid #ccc;">
            <h4 style="text-align: right; margin: 0; color: green;">TOTAL: Rp {data['harga']:,.0f} (LUNAS)</h4>
        </div>
        """
        st.markdown(pass_html, unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE STREAMLIT ---
# Menggunakan session_state agar database tiket tidak hilang saat halaman di-refresh/re-run
if 'database_tiket' not in st.session_state:
    st.session_state.database_tiket = {}

if 'aplikasi_ka' not in st.session_state:
    app = NavigasiKeretaApi()
    data_jalur_rel = [
        ('Gambir', 'Bandung', 150), ('Gambir', 'Semarang Tawang', 440),
        ('Bandung', 'Semarang Tawang', 390), ('Semarang Tawang', 'Surabaya Pasar Turi', 280),
        ('Bandung', 'Yogyakarta Lempuyangan', 360), ('Yogyakarta Lempuyangan', 'Surabaya Gubeng', 315),
        ('Gambir', 'Surabaya Pasar Turi', 720), ('Surabaya Pasar Turi', 'Surabaya Gubeng', 10), 
        ('Surabaya Gubeng', 'Banyuwangi Ketapang', 290)
    ]
    for s1, s2, j in data_jalur_rel:
        app.tambah_jalur_rel(s1, s2, j)
    st.session_state.aplikasi_ka = app

aplikasi_ka = st.session_state.aplikasi_ka
stasiun_tersedia = aplikasi_ka.dapatkan_semua_stasiun()

# --- TAMPILAN UTAMA WEB ---
st.title("🚂 SMART KIOSK INTERAKTIF KAI")
st.write("Selamat datang di sistem Navigasi & Reservasi Mandiri PT Kereta Api Indonesia.")

# Membuat Menu dengan Tabs Streamlit (Pengganti angka 1-6 pada CLI)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Peta Jaringan", 
    "🛒 Pesan Tiket", 
    "🖨️ Cetak Ulang", 
    "❌ Pembatalan", 
    "📊 Statistik"
])

# --- TAB 1: LIHAT PETA JARRINGAN ---
with tab1:
    st.header("Daftar Koneksi Stasiun Aktif")
    for stasiun, tetangga in aplikasi_ka.jaringan_rel.items():
        koneksi = ", ".join([f"{t[0]} ({t[1]} km)" for t in tetangga])
        st.markdown(f"**Stasiun {stasiun}** terhubung ke → `{koneksi}`")

# --- TAB 2: PEMESANAN TIKET BARU ---
with tab2:
    st.header("Formulir Reservasi Tiket")
    
    col1, col2 = st.columns(2)
    with col1:
        asal = st.selectbox("Pilih Stasiun Asal:", stasiun_tersedia, key="asal")
    with col2:
        tujuan = st.selectbox("Pilih Stasiun Tujuan:", stasiun_tersedia, key="tujuan")
        
    if asal == tujuan:
        st.warning("⚠️ Stasiun asal dan tujuan tidak boleh sama.")
    else:
        rute, total_jarak = aplikasi_ka.cari_rute_terpendek(asal, tujuan)
        if not rute:
            st.error("⚠️ Jalur rel stasiun tersebut tidak terhubung.")
        else:
            total_waktu_jam = total_jarak / 80
            waktu_str = f"{int(total_waktu_jam)} Jam {int((total_waktu_jam % 1) * 60)} Menit"
            
            st.info(f"🏁 **Rute Ditemukan!** Jarak: `{total_jarak} km` | Estimasi Waktu: `{waktu_str}`")
            
            kelas_pilihan = st.radio("Pilih Kelas Kereta:", ["Eksekutif (Rp 1.200/km)", "Ekonomi (Rp 600/km)"])
            kelas = "EKSEKUTIF" if "Eksekutif" in kelas_pilihan else "EKONOMI"
            tarif = 1200 if kelas == "EKSEKUTIF" else 600
            total_harga = total_jarak * tarif
            
            st.markdown(f"### Total Tagihan: **Rp {total_harga:,.0f}**")
            
            # Form Data Diri
            nama = st.text_input("Nama Lengkap Penumpang:").strip().upper()
            nik = st.text_input("Nomor NIK / ID Card:").strip()
            
            # Simulasi Uang Masuk via inputan angka Streamlit
            uang_dibayar = st.number_input("Masukkan Nominal Uang Pembayaran (Rp):", min_value=0, step=50000)
            
            if st.button("Proses Pembayaran & Cetak Tiket", type="primary"):
                if not nama or not nik:
                    st.error("⚠️ Data Nama dan NIK tidak boleh kosong!")
                elif uang_dibayar < total_harga:
                    st.error(f"⚠️ Uang Anda kurang! Sisa kekurangan: Rp {total_harga - uang_dibayar:,.0f}")
                else:
                    # Proses Sukses
                    kembalian = uang_dibayar - total_harga
                    if kembalian > 0:
                        st.balloons()
                        st.info(f"💵 Uang Kembalian Anda: **Rp {kembalian:,.0f}** (Silakan ambil kembalian)")
                    
                    # Generate data tiket
                    kode_booking = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
                    nomor_kursi = f"{random.randint(1, 14)}{random.choice(['A', 'B', 'C', 'D'])}"
                    nama_kereta = aplikasi_ka.tentukan_nama_kereta(asal, tujuan, kelas)
                    
                    tiket_baru = {
                        'kode': kode_booking, 'kereta': nama_kereta, 'kelas': kelas, 'kursi': nomor_kursi,
                        'nama': nama, 'nik': nik, 'asal': asal, 'tujuan': tujuan, 'jarak': total_jarak,
                        'waktu': waktu_str, 'rute': rute, 'harga': total_harga
                    }
                    
                    # Simpan ke database session state
                    st.session_state.database_tiket[kode_booking] = tiket_baru
                    
                    # Cetak tiket ke layar
                    aplikasi_ka.cetak_boarding_pass_streamlit(tiket_baru)

# --- TAB 3: CETAK ULANG BOARDING PASS ---
with tab3:
    st.header("Layanan Cetak Ulang Tiket")
    kode_cari = st.text_input("Masukkan 6 Digit Kode Booking Anda:", max_chars=6).strip().upper()
    
    if st.button("Cari & Cetak Tiket"):
        if kode_cari in st.session_state.database_tiket:
            tiket_temu = st.session_state.database_tiket[kode_cari]
            aplikasi_ka.cetak_boarding_pass_streamlit(tiket_temu)
        else:
            st.error("❌ Maaf, Kode Booking tidak valid atau sudah dibatalkan.")

# --- TAB 4: PEMBATALAN TIKET (REFUND) ---
with tab4:
    st.header("Pembatalan Tiket & Refund Dana")
    kode_batal = st.text_input("Masukkan Kode Booking yang Ingin Dibatalkan:", key="batal").strip().upper()
    
    if kode_batal:
        if kode_batal in st.session_state.database_tiket:
            tiket_batal = st.session_state.database_tiket[kode_batal]
            st.warning(f"Tiket ditemukan atas nama **{tiket_batal['nama']}** ({tiket_batal['kereta']})")
            
            refund_dana = tiket_batal['harga'] * 0.75
            st.markdown(f"Dana yang akan di-refund sebesar 75%: **Rp {refund_dana:,.0f}**")
            
            if st.button("Ya, Batalkan Perjalanan Ini", type="secondary"):
                del st.session_state.database_tiket[kode_batal]
                st.success(f"✅ Pembatalan Berhasil! Kode booking {kode_batal} telah hangus. Silakan ambil uang refund Anda.")
        else:
            st.error("❌ Kode booking tidak ditemukan.")

# --- TAB 5: STATISTIK JALUR ---
with tab5:
    st.header("Statistik Kepadatan Jaringan Rel")
    st.write("Urutan Stasiun Transit Hub paling strategis (berdasarkan jumlah koneksi):")
    
    terpadat = sorted(aplikasi_ka.jaringan_rel.items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (stasiun, rute_rel) in enumerate(terpadat, 1):
        st.markdown(f"{i}. **Stasiun {stasiun}** : Menghubungkan `{len(rute_rel)}` rute rel berbeda.")