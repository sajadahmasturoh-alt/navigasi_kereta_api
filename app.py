import heapq
import random

class NavigasiKeretaApi:
    """Aplikasi Sistem Manajemen dan Navigasi Kereta Api Modern menggunakan Dijkstra"""
    def __init__(self):
        self.jaringan_rel = {}
        self.database_tiket = {} # Menyimpan tiket aktif berdasarkan kode booking
        
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

    def cetak_boarding_pass(self, data):
        """Template visual Boarding Pass asli KAI"""
        print("\n+" + "="*68 + "+")
        print(f"|                     BOARDING PASS KERETA API                       |")
        print("+" + "="*68 + "+")
        print(f"  KODE BOOKING : {data['kode']}                      KERETA : {data['kereta']}")
        print(f"  KELAS        : {data['kelas']}                    KURSI  : {data['kursi']}")
        print("-" * 70)
        print(f"  PENUMPANG    : {data['nama']}")
        print(f"  NIK/ID       : {data['nik']}")
        print("-" * 70)
        print(f"  STASIUN ASAL : STASIUN {data['asal'].upper()}")
        print(f"  STASIUN TUJUAN: STASIUN {data['tujuan'].upper()}")
        print(f"  JARAK TEMPUH : {data['jarak']} km")
        print(f"  ESTIMASI     : {data['waktu']}")
        print("-" * 70)
        print(f"  JALUR REL TRANSIT YANG DILEWATI:")
        print(f"  ➔ {' ➔ '.join(data['rute'])}")
        print("-" * 70)
        print(f"  TOTAL BAYAR  : Rp {data['harga']:,.0f} (STATUS: LUNAS)")
        print("+" + "="*68 + "+")
        print("|   Terima Kasih. Semoga Perjalanan Anda Menyenangkan & Aman!        |")
        print("+" + "="*68 + "+\n")


# --- ALUR PROSES RESERVASI & MESIN PEMBAYARAN ---
def menu_pesan_tiket(aplikasi_ka):
    stasiun_tersedia = aplikasi_ka.dapatkan_semua_stasiun()
    print(f"\n--- RESERVASI TIKET KERETA API ---")
    for i, stasiun in enumerate(stasiun_tersedia, 1):
        print(f"[{i}] Stasiun {stasiun}")
    print("-" * 40)
    
    asal = input("Masukkan Nama Stasiun Asal  : ").strip()
    tujuan = input("Masukkan Nama Stasiun Tujuan: ").strip()

    if asal not in stasiun_tersedia or tujuan not in stasiun_tersedia or asal == tujuan:
        print("\n[⚠️] Stasiun tidak valid atau sama! Pemesanan dibatalkan.\n")
        return

    rute, total_jarak = aplikasi_ka.cari_rute_terpendek(asal, tujuan)
    if not rute:
        print("\n[⚠️] Jalur rel stasiun tersebut tidak terhubung.\n")
        return

    # Estimasi Waktu
    total_waktu_jam = total_jarak / 80
    waktu_str = f"{int(total_waktu_jam)} Jam {int((total_waktu_jam % 1) * 60)} Menit"

    print(f"\n[✔] Rute Ditemukan! Jarak: {total_jarak} km | Estimasi Waktu: {waktu_str}")
    print("1. Eksekutif (Rp 1.200/km) | 2. Ekonomi (Rp 600/km)")
    pilihan_kelas = input("Pilih kelas (1/2): ").strip()

    if pilihan_kelas == '1':
        kelas, tarif = "EKSEKUTIF", 1200
    elif pilihan_kelas == '2':
        kelas, tarif = "EKONOMI", 600
    else:
        print("[⚠️] Pilihan tidak valid.")
        return

    nama_kereta = aplikasi_ka.tentukan_nama_kereta(asal, tujuan, kelas)
    total_harga = total_jarak * tarif

    print(f"\n--- FORMULIR IDENTITAS PENUMPANG ---")
    nama = input("Nama Lengkap Penumpang: ").strip().upper()
    nik = input("Masukkan Nomor NIK      : ").strip()
    
    if not nama or not nik:
        print("[⚠️] Data tidak boleh kosong!")
        return

    # --- SIMULASI MESIN PEMBAYARAN TUNAI ---
    print(f"\n========================================")
    print(f"        MESIN PEMBAYARAN KIOSK          ")
    print(f"========================================")
    print(f" Total Tagihan: Rp {total_harga:,.0f}")
    print(f"----------------------------------------")
    
    uang_masuk = 0
    while uang_masuk < total_harga:
        try:
            print(f" Sisa yang harus dibayar: Rp {total_harga - uang_masuk:,.0f}")
            masukkan_uang = int(input(" Masukkan uang yang di bayar Anda (Rp): "))
            if masukkan_uang <= 0:
                print(" [⚠️] Masukkan nominal uang yang valid!")
                continue
            uang_masuk += masukkan_uang
        except ValueError:
            print(" [⚠️] Masukkan angka saja!")

    print(f"----------------------------------------")
    print(f" [✔] Pembayaran Berhasil Diterima!")
    kembalian = uang_masuk - total_harga
    if kembalian > 0:
        print(f" Uang Kembalian Anda: Rp {kembalian:,.0f} (Silahkan ambil di laci mesin)")
    print(f"========================================\n")

    # Penyimpanan Data Tiket
    kode_booking = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
    nomor_kursi = f"{random.randint(1, 14)}{random.choice(['A', 'B', 'C', 'D'])}"
    
    tiket_baru = {
        'kode': kode_booking, 'kereta': nama_kereta, 'kelas': kelas, 'kursi': nomor_kursi,
        'nama': nama, 'nik': nik, 'asal': asal, 'tujuan': tujuan, 'jarak': total_jarak,
        'waktu': waktu_str, 'rute': rute, 'harga': total_harga
    }
    
    aplikasi_ka.database_tiket[kode_booking] = tiket_baru
    print("[⌛] Sedang mencetak tiket otomatis...")
    aplikasi_ka.cetak_boarding_pass(tiket_baru)


