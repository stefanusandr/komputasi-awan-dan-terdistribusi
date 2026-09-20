# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [14-09-2026]
- Peserta: [Stefanus Andri Hendrawan, Fatih Khairu Alfifiajri, Moh Irham Maulana]
- Poin diskusi: pihak foodGo mengasumsi bahwa koneksi jaringannya tidak akan pernah gagal, hak ini menyebabkan terjadi nya paket loss saat grafik sedang tinggi dan untuk mengatasinya diperlukan perbaikan dalam kode nya dengan menerapkan mekanisme coba ulang(retry)
- Perbedaan pendapat (jika ada): -

## [19-09-2026]
- Peserta: [Stefanus Andri Hendrawan, Fatih Khairu Alfifiajri, Moh Irham Maulana]
- Poin diskusi: kegagalan foodGo saat trafik sedang tinggi disebabkan oleh kesalahan code pada jaringan yang membuat terjadinya kegagalan paket, untuk mengatasinya diperlukan penerapan pada kode retry mechanism, penambahan timeout, dan penerapan redudansi namun hal yang harus diperhatikan adanya penambahan biaya pada infrastruktur dan kompleksitas pengelolaan

## Review Silang
- [stefanus andri hendrawan] mengomentari analisis [Fatih Khairu Alfifiajri]: penerapan sistem time out juga perlu ditambahkan durasi time out nya supaya tidak terlalu cepat saat memutuskan koneksinya

## Log Penggunaan AI (Level 2)
menggunakan gemini ai untuk mencari ide dan wawasan baru bukan untuk mengcopas seluruh teks
> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| 09-19-2026 | Gemini | dampak ada dan tidaknya timeout pada aplikasi pesan antar makanan| menjelaskan definisi time out dan apa yang terjadi jika ada dan tidaknya time out pada aplikasi | mengolah kembali ringkasan tersebut sesuai dengan studi kasus FoodGo |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
