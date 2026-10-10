# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- **keduanya (RPC dan MQ)**, alesan kami ingin memahami perbedaan nyata antara komunikasi sinkron dan asinkron dalam konteks sistem terdistribusi FoodGo. Dengan mengerjakan keduanya, kami bisa membandingkan langsung kapan masing-masing pola cocok digunakan. 

## Kendala teknis

### Jalur A (RPC)

- Tidak ada kendala berarti karena `xmlrpc` merupakan bagian dari Python standard library.

- Perlu memastikan port 8000 tidak digunakan proses lain sebelum menjalankan server.

- Jika server dimatikan saat client sedang memanggil, client akan mendapat `connectionRefusedError` - ini

membuktikan sifat **tightly coupled** dari RPC.

### Jalur B (MO)
- Perlu Docker Desktop yang sudah berjalan sebelum `docker compose up -d`.
- Kadang RabbitMQ butuh waktu ~10-15 detik untuk fully ready setelah container start; jika `publisher.py` dijalankan terlalu cepat, koneksi ditolak. Solusi: tunggu sampai dashboard `http://localhost:15672` bisa diakses.
## Uji "pesan tidak hilang" (khusus Jalur B)
- **Langkah uji:**
 1. Pastikan RabbitMQ sudah berjalan (` docker compose up -d`).
 2. **Matikan** consumer (jangan jalankan `consumer.py`).
 3. Jalankan `publisher.py` - 3 event terkirim ke queue.
 4. cek dashboard RabbitMQ di `http://localhost:15672` queue `pembayaran_berhasil` menunjukkan 3 pesan dalam status "Ready".
 5. **Nyalakan** `consumer.py` → ketiga pesan langsung diproses satu per satu.
- **Hasil yang diamati:** Pesan **tidak hilang** meskipun consumer tidak aktif saat publisher mengirim. Ini karena:
  - Queue dideklarasikan dengan `durable=True` → queue bertahan meskipun RabbitMQ restart.
  - Pesan dikirim dengan `delivery_mode=2` (persistent) → pesan disimpan di disk.
  - Consumer menggunakan manual `basic_ack` → pesan baru dihapus dari queue setelah consumer mengonfirmasi pemrosesan berhasil.
  - Ini adalah inti dari **asynchronous decoupling**: publisher dan consumer tidak perlu hidup bersamaan.

## Analisis: RPC vs Message Queue

### Mengapa RPC cocok untuk cek saldo?
- Modul Pesanan **butuh jawaban seketika** tentang saldo user sebelum memproses order.
- Sifat **sinkron** RPC menjamin client mendapat respons langsung (atau error jika server mati).
- Tidak masuk akal memproses pesanan tanpa mengetahui saldo terlebih dahulu.

### Mengapa MQ cocok untuk notifikasi kurir?
- Modul Pembayaran **tidak perlu menunggu** konfirmasi dari modul Kurir.
- Jika kurir sedang sibuk/down, pembayaran tetap harus selesai → **asinkron** mencegah blocking.
- Pesan tersimpan di queue sampai kurir siap → **reliabilitas** terjamin.

### Apa yang terjadi jika pola salah dipakai?
- **RPC untuk notifikasi kurir:** Jika modul Kurir down, `proses_pembayaran` di modul Pembayaran ikut hang/error. User yang sudah bayar harus menunggu atau mendapat error, padahal pembayaran sebenarnya sudah berhasil.
- **MQ untuk cek saldo:** Modul Pesanan mengirim permintaan cek saldo ke queue, tapi tidak langsung dapat jawaban. Tidak bisa melanjutkan proses order karena belum tahu saldo cukup atau tidak. Harus implementasi pola request-reply yang rumit (correlation ID) padahal sebenarnya cukup pakai RPC biasa.

### Apa yang terjadi pada RPC jika server mati di tengah proses?
- Client akan mendapat exception `ConnectionRefusedError` atau timeout.
- Tidak ada mekanisme retry otomatis – client harus menangani error sendiri.
- Ini menunjukkan **tight coupling**: ketersediaan server langsung mempengaruhi client.

### Ke mana pesan tersimpan saat consumer mati? (Jalur B)
- Pesan tersimpan di **queue RabbitMQ** yang ada di broker (container Docker).
- Karena queue `durable=True` dan pesan `delivery_mode=2`, pesan disimpan di **disk** (bukan hanya di memori).
- Saat consumer hidup kembali dan connect ke queue yang sama, RabbitMQ langsung mengirimkan pesan yang menunggu.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline – bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|----|----|----|----|----|
| ... | ... | ... | ... | ... |
| 2026-10-09 | Antigravity | Minta bantuan mengerjakan tugas 4 RPC dan MQ | AI membantu melengkapi skeleton code TODO dan menyusun analisis perbandingan RPC vs MQ | Kode diimplementasikan berdasarkan pemahaman konsep dari materi kuliah, AI membantu struktur dan penulisan |