# --- PROGRAM UTAMA MENGGUNAKAN LOOP MENU ---
if __name__ == "__main__":
    aplikasi_ka = NavigasiKeretaApi()

    # Data Jaringan Rel Utama
    data_jalur_rel = [
        ('Gambir', 'Bandung', 150), ('Gambir', 'Semarang Tawang', 440),
        ('Bandung', 'Semarang Tawang', 390), ('Semarang Tawang', 'Surabaya Pasar Turi', 280),
        ('Bandung', 'Yogyakarta Lempuyangan', 360), ('Yogyakarta Lempuyangan', 'Surabaya Gubeng', 315),
        ('Gambir', 'Surabaya Pasar Turi', 720), ('Surabaya Pasar Turi', 'Surabaya Gubeng', 10), 
        ('Surabaya Gubeng', 'Banyuwangi Ketapang', 290)
    ]
    for s1, s2, j in data_jalur_rel:
        aplikasi_ka.tambah_jalur_rel(s1, s2, j)

    # Cetak menu panduan pertama kali di awal program berjalan
    print("\n" + "="*55)
    print("   SMART KIOSK INTERAKTIF PT KERETA API INDONESIA")
    print("="*55)
    print(" 1. Lihat Peta Hub Jaringan Rel Stasiun")
    print(" 2. Pemesanan Tiket Baru & Pembayaran Tunai")
    print(" 3. Cetak Ulang Boarding Pass (Cek Kode Booking)")
    print(" 4. Pembatalan Tiket Perjalanan (Refund Dana)")
    print(" 5. Cek Info Statistik Jaringan Rel Terpadat")
    print(" 6. Selesai / Keluar Sistem")
    print("-" * 55)

    while True:
        # Loop ini sekarang hanya akan langsung memunculkan inputan pilih menu layanan saja
        pilihan = input("Pilih menu layanan (1-6): ").strip()

        if pilihan == '1':
            print(f"\n--- DAFTAR KONEKSI STASIUN AKTIF ---")
            for stasiun, tetangga in aplikasi_ka.jaringan_rel.items():
                print(f" Stasiun {stasiun:22} terhubung ke -> ", end="")
                print(", ".join([f"{t[0]} ({t[1]} km)" for t in tetangga]))
            print("-" * 55)

        elif pilihan == '2':
            menu_pesan_tiket(aplikasi_ka)
            print("-" * 55)

        elif pilihan == '3':
            print(f"\n--- LAYANAN CETAK ULANG TIKET ---")
            kode = input("Masukkan 6 Digit Kode Booking Anda: ").strip().upper()
            if kode in aplikasi_ka.database_tiket:
                print("\n[✔] Data Ditemukan! Mengambil berkas tiket...")
                aplikasi_ka.cetak_boarding_pass(aplikasi_ka.database_tiket[kode])
            else:
                print("\n[❌] Maaf, Kode Booking tidak valid atau sudah dibatalkan.\n")
            print("-" * 55)

        elif pilihan == '4':
            print(f"\n--- PEMBATALAN TIKET & REFUND DANA ---")
            kode = input("Masukkan Kode Booking yang ingin dibatalkan: ").strip().upper()
            if kode in aplikasi_ka.database_tiket:
                tiket = aplikasi_ka.database_tiket[kode]
                print(f"\nDetail Tiket ditemukan atas nama: {tiket['nama']} ({tiket['kereta']})")
                konf = input("Apakah Anda yakin ingin membatalkan perjalanan? (y/n): ").strip().lower()
                if konf == 'y':
                    refund_dana = tiket['harga'] * 0.75
                    del aplikasi_ka.database_tiket[kode]
                    print(f"\n[✔] Pembatalan Berhasil. Kode booking {kode} hangus.")
                    print(f"    Dana refund sebesar 75% (Rp {refund_dana:,.0f}) keluar dari laci uang.")
                else:
                    print("\nPembatalan digagalkan.")
            else:
                print("\n[❌] Kode booking tidak ditemukan.\n")
            print("-" * 55)

        elif pilihan == '5':
            print(f"\n--- STATISTIK KEPADATAN JALUR REL ---")
            terpadat = sorted(aplikasi_ka.jaringan_rel.items(), key=lambda x: len(x[1]), reverse=True)
            print("Urutan stasiun Transit Hub paling strategis:")
            for i, (stasiun, rute) in enumerate(terpadat, 1):
                print(f" {i}. Stasiun {stasiun:22} : Menghubungkan {len(rute)} rute rel berbeda.")
            print("-" * 55)

        elif pilihan == '6':
            print("\nSistem Kiosk dinatikan. Semoga harimu menyenangkan bersama KAI!")
            break
            
        else:
            print("\n[⚠️] Pilihan tidak valid! Silakan masukkan angka 1 sampai 6.")
            print("-" * 55)