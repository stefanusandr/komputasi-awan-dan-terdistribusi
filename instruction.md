Berikut adalah usulan pembaruan untuk **Tugas 1 hingga 15** (kecuali Tugas 8 yang merupakan UTS) dengan metode **Problem Based Learning (PBL)**. Soal-soal ini dirancang agar relevan dengan materi per pekan dalam RPS dan dapat diimplementasikan menggunakan **GitHub** di mana mahasiswa melakukan *fork* dari repositori Anda.

Untuk menjaga integritas "**No AI**", setiap tugas mewajibkan mahasiswa menyertakan dokumentasi langkah demi langkah (*thought process*) dan analisis mendalam di file `README.md` mereka.

### **Bagian 1: Sistem Terdistribusi**

**Tugas 1 (Pekan 1): Identifikasi Masalah & Pitfall**
*   **Materi:** Definisi, Tujuan Desain, Pitfall.
*   **Masalah (Problem):** Sebuah startup "FoodGo" mengalami kegagalan sistem saat pesanan melonjak. Sistem mereka lambat dan sering *crash* karena mengasumsikan jaringan selalu aman dan latensi nol.
*   **Tugas Mahasiswa:** Menganalisis 3 *pitfalls* utama sistem terdistribusi yang dialami startup tersebut berdasarkan skenario yang diberikan dan mengusulkan solusi desain awal di repositori GitHub.

**Tugas 2 (Pekan 2): Perancangan Arsitektur**
*   **Materi:** Architectural Style (Layered, SOA, Pub-Sub).
*   **Masalah:** Startup "FoodGo" butuh sistem yang *decoupled* agar tim kurir dan tim resto tidak saling mengganggu jika salah satu modul diperbarui.
*   **Tugas Mahasiswa:** Menggambar dan menjelaskan rancangan arsitektur menggunakan gaya *Service-Oriented Architecture* (SOA) atau *Publish-Subscribe*. Mahasiswa mengunggah diagram (dalam format `.png`/`.md`) ke folder arsitektur di GitHub.

**Tugas 3 (Pekan 3): Efisiensi Proses & Kontainer**
*   **Materi:** Threading, Virtualization, Containers.
*   **Masalah:** Server "FoodGo" boros sumber daya karena setiap permintaan diproses sebagai proses baru yang berat.
*   **Tugas Mahasiswa:** Implementasikan program Python sederhana yang menggunakan *multithreading* untuk menangani simulasi pesanan masuk. Program tersebut harus dipaketkan ke dalam **Docker Container**. Mahasiswa menyertakan `Dockerfile` di repositori.

**Tugas 4 (Pekan 4): Komunikasi Antar Komponen**
*   **Materi:** RPC, Message-Queuing (MOM).
*   **Masalah:** Modul pembayaran dan modul pesanan harus berkomunikasi secara reliabel tanpa harus menunggu respon instan (*asynchronous*).
*   **Tugas Mahasiswa:** Membangun purwarupa komunikasi sederhana menggunakan **RPC** untuk permintaan sinkron atau **Message Passing** (seperti RabbitMQ/MQTT) untuk asinkron. Kode sumber diunggah ke GitHub.

**Tugas 5 (Pekan 5): Koordinasi & Konsensus**
*   **Materi:** Physical/Logical Clock, Election Algorithm.
*   **Masalah:** Terjadi konflik waktu pada urutan pesanan dan sistem membutuhkan satu "Node Leader" untuk mengelola antrean pesanan.
*   **Tugas Mahasiswa:** Mengimplementasikan simulasi **Bully Algorithm** atau **Raft** sederhana untuk menentukan leader di antara 5 node virtual. Hasil pemilihan leader harus dicatat dalam log di GitHub.

**Tugas 6 (Pekan 6): Penamaan & Resolusi Lokasi**
*   **Materi:** Flat Naming, Structured Naming (DNS), DHT.
*   **Masalah:** Pelanggan kesulitan menemukan alamat IP server kurir yang dinamis (selalu berubah).
*   **Tugas Mahasiswa:** Mensimulasikan cara kerja **Distributed Hash Table (DHT)** atau **Chord** untuk memetakan ID Kurir ke alamat IP mereka saat ini. Penjelasan teknis ditulis di `README.md`.

