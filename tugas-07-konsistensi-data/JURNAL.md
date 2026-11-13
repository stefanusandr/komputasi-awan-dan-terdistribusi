# Jurnal Proses — Tugas 7

## Diskusi Pemilihan Model Konsistensi

### Argumen yang Dipertimbangkan:
1. **Eventual Consistency Murni:**
   - Kelebihan: Latensi penulisan sangat rendah dan ketersediaan tinggi (*high availability*) karena server Jakarta dapat langsung merespons top-up tanpa menunggu server Bandung.
   - Kelemahan Fatal: Timbul *window of inconsistency*. Ketika pelanggan berpindah server dalam hitungan detik setelah top-up, pembacaan menghasilkan saldo lama (stale). Hal ini memicu penolakan transaksi (*insufficient funds*), komplain pengguna, dan risiko *double spending*.
   - Evaluasi: Eventual Consistency murni **ditolak** untuk kasus saldo *e-wallet*.

2. **Sequential Consistency (Data-Centric):**
   - Kelebihan: Menjamin bahwa semua replika (Jakarta dan Bandung) melihat urutan operasi yang identik secara global.
   - Kelemahan: Berdasarkan teorema CAP / PACELC, koordinasi sinkron antar-region lintas pulau/kota via jaringan WAN menimbulkan latensi tinggi pada setiap operasi top-up dan rentan mengalami *service disruption* jika terjadi *network partition*.
   - Evaluasi: Terlalu *overkill* dan mahal untuk diterapkan secara ketat di semua replika global.

3. **Client-Centric Consistency (Read-Your-Writes):**
   - Pertimbangan: Dalam transaksi *e-wallet*, sifat data bersifat personal (*client-scoped*). Pelanggan lain tidak perlu mengetahui secara instan kenaikan saldo pelanggan $A$. Kebutuhan mutlak adalah pelanggan $A$ harus selalu melihat hasil mutakhir dari apa yang ia tuliskan sendiri.
   - Evaluasi: Menjadi jalan tengah terbaik yang menyelesaikan akar masalah bisnis tanpa mengorbankan performa sistem secara global.

### Kesimpulan Akhir & Alasan:
- **Model Terpilih:** **Client-Centric Consistency dengan jaminan Read-Your-Writes (RYW)** didukung oleh *Monotonic Reads*.
- **Alasan:** Memungkinkan sistem FoodGo tetap memanfaatkan arsitektur replikasi asinkron antar-region (cepat dan hemat bandwidth), namun dengan jaminan proteksi di layer aplikasi: klien membawa token versi (*session version metadata*), sehingga jika permintaan baca mendarat di replika yang tertinggal (*stale*), server secara cerdas mengalihkan query (*redirect*) ke master atau menahan sejenak (*catch-up wait*) hingga data ter-update.

---

## Simulasi (src/replica_simulation.py)

### Implementasi:
- **TODO 1:** Menggunakan `threading.Timer(REPLICATION_DELAY, ...)` dengan delay 2.0 detik untuk mensimulasikan latensi replikasi asinkron dari server Jakarta ke server Bandung.
- **TODO 2:** Menambahkan fungsi pengawal `baca_saldo_read_your_writes()` yang memeriksa nomor versi pada replika tujuan dengan nomor versi yang diketahui klien (`versi_minimal`). Menyediakan penanganan via *redirect* ke server Jakarta dan *wait/polling* hingga replika lokal ter-update.
- **TODO 3:** Menguji pemanggilan fungsi tersebut segera setelah top-up ($t = 0.5\text{ detik} < 2.0\text{ detik}$) dan memverifikasi saldo yang terbaca.

### Hasil Skenario Naif vs Read-Your-Writes:
1. **Skenario Naif (Tanpa Read-Your-Writes):**
   - Pelanggan top-up Rp 50.000 ke Server Jakarta (Versi 1).
   - Setelah 0.5 detik, pelanggan memesan makanan melalui Server Bandung.
   - Hasil baca saldo dari Bandung: **Rp 0.0**.
   - Analisis: Terjadi *inconsistent read* (bug). Pesanan pelanggan ditolak karena server Bandung belum menerima paket replikasi yang masih berada dalam perjalanan (*in-flight*).
2. **Skenario dengan Read-Your-Writes:**
   - Pelanggan top-up Rp 20.000 ke Server Jakarta (Total saldo Rp 70.000, Versi 2). Klien mencatat `known_version = 2`.
   - Setelah 0.5 detik, pelanggan membaca saldo melalui Server Bandung dengan membawa token `versi_minimal = 2`.
   - Server Bandung mendeteksi bahwa data lokalnya masih Versi 1 (< Versi 2).
   - Melalui mekanisme *Read-Your-Writes (Redirect)*, pembacaan otomatis dialihkan ke Server Jakarta dan mengembalikan saldo tepat **Rp 70.000**.
   - Melalui mekanisme *Read-Your-Writes (Wait)*, server menahan respon sejenak hingga replikasi tiba pada detik ke-2, lalu mengembalikan saldo tepat **Rp 70.000**.
   - Transaksi pemesanan makanan berhasil 100%.

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-13 | Antigravity (Gemini) | Brainstorming perbandingan trade-off antara Data-Centric (Sequential/Eventual) vs Client-Centric Consistency pada kasus saldo dompet digital perbankan/e-wallet | AI menjelaskan konsep teoretis CAP theorem, latensi WAN, perbedaan data-centric vs client-centric, dan opsi jaminan seperti Read-Your-Writes dan Monotonic Reads | Ide dipetakan secara spesifik ke studi kasus FoodGo (Jakarta-Bandung), menyusun argumentasi dampak bisnis konkret (false negative saldo, CS spike, double spending), merancang sequence diagram Mermaid mandiri, serta menyusun kode simulasi Python dengan mekanisme version token. |
| 2026-11-13 | Antigravity (Gemini) | Brainstorming ide skenario tambahan di ekosistem ride-hailing/ojek online yang membutuhkan model konsistensi berbeda | AI memberikan variasi ide seperti pelacakan posisi armada kurir, klaim voucher diskon kuota terbatas, dan sistem review/rating | Memilih dan mengelaborasi dua kasus nyata: Klaim Flash Voucher (Sequential Consistency karena perlindungan race condition kuota) dan Live GPS Tracking Kurir (Monotonic Reads untuk mencegah marker motor melompat mundur di layar pengguna). |
