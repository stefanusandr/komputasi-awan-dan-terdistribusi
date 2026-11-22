# Jurnal Proses — Tugas 9

## Diskusi Deployment Model

### Opsi yang Dipertimbangkan:
1. **Public Cloud Murni:**
   - Pertimbangan: Menawarkan elastisitas terbaik (*auto-scaling* instan), biaya awal rendah (tanpa CapEx), dan infrastruktur global yang siap pakai.
   - Alasan Penolakan: Melanggar kedaulatan data hukum (UU PDP No. 27/2022 dan PP No. 71/2019). Menempatkan data kependudukan dan biometrik sensitif warga negara di infrastruktur *multi-tenant* pihak ketiga komersial asing menimbulkan risiko *extraterritorial subpoena* (mis. US CLOUD Act) dan ancaman sanksi pidana/denda hukum yang fatal bagi negara.

2. **Private Cloud Murni (On-Premise Pemerintah):**
   - Pertimbangan: Memberikan kontrol fisik dan yurisdiksi keamanan 100% di bawah kendali instansi pemerintah (Pusat Data Nasional / BSSN).
   - Alasan Penolakan: Gagal memenuhi karakteristik esensial NIST *Rapid Elasticity*. Pola akses kependudukan memiliki lonjakan ekstrem (*spikes*) musiman saat pendaftaran sekolah (PPDB), Pemilu/Pilkada, dan verifikasi bansos. Membangun kapasitas perangkat keras fisik mandiri seukuran beban puncak pemilu membutuhkan anggaran belanja modal (*CapEx*) raksasa yang 90% waktunya akan menganggur (*idle*). Jika tidak di-*overprovisioning*, server pemerintah dipastikan tumbang (*downtime*) saat terjadi lonjakan trafik jutaan kueri secara serentak.

3. **Community Cloud Antar-Instansi:**
   - Pertimbangan: Bagus untuk standarisasi antar-kementerian/lembaga negara, namun memiliki keterbatasan elastisitas yang serupa dengan private cloud jika tidak didukung oleh infrastruktur cloud publik skala masif.

### Kesimpulan Akhir & Alasan:
- **Model Terpilih:** **Hybrid Cloud (Sovereign Hybrid Cloud)**.
- **Alasan:** Merupakan satu-satunya model yang mampu menjembatani dua kutub kebutuhan yang berlawanan:
  - *Sisi Kerahasiaan (Confidentiality):* Data master kependudukan, biometrik, dan kunci enkripsi HSM tetap diisolasi 100% di dalam **Segmen Private Cloud (Pusat Data Nasional)**.
  - *Sisi Skalabilitas (Elasticity):* Penyerapan lonjakan kueri verifikasi dari ribuan instansi mitra (bank, sekolah, kepolisian) di-offload ke **Segmen Public/Edge Cloud** yang menjalankan *API Gateway, Caching*, dan *Zero-Knowledge Tokenization Proxy* dengan kapabilitas *rapid auto-scaling*.

---

## Diskusi Service Model per Komponen

Sistem data kependudukan dipetakan secara terstruktur ke dalam arsitektur multi-tier:

1. **Basis Data Inti Kependudukan & Biometric Matching Engine $\to$ IaaS (Private Cloud / PDN)**
   - Mengapa IaaS? Dibutuhkan kendali administratif mutlak hingga tingkat sistem operasi kernel, pengaturan parameter disk I/O, konfigurasi enkripsi *data-at-rest* tingkat rendah (LUKS/AES-256), serta integrasi perangkat keras khusus (*Hardware Security Module* - HSM dan akselerator komputasi biometrik) yang tidak dapat disediakan oleh model PaaS/SaaS komersial.

2. **API Gateway, Rate Limiting, Caching, & Tokenization Engine $\to$ PaaS (Public/Edge Cloud)**
   - Mengapa PaaS? Memanfaatkan *Managed Container Platform* (seperti Managed Kubernetes / K8s, Redis Cluster, dan Kafka). Pengembang dapat berfokus penuh pada logika bisnis autentikasi mTLS, perutean lalu lintas, dan mitigasi DDoS tanpa perlu dipusingkan oleh pemeliharaan dan penambalan kerentanan (*security patching*) sistem operasi server fisik. Karakteristik PaaS memungkinkan *auto-scale out* kontainer dalam hitungan detik saat musim lonjakan kueri tiba.

3. **Portal Pengecekan Status Warga & Aplikasi Petugas Dukcapil Daerah (SIAK Web) $\to$ SaaS**
   - Mengapa SaaS? Menyajikan antarmuka siap pakai (*turn-key*) berbasis web browser bagi masyarakat umum dan operator kelurahan/kecamatan. Pengguna akhir tidak perlu memasang perangkat lunak atau memelihara basis data lokal, cukup melakukan login aman terotentikasi.

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-22 | Antigravity (Gemini) | Brainstorming penerapan 5 karakteristik esensial NIST SP 800-145 pada sistem data kependudukan nasional yang memiliki kebutuhan kedaulatan data dan lonjakan trafik pemilu | AI menyarankan pemetaan 5 poin karakteristik NIST (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dan mengusulkan pemisahan segmen private vs public | Ide disintesis secara mendalam dengan konteks regulasi nyata di Indonesia (UU PDP No. 27/2022, PP PSTE No. 71/2019, dan Pusat Data Nasional), merumuskan arsitektur Sovereign Hybrid Cloud, serta menyusun diagram Mermaid arsitektur terintegrasi. |
| 2026-11-22 | Antigravity (Gemini) | Brainstorming skenario tandingan ekstrem untuk sistem kependudukan di daerah pelosok/3T yang minim infrastruktur IT | AI menyarankan skenario keterbatasan infrastruktur lokal pemda dan solusi sentralisasi berbasis lightweight client | Elaborasi dikembangkan menjadi model Government Community Cloud berbasis *Hub-and-Spoke* via SaaS terpusat di Pusat Data Nasional (PDN) dengan dukungan konektivitas Palapa Ring / Satelit SATRIA-1 dan protokol *store-and-forward* terenkripsi. |
