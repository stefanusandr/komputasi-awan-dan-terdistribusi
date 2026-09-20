# Rubrik Umum & Kebijakan Penggunaan AI (Level 2)

Dokumen ini berlaku untuk **semua** tugas (Tugas 1–15). Rubrik spesifik di tiap folder tugas adalah tambahan di atas dasar ini, bukan pengganti.

## 1. Aturan Kerja Kelompok

- Kelompok terdiri dari **3–4 mahasiswa**. Kelompok didaftarkan sekali di awal semester dan konsisten untuk semua tugas kecuali dosen menyatakan lain.
- Setiap anggota **wajib punya commit atas namanya sendiri** (bukan di-commit-kan orang lain) di setiap tugas. Kontribusi minimal: satu bagian kode/analisis yang bisa ditelusuri ke satu anggota.
- Di `README.md` submission, cantumkan tabel pembagian tugas:

  | Nama | NIM | Kontribusi |
  |---|---|---|
  | ... | ... | mis. "implementasi bully algorithm, load test" |

- Jika ada anggota yang tidak berkontribusi (nol commit di seluruh tugas, tidak disebut di tabel kontribusi manapun), nilainya dipisahkan dari kelompok.

## 2. Batasan "Cukup Laptop, Tanpa Biaya Cloud"

- Semua simulasi "server", "node", "VM", "cluster" dijalankan **lokal** di laptop, memakai Docker/Docker Compose atau proses lokal (`localhost` + port berbeda).
- Dilarang mendaftar layanan cloud berbayar atau memasukkan kartu kredit untuk tugas apa pun di repo ini. Satu-satunya pengecualian: Tugas 12 (PaaS) yang memang butuh akun **free-tier tanpa biaya** — caranya dijelaskan di README tugas tersebut.
- Jika laptop kalian tidak kuat menjalankan Docker (RAM sangat terbatas), hubungi dosen/asisten untuk alternatif (mis. lab kampus), bukan menyewa cloud sendiri.

## 3. Kebijakan Penggunaan AI — Level 2 (AI Assisted Idea Generation & Structuring)

Mata kuliah ini mengikuti kerangka **5-Level Penggunaan AI Telkom University**, dan seluruh tugas di repo ini ditetapkan di **Level 2**:

| Level | Nama | Status di mata kuliah ini |
|---|---|---|
| 1 | No AI | Bukan level ini — AI boleh dipakai sebatas ideation/structuring |
| **2** | **AI Assisted Idea Generation & Structuring** | **Level yang berlaku untuk semua tugas** |
| 3 | AI Editing | Dilarang — AI tidak boleh mengedit/memperbaiki kode atau tulisan kalian |
| 4 | AI Task Completion with Human Evaluation | Dilarang — AI tidak boleh menyelesaikan tugas walau dicek ulang manusia |
| 5 | Full AI | Dilarang |

### 3.1 Batasan Konkret Level 2

**Boleh** — AI dipakai sebagai partner diskusi di tahap *awal*, sebelum kalian menulis/mengetik sendiri:
- Brainstorming ide/alternatif pendekatan (mis. "apa saja algoritma election selain Bully?").
- Membantu menyusun **outline/struktur** (kerangka bagian apa saja yang perlu dibahas), bukan isinya.
- Menjelaskan konsep yang belum dipahami (bertanya "apa itu X", bukan "kerjakan X untuk saya").

**Tidak boleh** — AI menghasilkan **konten akhir** yang tinggal disalin/ditempel:
- Meminta AI menuliskan kode (lengkap atau sebagian signifikan) untuk mengisi bagian `# TODO` di skeleton.
- Meminta AI menulis draf akhir analisis/README/jurnal yang lalu ditempel langsung.
- Meminta AI memperbaiki (*editing*) kode atau tulisan yang sudah ada — ini masuk Level 3, bukan Level 2.
- Meminta AI membuat diagram/gambar arsitektur final.

Batas praktisnya: **ide boleh dari AI, tapi kalimat, baris kode, dan keputusan akhir harus keluar dari tangan kalian sendiri**, sebagai hasil olahan atas ide tadi — bukan hasil salin-tempel.

### 3.2 Cara Verifikasi

