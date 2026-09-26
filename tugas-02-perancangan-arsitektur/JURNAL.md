# Jurnal Proses — Tugas 2

**Kelompok:** Kelompok 3  
**Anggota:** Stefanus Andri Hendrawan (103072400115), [nama 2], [nama 3]

## Sesi 1: Evaluasi Masalah Tugas 1 & Brainstorming Opsi Arsitektur
- **Poin Diskusi & Keterhubungan dengan Tugas 1:**
  - Kami membuka kembali file analisis Tugas 1 untuk melihat 3 poin utama kegagalan sistem FoodGo saat trafik tinggi:
    1. Menganggap jaringan selalu andal (*the network is reliable*) yang membuat sistem tidak siap saat terjadi paket hilang/drop pada modul pembayaran.
    2. Mengabaikan latensi (*latency is zero*) dan tidak melakukan timeout pada pemanggilan antar service.
    3. Menggunakan desain *Single Point of Failure* (monolitik) yang membuat modul pembayaran menjadi *bottleneck* dan satu server crash melumpuhkan seluruh modul (kurir, resto, pesanan).
  - Stefanus menegaskan bahwa arsitektur baru di Tugas 2 harus secara langsung memecahkan 3 kelemahan desain di atas, terutama kebutuhan agar tim kurir dan tim resto bisa *decoupled* saat rilis/deploy.
- **Opsi arsitektur yang dipertimbangkan:**
  1. *Opsi 1 — Murni SOA (Request-Response Sinkron):*
     - Semua modul dipecah menjadi service mandiri, tapi komunikasinya tetap sinkron lewat REST/gRPC dari Pesanan $\rightarrow$ Pembayaran $\rightarrow$ Resto $\rightarrow$ Kurir.
     - *Perbedaan pendapat / bantahan:* Stefanus dan [nama 3] menilai opsi ini belum menuntaskan masalah latensi dan coupling. Kalau modul kurir lambat atau sedang di-restart, thread pesanan tetap terkunci dan pelanggan tidak bisa menyelesaikan transaksi.
  2. *Opsi 2 — Murni Publish-Subscribe (Event-Driven Penuh):*
     - Semua proses dari checkout, pembayaran, sampai penugasan kurir dilempar lewat Message Broker.
     - *Perbedaan pendapat / bantahan:* [nama 2] sempat mengusulkan ini agar full asinkron. Tapi Stefanus tidak setuju karena pelanggan yang membayar e-wallet butuh respons langsung (*immediate feedback*) di aplikasi apakah uangnya berhasil dipotong atau saldo kurang. Pembayaran tidak ramah UX jika dibuat asinkron murni.
  3. *Opsi 3 — Hybrid (SOA Sinkron untuk Pembayaran + Pub-Sub Asinkron untuk Resto & Kurir):*
     - Transaksi pesanan dan validasi pembayaran berjalan sinkron dengan batas timeout tegas. Begitu pembayaran sukses, Modul Pesanan cukup melempar event `OrderPaid` ke Message Broker tanpa perlu menunggu resto maupun kurir.
- **Alasan memilih Opsi 3 (Hybrid SOA + Pub-Sub):**
  - Opsi ini paling pas dan realistis untuk kasus FoodGo: memberikan kepastian instan untuk pembayaran finansial pelanggan, sekaligus memberikan *decoupling* penuh bagi tim resto dan tim kurir agar tidak saling sandera.

## Perancangan Diagram & Detail Komunikasi
- **Poin diskusi:** Menyusun alur skenario *end-to-end* (pelanggan pesan $\rightarrow$ bayar $\rightarrow$ resto masak $\rightarrow$ kurir jemput) dan menentukan batas tanggung jawab tiap service.
- **Revisi diagram (Versi 1 → Versi 2, apa yang berubah dan kenapa):**
  - *Versi 1 (Sketsa Awal Stefanus):*
    - Modul Pembayaran yang langsung mem-publish event `OrderPaid` ke Message Broker setelah transaksi pembayaran sukses.
    - Belum ada API Gateway (aplikasi mobile pelanggan langsung menembak IP/port Modul Pesanan).
  - *Kritik & Masukan Kelompok:*
    - [nama 3] mengingatkan bahwa Modul Pembayaran harus fokus ke transaksi finansial saja, tidak boleh tercampur logika bisnis pesanan (katalog makanan, alamat resto). Yang bertanggung jawab atas siklus status pesanan adalah Modul Pesanan.
    - [nama 2] mengusulkan penambahan API Gateway di layer paling depan sebagai *single entry point* untuk keamanan dan manajemen request routing.
  - *Versi 2 (Diagram Final):*
    - Menambahkan API Gateway sebagai pintu masuk utama request pelanggan.
    - Mengubah alur: Modul Pembayaran hanya mengembalikan respons sukses ke Modul Pesanan secara sinkron.
    - Modul Pesanan yang mengubah status lokal menjadi `PAID` lalu mem-publish event `OrderPaid` lengkap dengan payload data pesanan ke Message Broker.
    - Modul Resto dan Modul Kurir mengambil event dari broker secara paralel dan independen.


