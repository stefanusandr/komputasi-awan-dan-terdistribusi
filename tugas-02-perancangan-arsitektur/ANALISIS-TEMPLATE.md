# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Kelompok:** [kelompok 3]

| Nama | NIM |
|---|---|
| [Stefanus Andri Hendrawan] | [103072400115] | 
| [Fatih Khairu Alfifiajri] | [103072400105] | 
| [Moh Irham Maulana A.S] | [103072400063] | 

# Laporan Submission Tugas 2 — Perancangan Arsitektur FoodGo

## 1. Pemilihan Gaya Arsitektur & Justifikasi

### Gaya yang Dipilih:
Kombinasi (**Hybrid**) antara **Service-Oriented Architecture (SOA)** dan **Publish-Subscribe (Pub-Sub / Event-Driven)**.

### Justifikasi Pemilihan:
Keputusan ini diambil langsung berdasarkan evaluasi kegagalan FoodGo pada Tugas 1:
1. **Mengapa tidak Murni SOA (Semua Sinkron / REST API)?**  
   Pada Tugas 1 terbukti bahwa panggilan sinkron berantai (*chain request*) tanpa timeout membuat modul pesanan menggantung saat modul pembayaran lambat (Pitfall 1 & 2). Jika alur notifikasi resto dan penugasan kurir juga dipaksa sinkron (Pesanan panggil Resto, lalu Pesanan panggil Kurir), latensi jaringan akan menumpuk. Lebih fatal lagi, jika tim kurir sedang melakukan deploy pembaruan modul atau service kurir sedang *down*, transaksi pemesanan pelanggan akan langsung gagal atau timeout padahal pembayaran sudah terpotong. Ini berarti masalah *tight coupling* belum terselesaikan.

2. **Mengapa tidak Murni Pub-Sub (Semua Asinkron)?**  
   Jika proses checkout dan pembayaran dipaksa asinkron murni lewat antrean pesan (*queue*), pelanggan yang menekan tombol "Bayar" tidak akan langsung tahu apakah saldo/kartunya berhasil didebit atau ditolak detik itu juga. Pelanggan butuh respons langsung (*immediate feedback/consistency*) di layar aplikasi mereka bahwa pembayaran telah tervalidasi sebelum masuk ke tahap pembuatan makanan.

3. **Solusi Pendekatan Hybrid:**  
   - **SOA (Komunikasi Sinkron Request-Response):** Diterapkan pada fase transaksi kritis antara Client $\rightarrow$ API Gateway $\rightarrow$ Modul Pesanan $\rightarrow$ Modul Pembayaran. Panggilan ini diberi batas *timeout* yang jelas (solusi Pitfall 2 Tugas 1) dan mengembalikan status langsung ke pelanggan.
   - **Pub-Sub (Komunikasi Asinkron Event-Driven):** Diterapkan segera setelah pembayaran berhasil diverifikasi (`OrderPaid`). Modul Pesanan cukup mempublikasikan satu event ke Message Broker. Modul Resto dan Modul Kurir/Notifikasi bertindak sebagai subscriber independen yang menerima event tersebut tanpa membuat Modul Pesanan harus menunggu respon keduanya.

## 2. Komponen Sistem dan Peranannya

Sistem dirancang terdiri dari 4 komponen utama:

1. **API Gateway**
   - Berfungsi sebagai pintu masuk tunggal (*single point of entry*) untuk seluruh permintaan dari aplikasi pelanggan.
   - Menangani routing ke service internal, autentikasi, dan memisahkan jaringan luar dari service backend.

2. **Modul Pesanan (Order Service)**
   - Mengelola siklus hidup pesanan (status: `PENDING_PAYMENT`, `PAID`, `PREPARING`, `DELIVERING`, `COMPLETED`).
   - Menerima pesanan baru dari API Gateway, berkoordinasi secara sinkron dengan Modul Pembayaran, dan mengupdate status pesanan.
   - Berperan sebagai **Publisher** yang mengirimkan event `OrderPaid` ke Message Broker ketika transaksi pembayaran telah sukses.

3. **Modul Pembayaran (Payment Service)**
   - Berdiri sebagai service independen untuk memproses transaksi finansial (e-wallet, bank, dsb.).
   - Menerima request pemrosesan pembayaran dari Modul Pesanan secara sinkron dan mengembalikan status hasil transaksi (berhasil/gagal).
   - Pemisahan ini memecahkan masalah Tugas 1 di mana modul pembayaran menjadi *bottleneck* tunggal yang melumpuhkan seluruh server monolitik.

4. **Message Broker (Event Bus)**
   - Menggunakan perantara antrean pesan (misalnya RabbitMQ / Apache Kafka).
   - Menampung event `OrderPaid` ke dalam antrean persisten (*queue*) dan menyalurkannya ke service yang berlangganan (*subscriber*).
   - Menjadi penyangga (*buffer*) agar bila ada service penerima yang lambat atau sedang restart, pesan tidak hilang.