**Tugas 7 (Pekan 7): Konsistensi Data**
*   **Materi:** Data-Centric, Client-Centric Consistency.
*   **Masalah:** Data saldo *e-wallet* pelanggan berbeda di server wilayah Jakarta dan Bandung karena replikasi yang lambat.
*   **Tugas Mahasiswa:** Menganalisis skenario tersebut dan menentukan apakah sistem memerlukan *Sequential Consistency* atau *Eventual Consistency*. Mahasiswa harus mendemonstrasikan pemahaman melalui diagram alir urutan data (*read/write*) di GitHub.

---

### **Bagian 2: Komputasi Awan**

**Tugas 9 (Pekan 9): Cloud Delivery & Deployment**
*   **Materi:** Karakteristik Cloud, NIST Model.
*   **Masalah:** Pemerintah ingin membangun sistem data kependudukan yang sangat rahasia namun butuh skalabilitas cloud.
*   **Tugas Mahasiswa:** Memberikan rekomendasi model *deployment* (Public/Private/Hybrid) dan *service model* yang tepat. Jawaban diunggah dalam file Markdown di GitHub.

**Tugas 10 (Pekan 10): Arsitektur Cloud yang Skalabel**
*   **Materi:** Workload Distribution, Resource Pooling, Dynamic Scalability.
*   **Masalah:** Sebuah situs web tiket konser "mogok" karena tidak mampu menangani 1 juta pengguna dalam 1 menit.
*   **Tugas Mahasiswa:** Merancang arsitektur cloud menggunakan *Load Balancer* dan *Auto-scaling*. Analisis perbandingan *Horizontal* vs *Vertical Scaling* harus disertakan.

**Tugas 11 (Pekan 11): Implementasi IaaS**
*   **Materi:** Infrastructure as a Service (IaaS).
*   **Masalah:** Dibutuhkan server Linux kustom untuk menjalankan script otomasi perusahaan dengan biaya minimal.
*   **Tugas Mahasiswa:** Melakukan *provisioning* VM (menggunakan penyedia gratis seperti AWS Free Tier/Azure Student) dan mengunggah script Bash otomasi yang berjalan di VM tersebut ke GitHub.

**Tugas 12 (Pekan 12): Implementasi PaaS**
*   **Materi:** Platform as a Service (PaaS).
*   **Masalah:** Pengembang ingin fokus pada kode aplikasi Python tanpa mau mengurus sistem operasi atau *patching* keamanan server.
*   **Tugas Mahasiswa:** Mendeploy aplikasi web sederhana ke platform PaaS (seperti Heroku atau Google App Engine). Link aplikasi yang aktif dicantumkan di GitHub.

**Tugas 13 (Pekan 13): SaaS & Twelve-Factor App**
*   **Materi:** Software as a Service (SaaS), Twelve-Factor App.
*   **Masalah:** Aplikasi SaaS sering rusak saat dipindahkan dari lingkungan pengembangan ke produksi.
*   **Tugas Mahasiswa:** Mengaudit aplikasi sederhana mereka di GitHub berdasarkan **Twelve-Factor App** (fokus pada poin *Codebase, Dependencies,* dan *Config*).

**Tugas 14 (Pekan 14): Keamanan Cloud**
*   **Materi:** Shared Responsibility Model, Identity Management.
*   **Masalah:** Terjadi kebocoran data karena kunci akses (*access keys*) cloud bocor di repositori publik.
*   **Tugas Mahasiswa:** Mengimplementasikan pengaturan keamanan pada repositori GitHub mereka (misal: menggunakan *GitHub Secrets*) dan menjelaskan pembagian tanggung jawab keamanan antara penyedia cloud dan pengguna.

**Tugas 15 (Pekan 15): Studi Kasus Akhir**
*   **Materi:** Implementasi Cloud Sederhana.
*   **Masalah:** Bangunlah sebuah prototipe sistem "Smart City" sederhana yang menggabungkan sistem terdistribusi (simulasi sensor) dan penyimpanan cloud.
*   **Tugas Mahasiswa:** Proyek integrasi akhir. Mahasiswa harus menggabungkan minimal satu konsep sistem terdistribusi (dari tugas 1-7) ke dalam infrastruktur cloud (tugas 9-14) dalam satu repositori GitHub yang rapi.

### **Instruksi untuk Mahasiswa di Repo Utama:**
1.  **Fork** repositori ini ke akun Anda.
2.  Setiap pekan, kerjakan tugas di folder yang sesuai.
3.  Dilarang menggunakan AI untuk menghasilkan kode atau analisis. Kami akan memeriksa riwayat *commit* dan kedalaman analisis di `README.md`.
4.  Sertakan **video demo** atau **tangkapan layar** bukti pengerjaan teknis.