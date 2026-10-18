# Jurnal Proses — Tugas 5

## Implementasi Bully
- **Kendala saat mengisi TODO 1-4:**
  - **TODO 1 (`on_message`):** Saat banyak node dijalankan hampir bersamaan, banyak thread koneksi dibuat sekaligus (`handle_connection`). Jika setiap kali menerima `ELECTION` node memicu thread baru `start_election()`, terjadi duplikasi pemilihan secara masif. Solusinya, ditambahkan guard `self.election_in_progress` dan pengecekan apakah node sudah berstatus leader (`self.leader_id == self.node_id`) agar node yang sudah jadi leader langsung merespons dengan `COORDINATOR` tanpa memicu election ulang. Selain itu, pada sistem operasi Windows ditemukan kendala `UnicodeEncodeError: 'charmap' codec can't encode character '\u2605'` saat mencetak simbol bintang ke console cp1252, sehingga simbol diganti dengan format ASCII standar (`***`).
  - **TODO 2 (`start_election`):** Penanganan timeout non-blocking sebesar 2.0 detik (`ELECTION_TIMEOUT`) untuk menunggu balasan `OK` dari node-node yang ber-ID lebih tinggi. Flag `self.received_ok` harus di-reset setiap kali election baru dimulai. Apabila ada pesan `COORDINATOR` yang masuk saat proses menunggu timeout berlangsung, node tidak boleh menimpa leader tersebut dan harus membatalkan pencalonannya.
  - **TODO 3 (`declare_leader`):** Membutuhkan sinkronisasi thread menggunakan `self.lock` untuk mengamankan modifikasi status `self.leader_id = self.node_id` dan `self.election_in_progress = False`, kemudian melakukan iterasi broadcast `COORDINATOR` ke semua peers (`self.peers`).
  - **TODO 4 (`monitor_leader`):** Menentukan mekanisme liveness probe. Node leader tidak boleh mem-ping dirinya sendiri, dan jika sedang dalam masa election (`in_progress`), polling ditangguhkan. Pengecekan dilakukan periodik setiap 3 detik dengan mencoba membuka koneksi socket TCP ("PING"). Jika koneksi ditolak (`ConnectionRefusedError`), berarti leader mati, sehingga node mereset `self.leader_id = None` dan segera memanggil `start_election()`.

## Skenario 1: Start normal
- **Leader yang terpilih:** Node 5 (port 5005).
- **Log/observasi:** 
  - Saat Node 1 hingga Node 5 dinyalakan hampir bersamaan di localhost:
    - Node 1 memulai election ke Node 2, 3, 4, 5. Node 2, 3, 4, 5 membalas dengan pesan `OK` sehingga Node 1 mundur dari pencalonan.
    - Node 2 memulai election ke Node 3, 4, 5 dan menerima `OK` dari Node 3, 4, 5 lalu mundur.
    - Node 3 memulai election ke Node 4, 5 dan menerima `OK` dari Node 4, 5 lalu mundur.
    - Node 4 memulai election ke Node 5 dan menerima `OK` dari Node 5 lalu mundur.
    - Node 5 mendapati himpunan peer ber-ID lebih tinggi kosong (`higher_peers = []`), sehingga Node 5 langsung mendeklarasikan diri sebagai leader (`*** SAYA ADALAH LEADER BARU! ***`) dan menyiarkan pesan `COORDINATOR` ke seluruh node (1, 2, 3, 4).
  - Seluruh node 1, 2, 3, dan 4 berhasil menerima pesan `COORDINATOR` dari Node 5 dan serempak mencatat `leader_id = 5`.

## Skenario 2: Leader dimatikan
- **Leader baru yang terpilih:** Node 4 (port 5004).
- **Berapa lama waktu sampai leader baru terdeteksi:** ~3 hingga 5 detik.
  - Durasi ini terdiri dari interval loop monitoring (maksimal 3 detik) ditambah `ELECTION_TIMEOUT` (2 detik) untuk menunggu respons dari node ber-ID lebih tinggi.
- **Log/observasi:**
  - Ketika proses Node 5 dihentikan (terminasi proses), thread `monitor_leader` pada node yang tersisa (Node 1–4) mendeteksi kegagalan koneksi TCP ke port 5005 (`Leader (node 5) TIDAK MERESPONS!`).
  - Pemilihan ulang (*re-election*) terpicu:
    - Node 1 mengirim `ELECTION` ke 2, 3, 4, 5. Node 2, 3, 4 merespons `OK` ke Node 1.
    - Node 2 mengirim `ELECTION` ke 3, 4, 5. Node 3 dan 4 merespons `OK` ke Node 2.
    - Node 3 mengirim `ELECTION` ke 4 dan 5. Node 4 merespons `OK` ke Node 3.
    - Node 4 mengirim `ELECTION` ke Node 5. Karena Node 5 sudah mati, tidak ada respons `OK` yang kembali selama batas waktu 2 detik.
    - Node 4 mendeklarasikan diri sebagai leader baru (`*** SAYA ADALAH LEADER BARU! ***`) dan menyiarkan pesan `COORDINATOR` ke seluruh peer yang masih hidup (Node 1, 2, dan 3).
  - Node 1, 2, dan 3 menerima `COORDINATOR` dari Node 4 dan serempak memperbarui leader mereka ke Node 4.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-10-18 | Antigravity | Bagaimana alur kerja Bully Algorithm dan cara menangani timeout balasan OK serta koordinasi state antar-thread di Python socket? | Penjelasan konsep Bully (ELECTION, OK, COORDINATOR), mekanisme deteksi node gagal via timeout koneksi socket, dan penggunaan state flag dengan threading.Lock. | Diimplementasikan secara mandiri ke dalam metode TODO 1-4 di `src/node.py` dengan penyesuaian protokol pesan TCP sederhana, penanganan crash encoding cp1252 Windows, dan penulisan laporan analisis komparatif FoodGo. |