## Analisis Trade-off & Review Silang
- **Review Silang:**
  - Stefanus memeriksa bagian analisis *decoupling* tim kurir dan tim resto yang ditulis [nama 2]: penjelasannya sudah tepat, isolasi container memastikan tim kurir bisa rilis update tanpa bikin service resto down.
  - [nama 2] dan [nama 3] mengecek bagian trade-off agar tidak berat sebelah (tidak hanya memuji arsitektur baru).
- **Poin Kritis Trade-off yang Disepakati:**
  1. *Kompleksitas Debugging:* Alur Pub-Sub tidak linear sehingga tracing error lebih sulit dibanding monolit. Perlu Correlation ID di setiap payload event.
  2. *Potensi SPOF Baru:* Message Broker menjadi simpul pusat pesan, sehingga broker wajib di-deploy dengan replikasi/clustering.
  3. *Idempotency:* Service kurir dan resto harus tahan terhadap potensi pesan duplikat dari antrean broker.

---

## Kesimpulan Diskusi Kelompok (Sinkronisasi dengan Tugas 1 & Tugas 2)

Berdasarkan seluruh sesi diskusi, kelompok kami menyimpulkan bahwa rancangan arsitektur hybrid ini secara langsung menjawab ketiga akar masalah kegagalan sistem yang kami temukan pada Tugas 1:

1. **Menjawab Masalah Jaringan Tidak Andal & Paket Drop (Pitfall 1 Tugas 1):**
   - Pemanggilan pembayaran kini dipasangi penanganan error dan retry terukur dengan batas timeout yang jelas.
   - Untuk alur ke resto dan kurir, Message Broker berfungsi sebagai penyangga (*buffer*). Jika jaringan ke service kurir sempat drop atau service kurir sedang offline, event `OrderPaid` tetap tersimpan aman di antrean (*message persistence*) dan akan langsung diproses begitu service kembali terhubung.

2. **Menjawab Masalah Latensi Nol & Ketiadaan Timeout (Pitfall 2 Tugas 1):**
   - Rantai panggilan sinkron yang panjang (*cascading latency*) berhasil diputus.
   - Modul Pesanan tidak lagi menunggu (*non-blocking*) proses konfirmasi resto maupun pencarian kurir. Begitu pembayaran terverifikasi, pelanggan langsung menerima kepastian status pesanan di layar, sehingga *thread pool* server tidak terkunci dan siap melayani pesanan berikutnya saat jam sibuk.

3. **Menjawab Masalah Single Point of Failure & Bottleneck Monolitik (Pitfall 3 Tugas 1):**
   - Modul Pembayaran dipisahkan menjadi service tersendiri sehingga beban komputasinya terisolasi dan tidak lagi menjadi *bottleneck* yang menumbangkan seluruh aplikasi FoodGo.
   - Yang terpenting, Modul Kurir dan Modul Resto kini berjalan di proses/container yang sepenuhnya terpisah (*decoupled*). Tim kurir dapat melakukan pembaruan kode dan deploy ulang kapan saja tanpa memicu restart pada modul resto ataupun mengakibatkan *downtime* total.

**Kesimpulan Akhir:**  
Pilihan arsitektur hybrid (SOA sinkron untuk transaksi checkout dan pembayaran + Pub-Sub asinkron via Message Broker untuk penanganan resto dan kurir) adalah solusi paling ideal untuk kebutuhan FoodGo. Meskipun arsitektur ini memunculkan trade-off baru berupa kompleksitas pelacakan pesan non-linear dan kebutuhan konfigurasi broker yang *reliable*, trade-off tersebut sangat sebanding dengan keandalan dan skalabilitas sistem yang didapatkan.

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26 September 2026 | Claude 3.5 Sonnet | "Apa perbedaan mendasar dan trade-off antara arsitektur SOA request-response dengan Publish-Subscribe untuk sistem food delivery saat lonjakan trafik?" | AI memberikan penjelasan tentang perbandingan latensi, coupling waktu, dan menyarankan penggunaan Saga Pattern atau event-driven murni. | Kelompok mengambil konsep pemisahan event asinkron untuk resto dan kurir, tetapi menolak saran Saga Pattern karena dinilai over-engineering untuk skala tugas pekan 2. Kelompok merumuskan sendiri pendekatan hybrid SOA + Pub-Sub yang sesuai kebutuhan studi kasus FoodGo. |
| 26 September 2026 | ChatGPT (GPT-4o) | "Bantu berikan contoh sintaks dasar Mermaid graph TD untuk menggambarkan alur service dengan panah solid sinkron dan putus-putus asinkron." | AI memberikan template dasar sintaks Mermaid menggunakan `-->` dan `-.->`. | Template sintaks dasar tersebut kami modifikasi sendiri untuk memetakan 6 komponen nyata FoodGo (Gateway, Pesanan, Pembayaran, Broker, Resto, Kurir) beserta urutan langkah konkret 1 sampai 8. |
