# Jurnal Proses — Tugas 5

## Implementasi Bully
- **Kendala saat mengisi TODO 1-4:**
 ## Daftar Tugas (TODO) Implementasi Leader Election

- [ ] **TODO 1: Optimasi Handler `on_message`** 
  - **Konteks:** Eksekusi banyak node secara bersamaan memicu lonjakan thread koneksi (`handle_connection`). Tanpa batasan, pesan `ELECTION` yang masuk bertubi-tubi akan memicu proses pemilihan secara redundan.
  - **Tindakan:**
    - Tambahkan *guard flag* `self.election_in_progress`.
    - Lakukan verifikasi status kepemimpinan (`self.leader_id == self.node_id`). Jika node sudah menjadi *leader*, wajib langsung membalas dengan pesan `COORDINATOR` tanpa memulai pemilihan ulang.
    - **Bugfix Terminal Windows:** Ganti karakter Unicode bintang (`\u2605`) menjadi ASCII standar (`***`) untuk mencegah *crash* `UnicodeEncodeError: 'charmap' codec can't encode character` pada *console* (cp1252).

- [ ] **TODO 2: Mekanisme Timeout di `start_election`** 
  - **Tindakan:**
    - Terapkan *timeout non-blocking* selama `2.0` detik (`ELECTION_TIMEOUT`) untuk menunggu balasan `OK` dari node dengan ID yang lebih besar.
    - Pastikan nilai *flag* `self.received_ok` selalu di-*reset* setiap kali memulai sesi pemilihan baru.
    - **Resolusi Konflik:** Apabila di tengah waktu tunggu node menerima pesan `COORDINATOR` dari node lain, segera batalkan pencalonan diri agar tidak terjadi penimpaan posisi *leader*.

- [ ] **TODO 3: Sinkronisasi Thread di `declare_leader`** 
  - **Tindakan:**
    - Implementasikan penguncian *thread* (`self.lock`) untuk mencegah *race condition* saat memperbarui *state* internal:
      - `self.leader_id = self.node_id`
      - `self.election_in_progress = False`
    - Setelah *state* aman diperbarui, lakukan *broadcast* pesan `COORDINATOR` secara iteratif ke semua koneksi *peers* yang aktif (`self.peers`).

- [ ] **TODO 4: Mekanisme Liveness Probe di `monitor_leader`** 
  - **Tindakan:**
    - Buat pengecekan ketersediaan (rutin setiap `3` detik) dengan mengirimkan *ping* melalui koneksi TCP socket (`"PING"`).
    - **Pengecualian:** Node *leader* tidak boleh melakukan *ping* ke dirinya sendiri, dan proses *polling* harus ditangguhkan ( *paused* ) selama proses pemilihan sedang berlangsung.
    - **Failover:** Jika hasil *ping* ditolak (`ConnectionRefusedError`), asumsikan *leader* telah *down*. Segera *reset* nilai `self.leader_id = None` dan eksekusi `start_election()` untuk memicu pemilihan baru.

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