Karena Level 2 tetap mengizinkan AI (bukan melarang total seperti Level 1), verifikasi berfokus pada **membuktikan pengolahan/pemahaman manusia atas hasil akhir**, bukan sekadar mendeteksi "apakah AI pernah dipakai":

1. **Log Penggunaan AI di `JURNAL.md`.** Setiap sesi pemakaian AI (tools, prompt, ringkasan saran, dan bagaimana diolah jadi hasil sendiri) wajib dicatat. Log kosong ("Tidak memakai AI") juga valid jika memang tidak dipakai.
2. **Commit history granular.** Commit tunggal raksasa berisi solusi jadi tetap dicurigai — proses (draf salah, revisi, debugging) harus terlihat bertahap, mencerminkan pengolahan manual, bukan tempel-sekali-jadi.
3. **Bukti eksekusi nyata.** Screenshot terminal dengan timestamp/hostname asli, atau video demo singkat (1–3 menit, tidak perlu editing) yang menunjukkan program benar-benar jalan di laptop kalian — bukan cuma potongan kode.

Catatan: mata kuliah ini **tidak** memakai sesi tanya-jawab/viva lisan sebagai mekanisme verifikasi (tidak sustainable untuk skala 5 kelas). Verifikasi sepenuhnya berbasis artefak asinkron di atas (log AI, commit history, `JURNAL.md`, bukti eksekusi), yang bisa diperiksa dosen/asisten kapan saja tanpa perlu sesi langsung dengan tiap kelompok.

Konsekuensi pelanggaran batas Level 2 (mis. konten akhir terbukti hasil generate AI tanpa diolah, atau log AI tidak jujur) mengikuti aturan integritas akademik kampus (indikasi awal → klarifikasi; terbukti → nilai 0 untuk tugas terkait, kasus berat dieskalasi).

## 4. Struktur Rubrik Penilaian (Bobot Dasar)

Tiap tugas memakai variasi dari bobot berikut (persentase spesifik ada di README masing-masing tugas):

| Komponen | Bobot Tipikal | Yang Dinilai |
|---|---|---|
| Kebenaran teknis / fungsionalitas | 35% | Kode berjalan, simulasi/analisis sesuai konsep materi minggu itu |
| Kedalaman analisis (`README.md`/`ANALISIS.md`) | 30% | Bukan sekadar deskripsi, tapi *kenapa* solusi ini dipilih dibanding alternatif |
| Proses & jurnal (`JURNAL.md`, commit history, Log Penggunaan AI) | 20% | Keaslian proses, iterasi, debugging yang tercatat, kejujuran & kepatuhan log AI terhadap batas Level 2 |
| Kerja sama kelompok & bukti demo | 15% | Pembagian kontribusi jelas di tabel kontribusi + commit history, video/screenshot eksekusi valid |

## 5. Format Submission Standar

Kecuali disebutkan lain di README tugas spesifik, tiap folder submission berisi:

```
tugas-XX-.../
├── README.md        # Analisis studi kasus (soal ada di README materi)
├── JURNAL.md         # Log proses berpikir & debugging
├── src/              # Kode (jika tugas menuntut implementasi)
├── bukti/            # Screenshot/video demo eksekusi
└── (file lain sesuai instruksi spesifik, mis. diagram/, Dockerfile)
```

## 6. Cara Submit & Menilai di LMS (Moodle)

- Mahasiswa mengumpulkan **link permalink git tag** (bukan Pull Request) ke assignment Moodle tugas terkait — lihat tutorial & contoh di [`HANDBOOK.md`](HANDBOOK.md#25-cara-submit-tugas-git-tag--link-ke-lms-moodle).
- Assignment Moodle diset sebagai **Group Assignment** (satu submission per kelompok, bukan per mahasiswa) dengan tipe submission **Online text/URL**.
- Untuk penilaian, gunakan **Moodle Rubric grading method** per assignment. Template rubrik tiap tugas (format CSV, siap dipakai sebagai referensi untuk mengisi rubrik di Moodle) tersedia secara lokal di folder `rubrik-moodle/` — folder ini **tidak ikut ter-commit ke repo** (lihat `.gitignore`) karena berisi rincian penilaian internal, bukan materi untuk mahasiswa.

Lihat [`HANDBOOK.md`](HANDBOOK.md) untuk tutorial teknis (Git, Docker, dst).
